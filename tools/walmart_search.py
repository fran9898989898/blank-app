"""Ancla de Walmart US vía Apify (actor axesso_data~walmart-search-scraper, ~$0,005 por producto en plan
gratuito). walmart.com bloquea la lectura directa y el navegador de Apify («Robot or human?»).

Uso:  APIFY_TOKEN=... python tools/walmart_search.py "quilted car basket" "peppermint mouse repellent" --tope 0.25 > out.csv
Salida: consulta, posicion, producto, precio, estrellas, resenas, vendedor, patrocinado, url
Nunca inventa: si el actor no devuelve un campo, sale vacío.
"""
import argparse
import csv
import os
import sys


ACTOR = "axesso_data~walmart-search-scraper"


def pick(d, *keys):
    for k in keys:
        cur = d
        for part in k.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur not in (None, ""):
            return cur
    return ""


def search(token, q, tope):
    from apify_guard import run  # caché, corte de sesión y sin reintentos
    return run(ACTOR, {"input": [{"keyword": q, "startPage": 1, "endPage": 1, "sortBy": "best_match"}]},
               tope_usd=tope, timeout=240)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("consultas", nargs="+")
    ap.add_argument("--tope", type=float, default=0.25)
    ap.add_argument("--raw", help="guarda la respuesta cruda en este fichero JSON")
    a = ap.parse_args()
    token = os.environ.get("APIFY_TOKEN") or sys.exit("Falta APIFY_TOKEN.")
    w = csv.writer(sys.stdout)
    w.writerow(["consulta", "posicion", "producto", "precio", "estrellas", "resenas", "vendedor", "patrocinado", "url"])
    raw = {}
    for q in a.consultas:
        items = search(token, q, a.tope)
        raw[q] = items
        rows = []
        for it in items:
            prods = it.get("searchProductDetails") or it.get("products") or [it]
            rows.extend(prods if isinstance(prods, list) else [prods])
        for i, p in enumerate(rows, 1):
            url = pick(p, "productUrl", "url", "canonicalUrl")
            if url and url.startswith("/"):
                url = "https://www.walmart.com" + url
            w.writerow([q, i, pick(p, "productDescription", "name", "title"),
                        pick(p, "price", "currentPrice", "priceInfo.currentPrice.price"),
                        pick(p, "rating.averageRating", "averageRating", "productRating"),
                        pick(p, "rating.numberOfReviews", "numberOfReviews", "countReview"),
                        pick(p, "sellerName", "seller", "soldBy"),
                        "sí" if pick(p, "sponsored", "isSponsored") is True else "", url])
        print(f"{q}: {len(rows)} productos", file=sys.stderr)
    if a.raw:
        import json
        json.dump(raw, open(a.raw, "w"), ensure_ascii=False)


if __name__ == "__main__":
    main()
