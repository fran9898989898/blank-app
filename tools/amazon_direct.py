"""Ancla de Amazon US leyendo la búsqueda directamente (sin Apify). Si Amazon devuelve captcha, avisa.

Uso:  python tools/amazon_direct.py "quilted basket" "mouse repellent pouches" > out.csv
Salida: consulta, posicion, patrocinado, producto, precio, estrellas, resenas, comprados_mes, url
"""
import csv
import html
import re
import sys
import urllib.parse

import requests

H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36",
     "Accept-Language": "en-US,en;q=0.9", "Accept": "text/html,application/xhtml+xml"}


def search(q):
    r = requests.get("https://www.amazon.com/s?k=" + urllib.parse.quote_plus(q), headers=H, timeout=30)
    if "captcha" in r.text.lower()[:20000] and "s-search-result" not in r.text:
        sys.exit(f"Amazon devolvió captcha para «{q}»")
    blocks = re.split(r'data-component-type="s-search-result"', r.text)[1:]
    out = []
    for b in blocks:
        b = b[:60000]
        asin = re.search(r'data-asin="([A-Z0-9]{10})"', b) or re.search(r"/dp/([A-Z0-9]{10})", b)
        title = re.search(r"<h2[^>]*aria-label=\"([^\"]+)\"", b) or re.search(r"<h2[^>]*>.*?<span[^>]*>([^<]+)</span>", b, re.S)
        price = re.search(r'class="a-offscreen">\$([\d,]+\.\d\d)<', b)
        stars = re.search(r"(\d\.\d) out of 5 stars", b)
        revs = re.search(r'aria-label="([\d,.]+K?) ratings?"', b) or re.search(r's-underline-text">\(?([\d,.]+K?)\)?<', b)
        bought = re.search(r"([\d,.]+K?\+) bought in past month", b)
        sp = "Sponsored" in b[:8000]
        if not price:
            continue
        out.append([html.unescape(title.group(1)).strip()[:140] if title else "", price.group(1),
                    stars.group(1) if stars else "", revs.group(1) if revs else "", bought.group(1) if bought else "",
                    "sí" if sp else "", f"https://www.amazon.com/dp/{asin.group(1)}" if asin else ""])
    return out


if __name__ == "__main__":
    w = csv.writer(sys.stdout)
    w.writerow(["consulta", "posicion", "producto", "precio", "estrellas", "resenas", "comprados_mes", "patrocinado", "url"])
    for q in sys.argv[1:]:
        for i, row in enumerate(search(q), 1):
            w.writerow([q, i] + row)
