"""Cuenta operadores en la Biblioteca de Anuncios de Meta (US) vía un actor de Apify.

Uso:
  APIFY_TOKEN=... python tools/meta_library.py "sleep mask" "knee brace" --max 30 --tope 3
Salida (CSV por stdout): consulta, anunciantes distintos, dominios distintos, operadores >=30 días,
  anunciante con más anuncios, días del anuncio más antiguo, y una línea por anunciante.

- Actor configurable con APIFY_ACTOR (por defecto el scraper oficial de Apify de la Biblioteca).
- --tope: gasto máximo en USD por ejecución (se pasa a Apify como maxTotalChargeUsd) → el límite
  lo aplica Apify, no este script. Aun así, fija también un límite mensual en tu cuenta.
- Nunca inventa: si el actor no devuelve un campo, sale vacío.
"""
import argparse
import csv
import datetime as dt
import os
import sys
import urllib.parse
from collections import defaultdict

import requests

API = "https://api.apify.com/v2"
ACTOR = os.environ.get("APIFY_ACTOR", "apify~facebook-ads-scraper")


def library_url(q):
    params = {
        "active_status": "active",
        "ad_type": "all",
        "country": "US",
        "q": q,
        "search_type": "keyword_unordered",
        "media_type": "all",
    }
    return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode(params)


def run_actor(token, q, max_items, tope):
    body = {"startUrls": [{"url": library_url(q)}], "resultsLimit": max_items, "activeStatus": "active"}
    r = requests.post(
        f"{API}/acts/{ACTOR}/run-sync-get-dataset-items",
        params={"token": token, "maxTotalChargeUsd": tope, "timeout": 300},
        json=body,
        timeout=330,
    )
    r.raise_for_status()
    return r.json()


def pick(d, *keys):
    for k in keys:
        cur = d
        for part in k.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur not in (None, ""):
            return cur
    return ""


def days_running(ad):
    start = pick(ad, "startDate", "start_date", "startDateFormatted", "ad_delivery_start_time")
    if not start:
        return None
    try:
        if isinstance(start, (int, float)):
            d0 = dt.datetime.utcfromtimestamp(start)
        else:
            d0 = dt.datetime.fromisoformat(str(start)[:10])
        return (dt.datetime.utcnow() - d0).days
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("consultas", nargs="+")
    ap.add_argument("--max", type=int, default=30, help="anuncios por consulta (≈30 según la skill)")
    ap.add_argument("--tope", type=float, default=3.0, help="USD máx. por consulta")
    a = ap.parse_args()
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Falta APIFY_TOKEN en las variables de entorno.")
    w = csv.writer(sys.stdout)
    w.writerow(["consulta", "anunciante", "dominio", "anuncios", "dias_max", "resumen"])
    for q in a.consultas:
        ads = run_actor(token, q, a.max, a.tope)
        per = defaultdict(lambda: {"n": 0, "dias": 0, "dom": ""})
        for ad in ads:
            name = pick(ad, "pageName", "page_name", "snapshot.page_name") or "?"
            link = pick(ad, "snapshot.link_url", "linkUrl", "snapshot.cards.0.link_url")
            dom = urllib.parse.urlparse(link).netloc.replace("www.", "") if link else ""
            p = per[name]
            p["n"] += 1
            p["dias"] = max(p["dias"], days_running(ad) or 0)
            p["dom"] = p["dom"] or dom
        doms = {v["dom"] for v in per.values() if v["dom"]}
        ops30 = [k for k, v in per.items() if v["dias"] >= 30]
        top = max(per.items(), key=lambda kv: kv[1]["n"]) if per else ("", {"n": 0})
        oldest = max((v["dias"] for v in per.values()), default=0)
        w.writerow([q, "", "", len(ads), oldest,
                    f"anunciantes={len(per)} dominios={len(doms)} operadores_30d={len(ops30)} lider={top[0]}({top[1]['n']})"])
        for name, v in sorted(per.items(), key=lambda kv: -kv[1]["n"]):
            w.writerow([q, name, v["dom"], v["n"], v["dias"], ""])


if __name__ == "__main__":
    main()
