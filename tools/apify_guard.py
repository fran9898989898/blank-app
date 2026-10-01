"""Única puerta a Apify. Todos los scripts de tools/ llaman a `run()`; nadie llama a la API de actores directamente.

Reglas (auditoría 1-oct-2026: $3,08 de $9,86 se fueron en reintentos y búsquedas repetidas):
  - maxItems ≤ 30 por run (se recorta en el input: resultsLimit / maxItems / maxResults).
  - maxTotalChargeUsd ≤ 0,50 por run.
  - Antes de cada run lee el gasto REAL del ciclo en la API de Apify y lo compara con la base de la sesión:
    si (gastado en la sesión + tope del run) > $2 → no lanza y avisa.
  - Sin reintentos: un fallo se devuelve como error; quien llama decide.
  - Caché de 7 días por (actor + input): la misma consulta no se paga dos veces.

Uso:
  python tools/apify_guard.py --nueva-sesion     # fija la base de gasto (al empezar cada sesión)
  python tools/apify_guard.py --estado           # gasto real de la sesión y del ciclo
Como módulo:  from apify_guard import run;  items = run("apify~rag-web-browser", {...})
"""
import argparse
import hashlib
import json
import os
import sys
import time

import requests

API = "https://api.apify.com/v2"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".apify_cache")
LEDGER = os.path.join(ROOT, "auditoria", "sesion_apify.json")
MAX_ITEMS = 30
MAX_RUN_USD = 0.50
MAX_SESSION_USD = 2.00
CACHE_DAYS = 7
ITEM_KEYS = ("resultsLimit", "maxItems", "maxResults")


class GuardError(RuntimeError):
    pass


def _token():
    t = os.environ.get("APIFY_TOKEN")
    if not t:
        raise GuardError("Falta APIFY_TOKEN.")
    return t


def gasto_ciclo():
    r = requests.get(f"{API}/users/me/usage/monthly", headers={"Authorization": f"Bearer {_token()}"}, timeout=30)
    r.raise_for_status()
    return float(r.json()["data"]["totalUsageCreditsUsdAfterVolumeDiscount"])


def _ledger():
    if not os.path.exists(LEDGER):
        raise GuardError("No hay sesión abierta: ejecuta `python tools/apify_guard.py --nueva-sesion`.")
    return json.load(open(LEDGER))


def nueva_sesion():
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    base = gasto_ciclo()
    json.dump({"inicio": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "base_usd": base, "runs": []},
              open(LEDGER, "w"), indent=1)
    return base


def estado():
    led = _ledger()
    ciclo = gasto_ciclo()
    return {"inicio": led["inicio"], "gastado_sesion": round(ciclo - led["base_usd"], 3), "ciclo": round(ciclo, 3),
            "limite_sesion": MAX_SESSION_USD, "runs": len(led["runs"])}


def _key(actor, inp):
    return hashlib.sha256((actor + json.dumps(inp, sort_keys=True)).encode()).hexdigest()[:32]


def clamp(inp):
    inp = dict(inp)
    for k in ITEM_KEYS:
        if k in inp and (inp[k] is None or inp[k] > MAX_ITEMS):
            inp[k] = MAX_ITEMS
    return inp


def run(actor, inp, tope_usd=MAX_RUN_USD, timeout=300, dry_run=False):
    """Lanza un actor con las reglas de arriba. Devuelve los items del dataset (lista)."""
    inp = clamp(inp)
    tope = min(float(tope_usd), MAX_RUN_USD)
    key = _key(actor, inp)
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < CACHE_DAYS * 86400:
        return json.load(open(path))["items"]
    led = _ledger()
    gastado = gasto_ciclo() - led["base_usd"]
    if gastado + tope > MAX_SESSION_USD:
        raise GuardError(f"Corte de sesión: gastado ${gastado:.2f} + tope del run ${tope:.2f} > ${MAX_SESSION_USD:.2f}. "
                         "No se lanza.")
    if dry_run:
        return {"lanzaria": actor, "input": inp, "tope_usd": tope, "gastado_sesion": round(gastado, 3)}
    r = requests.post(f"{API}/acts/{actor}/run-sync-get-dataset-items",
                      headers={"Authorization": f"Bearer {_token()}"},
                      params={"timeout": timeout, "maxTotalChargeUsd": tope, "maxItems": MAX_ITEMS},
                      json=inp, timeout=timeout + 30)
    r.raise_for_status()  # sin reintentos
    items = r.json()
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"actor": actor, "input": inp, "fecha": time.time(), "items": items}, open(path, "w"))
    led["runs"].append({"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "actor": actor, "key": key,
                        "items": len(items)})
    json.dump(led, open(LEDGER, "w"), indent=1)
    return items


def sembrar_cache(actor, inp, items):
    """Guarda en caché un resultado ya pagado (p. ej. leído de un dataset antiguo) sin lanzar nada."""
    inp = clamp(inp)
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"actor": actor, "input": inp, "fecha": time.time(), "items": items},
              open(os.path.join(CACHE, _key(actor, inp) + ".json"), "w"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nueva-sesion", action="store_true")
    ap.add_argument("--estado", action="store_true")
    a = ap.parse_args()
    try:
        if a.nueva_sesion:
            print(f"Sesión abierta. Base de gasto del ciclo: ${nueva_sesion():.3f}")
        if a.estado:
            print(json.dumps(estado(), indent=1))
    except GuardError as e:
        sys.exit(str(e))
