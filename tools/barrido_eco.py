"""Barrido «economía primero»: para cada candidato calcula el margen con precios REALES antes de mirar nada más.

Uso:  APIFY_TOKEN=... python tools/barrido_eco.py barridos/AAAA-MM-DD-X/candidatos.json [--tope 2.0]
Salida: <carpeta>/eco.json (una ficha por candidato) y resumen por stderr.

Orden de puertas (se para en la primera que falla, para no gastar en lo que ya está muerto):
  1. Genérico AliExpress: búsqueda directa ($0) → los 3 más vendidos que contengan `ali_must` → coste =
     el mayor entre el precio leído en la ficha (navegador de Apify) y 0,5 × tachado (la ficha puede enseñar
     la oferta de bienvenida al visitante nuevo; sin oferta, precio normal ≈ mitad del tachado).
  2. Precio de rivales: fichas Shopify de los anunciantes de la Biblioteca (Apify) o `rivales` fijos del JSON.
  3. Margen = mediana rivales − Ali real − envío (`envio`, 8 por defecto) − 3 % pasarela.  < $15 → MUERE.
  4. Ancla Amazon (Apify): mínimo con ≥50 reseñas cuyo título contenga `amazon_must` (o `ali_must`). Si mínimo < 70 % de la mediana de rivales → aviso AMAZON.
  5. Biblioteca (raw ya guardado o Apify): anunciantes ≥21 d (dominios no retail, redes unidas con `redes`),
     días del anuncio más antiguo del LÍDER (el dominio con más anuncios), tiendas nuevas <21 d (enjambre).
Semáforo: VERDE = margen ≥15 + Amazon ok + 3–8 anunciantes ≥21 d + líder ≤120 d + persona "sí".
          AMARILLO = margen ≥15 pero falla una del resto. GRIS = margen <15 (se dice con cuánto).
Nunca inventa: dato que no se lee queda en None y la ficha lo dice.
"""
import argparse
import csv
import io
import json
import os
import re
import statistics
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from amazon_search import parse as amazon_parse  # noqa: E402
from meta_library import days_running, pick, run_actor  # noqa: E402
from web_read import read  # noqa: E402

HERE = os.path.dirname(__file__)
RETAIL = {"amazon.com", "walmart.com", "target.com", "temu.com", "etsy.com", "ebay.com", "facebook.com", "fb.me",
          "instagram.com", "amzn.to", "amzlink.to", "amzn.markable.ai", "m.shein.com", "urlgeni.us", "homedepot.com"}
COST = {"lib_ad": 0.005, "page": 0.016, "shopify": 0.007}  # costes reales medidos en la auditoría del 1-oct


class Budget:
    def __init__(self, tope):
        self.tope, self.used = tope, 0.0

    def spend(self, x):
        if self.used + x > self.tope:
            raise SystemExit(f"Tope de Apify ${self.tope} alcanzado (${self.used:.2f} gastado).")
        self.used += x


def ali_search(q):
    out = subprocess.run([sys.executable, os.path.join(HERE, "ali_search.py"), q, "--pages", "1"],
                         capture_output=True, text=True, timeout=200).stdout
    return list(csv.DictReader(io.StringIO(out)))


def sold(v):
    m = re.search(r"([\d,]+)", v or "")
    return int(m.group(1).replace(",", "")) if m else 0


def ali_real(pid, budget):
    budget.spend(COST["page"])
    md = read(f"https://www.aliexpress.us/item/{pid}.html?gatewayAdapt=glo2usa", tope=0.05)
    m = re.search(r"\$\s?(\d{1,3}\.\d\d)", md)
    ship = re.search(r"(?i)shipping[:\s]*(?:US\s*)?\$\s?(\d+\.\d\d)", md)
    return (float(m.group(1)) if m else None), (float(ship.group(1)) if ship else None)


def amazon(q, budget):
    budget.spend(COST["page"])
    rows = amazon_parse(read("https://www.amazon.com/s?k=" + urllib.parse.quote_plus(q)))
    out = []
    for r in rows:
        revs = r[3].replace(",", "").upper()
        n = float(revs[:-1]) * 1000 if revs.endswith("K") else float(revs or 0)
        out.append({"producto": r[0][:90], "precio": float(r[1]), "resenas": int(n), "mes": r[4]})
    return out


