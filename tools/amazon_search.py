"""Ancla de precio en Amazon US: primeras posiciones de una búsqueda con precio, estrellas,
reseñas y "bought in past month". Lee Amazon vía Apify (tools/web_read.py, ~$0,0025 por búsqueda).

Uso:
  APIFY_TOKEN=... python tools/amazon_search.py "3d contoured sleep mask" "weighted eye mask"
Salida (CSV por stdout): consulta, posicion, producto, precio, estrellas, resenas, comprados_mes, url
"""
import csv
import re
import sys
import urllib.parse

from web_read import read


def parse(md):
    out = []
    for blk in re.split(r"\n## ", md)[1:]:
        title = blk.split("\n", 1)[0].strip()
        m = re.search(r"\]\((https://www\.amazon\.com/[^)\s]*?/dp/[A-Z0-9]{10})", blk)
        price = re.search(r"Price, product page\[\$(\d+(?:\.\d\d)?)", blk)
        if not price:
            continue
        stars = re.search(r"(\d\.\d) out of 5 stars", blk)
        revs = re.search(r"\[\(([\d.,]+K?)\)\]", blk)
        bought = re.search(r"([\d.,]+K?\+) bought in past month", blk)
        out.append([title[:140], price.group(1), stars.group(1) if stars else "", revs.group(1) if revs else "",
                    bought.group(1) if bought else "", m.group(1) if m else ""])
    return out


def main():
    w = csv.writer(sys.stdout)
    w.writerow(["consulta", "posicion", "producto", "precio", "estrellas", "resenas", "comprados_mes", "url"])
    for q in sys.argv[1:]:
        rows = []
        for _ in range(3):  # Amazon devuelve a veces una página de error antibots: reintentar
            rows = parse(read("https://www.amazon.com/s?k=" + urllib.parse.quote_plus(q) + "&ref=nb_sb_noss"))
            if rows:
                break
        if not rows:
            print(f"# {q}: Amazon no devolvió resultados tras 3 intentos", file=sys.stderr)
        for i, row in enumerate(rows, 1):
            w.writerow([q, i] + row)


if __name__ == "__main__":
    main()
