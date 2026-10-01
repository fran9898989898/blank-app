"""Paso 1 del barrido «Amazon primero»: por cada tipo, el EQUIVALENTE FUNCIONAL MÁS BARATO en Amazon US
con Prime y ≥100 reseñas (no el más vendido). Pasa si ese precio es ≥ $25 (--min).

Uso:  APIFY_TOKEN=... python tools/amazon_first.py barridos/<carpeta>/tipos_amazon.json [--min 25] [--tope 0.5]
Entrada: [{"k": "...", "tipo": "...", "q": "búsqueda amazon", "must": ["palabras", "del título"]}]
Salida: <carpeta>/amazon.json con, por tipo: equivalente más barato, los 5 primeros resultados, ventas/mes
del más vendido y las marcas más repetidas (para detectar marca que el comprador busca por su nombre).
Prime: el bloque de resultado menciona "Prime". Nunca inventa: si Amazon no devuelve resultados, queda en None.
"""
import argparse
import collections
import json
import os
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
from web_read import read  # noqa: E402


def num(s):
    s = (s or "").replace(",", "").upper()
    return int(float(s[:-1]) * 1000) if s.endswith("K") else int(float(s or 0))


def parse(md):
    out = []
    for blk in re.split(r"\n## ", md)[1:]:
        title = blk.split("\n", 1)[0].strip()
        price = re.search(r"Price, product page\[\$(\d+(?:\.\d\d)?)", blk)
        if not price:
            continue
        revs = re.search(r"\[\(([\d.,]+K?)\)\]", blk)
        bought = re.search(r"([\d.,]+K?)\+ bought in past month", blk)
        url = re.search(r"\]\((https://www\.amazon\.com/[^)\s]*?/dp/[A-Z0-9]{10})", blk)
        out.append({"titulo": title[:150], "precio": float(price.group(1)), "resenas": num(revs.group(1)) if revs else 0,
                    "mes": num(bought.group(1)) if bought else 0, "prime": "prime" in blk.lower(),
                    "sponsored": "sponsored" in blk.lower()[:400], "url": url.group(1) if url else ""})
    return out


def search(q):
    # Sin reintentos (auditoría 1-oct: 260 runs para 59 búsquedas). Si Amazon devuelve error, queda sin dato.
    return parse(read("https://www.amazon.com/s?k=" + urllib.parse.quote_plus(q) + "&ref=nb_sb_noss"))


def evalua(t, minimo, cache):
    path = os.path.join(cache, t["k"] + ".json")
    if os.path.exists(path):
        rows = json.load(open(path))
    else:
        try:
            rows = search(t["q"])
        except Exception as e:  # noqa: BLE001
            print(f"# {t['k']}: {e.__class__.__name__}", file=sys.stderr)
            rows = None
        if rows is not None:
            json.dump(rows, open(path, "w"))
        rows = rows or []
    must = [w.lower() for w in t["must"]]
    rel = [r for r in rows if all(w in r["titulo"].lower() for w in must)]
    ok = [r for r in rel if r["prime"] and r["resenas"] >= 100]
    cheapest = min(ok, key=lambda r: r["precio"]) if ok else None
    marcas = collections.Counter(r["titulo"].split()[0].strip(",").upper() for r in rel[:15])
    top = max(rel, key=lambda r: r["mes"]) if rel else None
    return {**t, "n_resultados": len(rows), "n_relevantes": len(rel), "barato": cheapest,
            "pasa": bool(cheapest and cheapest["precio"] >= minimo),
            "mas_vendido": top, "marcas_top": marcas.most_common(4), "top5": rel[:5]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tipos")
    ap.add_argument("--min", type=float, default=25.0)
    a = ap.parse_args()
    tipos = json.load(open(a.tipos))
    cache = os.path.join(os.path.dirname(a.tipos), "amazon_raw")
    os.makedirs(cache, exist_ok=True)
    with ThreadPoolExecutor(1) as ex:  # en serie: el guard lee el gasto real antes de cada run
        res = list(ex.map(lambda t: evalua(t, a.min, cache), tipos))
    json.dump(res, open(os.path.join(os.path.dirname(a.tipos), "amazon.json"), "w"), ensure_ascii=False, indent=1)
    for r in sorted(res, key=lambda r: -(r["barato"] or {}).get("precio", 0)):
        b = r["barato"]
        print(f"{'PASA' if r['pasa'] else '----'} {r['k']:26s} rel={r['n_relevantes']:2d}/{r['n_resultados']:2d} "
              f"barato={b and b['precio']} ({b and b['resenas']} res.) top_mes={(r['mas_vendido'] or {}).get('mes')} "
              f"marcas={r['marcas_top'][:3]}")


if __name__ == "__main__":
    main()
