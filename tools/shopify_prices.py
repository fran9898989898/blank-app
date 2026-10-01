"""Precios reales de tiendas Shopify vía Apify (actor autofacts~shopify, ~$0,002 por producto).

Sirve cuando la red local/nube bloquea las tiendas: Apify las lee desde sus servidores.
No necesita aprobar permisos en Apify (actor de permisos limitados).

Uso:
  APIFY_TOKEN=... python tools/shopify_prices.py https://tienda.com/products/x https://otra.com/products/y
Salida (CSV por stdout): url, producto, variante, precio, precio_tachado, stock
"""
import csv
import os
import sys


ACTOR = "autofacts~shopify"


def main():
    urls = sys.argv[1:]
    if not urls:
        sys.exit(__doc__)
    from apify_guard import run
    body = {"startUrls": [{"url": u} for u in urls], "maxRequestsPerCrawl": 2 * len(urls),
            "maxResults": min(2 * len(urls), 30), "proxy": {"useApifyProxy": True}}
    items = run(ACTOR, body, tope_usd=0.1, timeout=240)
    w = csv.writer(sys.stdout)
    w.writerow(["url", "producto", "variante", "precio", "precio_tachado", "stock"])
    for p in items:
        for v in p.get("variants") or []:
            pr = v.get("price") or {}
            cents = lambda x: f"{x / 100:.2f}" if x else ""
            w.writerow([(p.get("source") or {}).get("canonicalUrl", ""), p.get("title", ""), v.get("title", ""),
                        cents(pr.get("current")), cents(pr.get("previous")), pr.get("stockStatus", "")])


if __name__ == "__main__":
    main()