def library(cfg, carpeta, budget):
    ads = []
    for q in cfg["library_q"]:
        path = os.path.join(carpeta, "raw", q.replace(" ", "_") + ".json")
        if not os.path.exists(path):
            budget.spend(COST["lib_ad"] * 30)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            json.dump(run_actor(os.environ["APIFY_TOKEN"], q, 30, 0.25, True), open(path, "w"))
        ads += json.load(open(path))
    redes = {d: g for g in cfg.get("redes", []) for d in g.split("+")}
    excl = set(cfg.get("excluir", []))
    per, urls = {}, {}
    for a in ads:
        link = pick(a, "snapshot.linkUrl", "snapshot.cards.0.linkUrl") or ""
        u = urllib.parse.urlparse(link)
        d = u.netloc.lower().replace("www.", "")
        if not d or d in RETAIL or d in excl:
            continue
        key = redes.get(d, d)
        v = per.setdefault(key, {"n": 0, "dias": 0})
        v["n"] += 1
        v["dias"] = max(v["dias"], days_running(a) or 0)
        if "/products/" in u.path:
            urls.setdefault(key, f"https://{u.netloc}{u.path}")
    old = {k: v for k, v in per.items() if v["dias"] >= 21}
    nuevos = [k for k, v in per.items() if v["dias"] < 21]
    lider = max(old.items(), key=lambda kv: (kv[1]["n"], kv[1]["dias"]))[0] if old else None
    return {"anunciantes_21d": len(old), "nuevos_21d": len(nuevos), "lider": lider,
            "lider_dias": old[lider]["dias"] if lider else None,
            "mas_antiguo_tipo": max((v["dias"] for v in per.values()), default=0),
            "dominios": {k: v for k, v in sorted(per.items(), key=lambda kv: -kv[1]["dias"])},
            "urls": [urls[k] for k in old if k in urls][:4]}


def shopify(urls, budget):
    if not urls:
        return []
    budget.spend(COST["shopify"] * len(urls) * 2)
    out = subprocess.run([sys.executable, os.path.join(HERE, "shopify_prices.py")] + urls,
                         capture_output=True, text=True, timeout=320).stdout
    seen, prices = set(), []
    for r in csv.DictReader(io.StringIO(out)):
        if r["url"] not in seen and r["precio"]:
            seen.add(r["url"])
            prices.append({"url": r["url"], "producto": r["producto"][:60], "precio": float(r["precio"])})
    return prices


