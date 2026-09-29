"""Vuelca los anuncios de búsquedas en la Biblioteca de Meta (US, activos) en el formato BUSQ del visor.

Uso:
  APIFY_TOKEN=... python tools/meta_dump.py --b H --filtro "basket" "everything basket" "quilted tote" > out.json
Por anuncio: p página, d dominio, u link, dias, id, f formato, t texto, v variantes (collationCount),
r relevante (menciona algún término de --filtro). Nunca inventa: campo que el actor no da, vacío.
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse

from meta_library import ad_text, days_running, pick, relevant, run_actor

PRECIO = 0.0058  # USD por anuncio del actor, observado en corridas anteriores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("consultas", nargs="+")
    ap.add_argument("--b", required=True, help="id del barrido en el visor")
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--tope", type=float, default=0.5)
    ap.add_argument("--filtro", default="")
    a = ap.parse_args()
    token = os.environ.get("APIFY_TOKEN") or sys.exit("Falta APIFY_TOKEN.")
    terms = [t.strip().lower() for t in a.filtro.split(",") if t.strip()]
    out = []
    for q in a.consultas:
        ads = run_actor(token, q, a.max, a.tope, True)
        rows = []
        for ad in ads:
            s = ad.get("snapshot") or {}
            link = pick(ad, "snapshot.linkUrl", "snapshot.cards.0.linkUrl") or ""
            body = (s.get("body") or {}).get("text") or (((s.get("cards") or [{}])[0]).get("body")) or ""
            title = s.get("title") or (((s.get("cards") or [{}])[0]).get("title")) or ""
            rows.append({"p": pick(ad, "pageName", "snapshot.pageName") or "",
                         "d": urllib.parse.urlparse(link).netloc.lower().replace("www.", "") if link else "",
                         "u": link, "dias": days_running(ad) or 0,
                         "id": str(pick(ad, "adArchiveID", "adArchiveId", "ad_archive_id") or ""),
                         "f": s.get("displayFormat") or "", "t": (f"{title} — {body}" if title else body)[:220],
                         "v": ad.get("collationCount") or 1, "r": relevant(ad, terms)})
        out.append({"q": q, "modo": "frase exacta", "b": a.b,
                    "fecha": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
                    "usd": round(len(ads) * PRECIO, 3), "ads": rows})
        print(f"{q}: {len(ads)} anuncios", file=sys.stderr)
    json.dump(out, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
