"""Cuenta operadores en la Biblioteca de Anuncios de Meta (US) vía un actor de Apify.

Uso:
  APIFY_TOKEN=... python tools/meta_library.py "sleep mask" "knee brace" --max 30 --tope 3 \
      --filtro "sleep mask,eye mask,sleeping mask"
Salida (CSV por stdout): consulta, anunciantes distintos, dominios distintos, operadores >=30 días,
  anunciante con más anuncios, días del anuncio más antiguo, y una línea por anunciante.

- Actor configurable con APIFY_ACTOR (por defecto el scraper oficial de Apify de la Biblioteca).
- --tope: gasto máximo en USD por ejecución (se pasa a Apify como maxTotalChargeUsd) → el límite
  lo aplica Apify, no este script. Aun así, fija también un límite mensual en tu cuenta.
- Por defecto busca la FRASE EXACTA: keyword_unordered ("--amplia") devuelve anuncios con las palabras
  sueltas (p. ej. "sleep" + "mask" → CPAP, cosmética) y el conteo sale inflado.
- --filtro descarta anuncios que no mencionan el producto; revisa igualmente la lista a ojo.
- Operador = dominio de destino, no página de Facebook.
- Nunca inventa: si el actor no devuelve un campo, sale vacío.
"""
import argparse
import csv
import datetime as dt
import os
import sys
import urllib.parse
from collections import defaultdict

import requests

API = "https://api.apify.com/v2"
ACTOR = os.environ.get("APIFY_ACTOR", "apify~facebook-ads-scraper")


def library_url(q, exacta):
    params = {
        "active_status": "active",
        "ad_type": "all",
        "country": "US",
        "q": q,
        "search_type": "keyword_exact_phrase" if exacta else "keyword_unordered",
        "media_type": "all",
    }
    return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode(params)


def run_actor(token, q, max_items, tope, exacta):
    """Pasa por apify_guard: ≤30 anuncios, ≤$0,50 por run, corte de sesión a $2, caché 7 días, sin reintentos.
    `token` se mantiene por compatibilidad; el guard lo lee del entorno."""
    from apify_guard import run
    body = {"startUrls": [{"url": library_url(q, exacta)}], "resultsLimit": max_items, "activeStatus": "active"}
    return run(ACTOR, body, tope_usd=tope)


def pick(d, *keys):
    for k in keys:
        cur = d
        for part in k.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur not in (None, ""):
            return cur
    return ""


def ad_text(ad):
    s = ad.get("snapshot") or {}
    parts = [s.get("title"), (s.get("body") or {}).get("text"), s.get("linkUrl"), s.get("caption"),
             s.get("linkDescription")]
    for c in s.get("cards") or []:
        parts += [c.get("title"), c.get("body"), c.get("linkUrl")]
    return " ".join(str(x) for x in parts if x).lower().replace("-", " ")


def relevant(ad, terms):
    """True si el anuncio menciona alguno de los términos (texto, título o URL). Sin términos → True."""
    if not terms:
        return True
    t = ad_text(ad)
    return any(term in t for term in terms)


def days_running(ad):
    start = pick(ad, "startDate", "start_date", "startDateFormatted", "ad_delivery_start_time")
    if not start:
        return None
    try:
        if isinstance(start, (int, float)):
            d0 = dt.datetime.utcfromtimestamp(start)
        else:
            d0 = dt.datetime.fromisoformat(str(start)[:10])
        return (dt.datetime.utcnow() - d0).days
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("consultas", nargs="+")
    ap.add_argument("--max", type=int, default=30, help="anuncios por consulta (≈30 según la skill)")
    ap.add_argument("--tope", type=float, default=3.0, help="USD máx. por consulta")
    ap.add_argument("--amplia", action="store_true",
                    help="keyword_unordered (cualquier orden). Por defecto frase exacta: la amplia mete ruido")
    ap.add_argument("--filtro", default="",
                    help="términos separados por coma; solo cuentan anuncios que mencionen alguno (texto/URL)")
    a = ap.parse_args()
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Falta APIFY_TOKEN en las variables de entorno.")
    w = csv.writer(sys.stdout)
    terms = [t.strip().lower() for t in a.filtro.split(",") if t.strip()]
    w.writerow(["consulta", "anunciante", "dominio", "anuncios", "dias_max", "resumen"])
    for q in a.consultas:
        ads = run_actor(token, q, a.max, a.tope, not a.amplia)
        rel = [ad for ad in ads if relevant(ad, terms)]
        # Operador = dominio de destino (varias páginas de FB pueden ser la misma tienda).
        per = defaultdict(lambda: {"n": 0, "dias": 0, "pages": set()})
        for ad in rel:
            name = pick(ad, "pageName", "snapshot.pageName", "page_name") or "?"
            link = pick(ad, "snapshot.linkUrl", "snapshot.cards.0.linkUrl", "snapshot.link_url", "linkUrl")
            dom = urllib.parse.urlparse(link).netloc.lower().replace("www.", "") if link else ""
            p = per[dom or f"(sin dominio) {name}"]
            p["n"] += 1
            p["dias"] = max(p["dias"], days_running(ad) or 0)
            p["pages"].add(name)
        ops30 = [k for k, v in per.items() if v["dias"] >= 30]
        top = max(per.items(), key=lambda kv: kv[1]["n"]) if per else ("", {"n": 0})
        oldest = max((v["dias"] for v in per.values()), default=0)
        w.writerow([q, "", "", len(ads), oldest,
                    f"relevantes={len(rel)}/{len(ads)} operadores={len(per)} operadores_30d={len(ops30)} "
                    f"lider={top[0]}({top[1]['n']})"])
        for dom, v in sorted(per.items(), key=lambda kv: -kv[1]["n"]):
            w.writerow([q, " / ".join(sorted(v["pages"])), dom, v["n"], v["dias"], ""])


if __name__ == "__main__":
    main()