def evalua(cfg, carpeta, budget):
    f = {"k": cfg["k"], "tipo": cfg["tipo"], "cat": cfg.get("cat", ""), "persona": cfg.get("persona", "verificar")}
    # 1. AliExpress real
    must = [w.lower() for w in cfg.get("ali_must", [])]
    cands = [r for r in ali_search(cfg["ali_q"]) if r["precio"] and all(w in r["titulo"].lower() for w in must)]
    cands.sort(key=lambda r: -sold(r["vendidos"]))
    best = None
    for r in cands[:3]:
        real, ship = ali_real(r["id"], budget)
        if real is None:
            continue
        # La ficha puede mostrar la oferta de bienvenida al visitante nuevo. Coste conservador: el mayor entre
        # lo leído y la mitad del tachado (en fichas sin oferta, precio normal ≈ 0,5 × tachado: 10,02/20,88; 13,49/26,98).
        tach = float(r["tachado"]) if r["tachado"] else 0.0
        coste = max(real, round(0.5 * tach, 2))
        item = {"id": r["id"], "titulo": r["titulo"], "vendidos": r["vendidos"], "leido": real, "tachado": tach,
                "real": coste, "envio_ali": ship, "busqueda": float(r["precio"]), "url": r["url"], "foto": r.get("imagen", "")}
        if best is None or real + (ship or 0) < best["real"] + (best["envio_ali"] or 0):
            best = item
    f["ali"] = best
    # 2. Biblioteca + rivales
    lib = library(cfg, carpeta, budget)
    f["lib"] = lib
    rivales = [{"url": "", "producto": "fijo", "precio": p} for p in cfg.get("rivales", [])] or shopify(lib["urls"], budget)
    f["rivales"] = rivales
    med = statistics.median([r["precio"] for r in rivales]) if rivales else None
    f["precio_rivales"] = med
    # 3. Margen
    envio = cfg.get("envio", 8.0)
    if best and med:
        f["margen"] = round(med - best["real"] - (best["envio_ali"] or 0) - envio - 0.03 * med, 2)
        f["landed_pct"] = round(100 * (best["real"] + (best["envio_ali"] or 0)) / med)
    else:
        f["margen"], f["landed_pct"] = None, None
    if f["margen"] is None or f["margen"] < 15:
        f["semaforo"], f["motivo"] = "GRIS", (f"margen ${f['margen']}" if f["margen"] is not None else "sin precio real de Ali o de rivales")
        return f
    # 4. Amazon
    amz = amazon(cfg.get("amazon_q", cfg["ali_q"]), budget)
    amust = [w.lower() for w in cfg.get("amazon_must", cfg.get("ali_must", []))]
    rel = [a for a in amz if a["resenas"] >= 50 and all(w in a["producto"].lower() for w in amust)]
    f["amazon"] = sorted(rel, key=lambda a: a["precio"])[:5]
    amin = f["amazon"][0]["precio"] if f["amazon"] else None
    f["amazon_min"] = amin
    avisos = []
    if amin is not None and amin < 0.7 * med:
        avisos.append(f"Amazon a ${amin} (<70 % de ${med})")
    if not 3 <= lib["anunciantes_21d"] <= 8:
        avisos.append(f"{lib['anunciantes_21d']} anunciantes ≥21 d")
    if lib["lider_dias"] is None or lib["lider_dias"] > 120:
        avisos.append(f"líder con {lib['lider_dias']} d")
    if lib["nuevos_21d"] >= 5:
        avisos.append(f"enjambre: {lib['nuevos_21d']} tiendas nuevas <21 d")
    if f["persona"] != "sí":
        avisos.append("persona sin verificar")
    f["avisos"] = avisos
    f["semaforo"] = "VERDE" if not avisos else "AMARILLO"
    f["motivo"] = "; ".join(avisos) or "pasa todo"
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidatos")
    ap.add_argument("--tope", type=float, default=2.0)
    a = ap.parse_args()
    carpeta = os.path.dirname(a.candidatos)
    budget = Budget(a.tope)
    dest = os.path.join(carpeta, "eco.json")
    prev = json.load(open(dest)) if os.path.exists(dest) else {"gasto_estimado": 0, "fichas": []}
    hechos = {f["k"]: f for f in prev["fichas"]}
    out = list(prev["fichas"])
    for cfg in json.load(open(a.candidatos)):
        if cfg["k"] in hechos:
            continue
        f = None
        try:  # sin reintentos: un fallo deja el candidato sin ficha y se sigue
            f = evalua(cfg, carpeta, budget)
        except SystemExit as e:
            print(e, file=sys.stderr)
            break
        except Exception as e:  # noqa: BLE001 (GuardError incluido: corte de sesión)
            print(f"# {cfg['k']}: {e.__class__.__name__}: {e}", file=sys.stderr)
            if e.__class__.__name__ == "GuardError":
                break
        if f is None:
            continue
        out.append(f)
        json.dump({"gasto_estimado": round(prev["gasto_estimado"] + budget.used, 3), "fichas": out},
                  open(dest, "w"), ensure_ascii=False, indent=1)
        print(f"{f['semaforo']:8s} {f['k']:28s} margen={f['margen']} rivales={f['precio_rivales']} "
              f"ali={f['ali'] and f['ali']['real']} amz={f.get('amazon_min')} {f['motivo']}", file=sys.stderr)
    print(f"Gasto Apify estimado: ${budget.used:.2f}", file=sys.stderr)


if __name__ == "__main__":
    main()
