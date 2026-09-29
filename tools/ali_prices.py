"""Extrae precio, precio tachado, vendidos y envío a US de fichas de AliExpress.

Uso:  python tools/ali_prices.py URL [URL ...]  > precios.csv
Requiere: pip install playwright  (y un Chromium; en Claude Code web ya viene en /opt/pw-browsers)
Necesita acceso de red a aliexpress.com / aliexpress.us (en la sesión cloud hay que
añadir esos dominios en Network access del entorno).

Lee el TEXTO renderizado de la página (no clases CSS, que AliExpress cambia a menudo)
y aplica expresiones regulares. Si un campo no aparece, sale vacío: nunca se inventa.
"""
import csv
import os
import re
import sys

from playwright.sync_api import sync_playwright

PRICE = re.compile(r"(?:US\s*\$|\$)\s?(\d{1,3}(?:[.,]\d{2}))")
SOLD = re.compile(r"([\d,.]+\+?)\s*(?:sold|vendidos)", re.I)
SHIP = re.compile(r"(Free shipping|Shipping:\s*(?:US\s*)?\$\s?[\d.,]+|Env[ií]o gratis)", re.I)
DELIVERY = re.compile(r"(Delivery:?\s*[A-Z][a-z]{2}\s*\d{1,2}(?:\s*-\s*\d{1,2})?)")


def extract(page, url):
    page.goto(url.split("?")[0] + "?gatewayAdapt=glo2usa", timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    text = page.inner_text("body")
    prices = PRICE.findall(text)
    row = {
        "url": url,
        "titulo": (page.title() or "")[:120],
        "precio": prices[0] if prices else "",
        "precio_tachado": prices[1] if len(prices) > 1 else "",
        "vendidos": (SOLD.search(text) or [None, ""])[1] if SOLD.search(text) else "",
        "envio_us": SHIP.search(text).group(1) if SHIP.search(text) else "",
        "entrega": DELIVERY.search(text).group(1) if DELIVERY.search(text) else "",
    }
    if "captcha" in text.lower() or "slide to verify" in text.lower():
        row["titulo"] = "BLOQUEADO POR CAPTCHA — repetir a mano"
    return row


def main(urls):
    w = csv.DictWriter(sys.stdout, fieldnames=["url", "titulo", "precio", "precio_tachado", "vendidos", "envio_us", "entrega"])
    w.writeheader()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        ctx = b.new_context(locale="en-US", extra_http_headers={"Accept-Language": "en-US"})
        page = ctx.new_page()
        for u in urls:
            try:
                w.writerow(extract(page, u))
            except Exception as e:  # una ficha rota no para las demás
                w.writerow({"url": u, "titulo": f"ERROR: {e.__class__.__name__}"})
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:])
