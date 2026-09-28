"""Extrae los anuncios de una búsqueda de AliExpress (datos que la propia página trae en el HTML).

Uso:  python tools/ali_search.py "3d sleep mask" "weighted eye mask" --pages 2 > out.csv
Campos: consulta, id, título, precio de venta, precio tachado, descuento, vendidos, estrellas,
envío (etiquetas de la tarjeta), sale desde (shipFrom), ¿precio de nuevo usuario?, url.
No inventa nada: si la tarjeta no trae un dato, la celda sale vacía.
"""
import argparse
import csv
import json
import re
import sys
import urllib.parse

import requests

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def items_from_html(h):
    i = h.find('"itemList":{"content":[')
    if i < 0:
        return []
    start = h.index("[", i)
    depth, j, in_str, esc = 0, start, False, False
    while j < len(h):
        c = h[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        j += 1
    return json.loads(h[start : j + 1])


def row(q, it):
    p = it.get("prices") or {}
    sale = (p.get("salePrice") or {})
    orig = (p.get("originalPrice") or {})
    tags = []
    for s in it.get("sellingPoints") or []:
        t = (s.get("tagContent") or {}).get("tagText")
        if t:
            tags.append(t)
    trace = urllib.parse.unquote(((it.get("trace") or {}).get("pdpParams") or {}).get("pdp_cdi", ""))
    ship_from = (re.search(r'"shipFrom":"([A-Z]{2})"', trace) or [None, ""])[1]
    npi = ((it.get("trace") or {}).get("pdpParams") or {}).get("pdp_npi", "")
    ev = it.get("evaluation") or {}
    sold = (it.get("trade") or {}).get("tradeDesc", "")
    pid = it.get("productId", "")
    return {
        "consulta": q,
        "id": pid,
        "titulo": ((it.get("title") or {}).get("displayTitle") or "")[:110],
        "precio": sale.get("minPrice", ""),
        "tachado": orig.get("minPrice", ""),
        "dto_%": sale.get("discount", ""),
        "vendidos": sold,
        "estrellas": ev.get("starRating", ""),
        "envio_etiquetas": " | ".join(tags),
        "sale_desde": ship_from,
        "precio_nuevo_usuario": "si" if "new_user" in npi else "",
        "url": f"https://www.aliexpress.us/item/{pid}.html" if pid else "",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("consultas", nargs="+")
    ap.add_argument("--pages", type=int, default=1)
    a = ap.parse_args()
    w = None
    for q in a.consultas:
        slug = re.sub(r"\s+", "-", q.strip().lower())
        for pg in range(1, a.pages + 1):
            url = f"https://www.aliexpress.us/w/wholesale-{slug}.html?page={pg}&shipCountry=US"
            h = requests.get(url, headers=H, timeout=40).text
            if "punish" in h and "itemList" not in h:
                print(f"# BLOQUEO ANTIBOT en {url}", file=sys.stderr)
                continue
            for it in items_from_html(h):
                r = row(q, it)
                if w is None:
                    w = csv.DictWriter(sys.stdout, fieldnames=list(r))
                    w.writeheader()
                w.writerow(r)


if __name__ == "__main__":
    main()
