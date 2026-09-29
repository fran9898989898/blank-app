"""Lee cualquier página web vía Apify (actor apify~rag-web-browser, ~$0,0025 por página) y la
devuelve en markdown. Sirve cuando la red de la sesión bloquea el dominio (tiendas, Amazon...).
No necesita aprobar permisos en Apify.

Uso:
  APIFY_TOKEN=... python tools/web_read.py https://tienda.com/products/x [> pagina.md]
  Como módulo: from web_read import read; md = read(url)
"""
import os
import sys

import requests


def read(url, browser=True, tope=0.05):
    token = os.environ.get("APIFY_TOKEN") or sys.exit("Falta APIFY_TOKEN.")
    body = {"query": url, "maxResults": 1, "outputFormats": ["markdown"],
            "scrapingTool": "browser-playwright" if browser else "raw-http"}
    r = requests.post("https://api.apify.com/v2/acts/apify~rag-web-browser/run-sync-get-dataset-items",
                      headers={"Authorization": f"Bearer {token}"}, params={"timeout": 180, "maxTotalChargeUsd": tope}, json=body, timeout=200)
    r.raise_for_status()
    items = r.json()
    return (items[0].get("markdown") or "") if items else ""


if __name__ == "__main__":
    for u in sys.argv[1:]:
        print(read(u))
