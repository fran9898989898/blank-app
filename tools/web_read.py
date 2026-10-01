"""Lee cualquier página web vía Apify (actor apify~rag-web-browser, ~$0,009–0,016 por página medido el 1-oct) y la
devuelve en markdown. Sirve cuando la red de la sesión bloquea el dominio (tiendas, Amazon...).
No necesita aprobar permisos en Apify.

Uso:
  APIFY_TOKEN=... python tools/web_read.py https://tienda.com/products/x [> pagina.md]
  Como módulo: from web_read import read; md = read(url)
"""
import os
import sys


def read(url, browser=True, tope=0.05):
    """Pasa por apify_guard (caché 7 días, corte de sesión, sin reintentos). Coste real medido: ~$0,009–0,016 por página."""
    from apify_guard import run
    body = {"query": url, "maxResults": 1, "outputFormats": ["markdown"],
            "scrapingTool": "browser-playwright" if browser else "raw-http"}
    items = run("apify~rag-web-browser", body, tope_usd=tope, timeout=180)
    return (items[0].get("markdown") or "") if items else ""


if __name__ == "__main__":
    for u in sys.argv[1:]:
        print(read(u))
