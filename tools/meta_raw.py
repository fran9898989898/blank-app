"""Guarda el JSON crudo del actor de la Biblioteca de Meta (US, activos, frase exacta) por keyword.

Uso:  APIFY_TOKEN=... python tools/meta_raw.py "hat rack" --max 24 --tope 0.2 --out barridos/<fecha>/raw
Sirve para sacar después lo que haga falta (anunciantes, fechas, textos, miniaturas) sin volver a pagar.
"""
import argparse
import json
import os
import sys

from meta_library import run_actor

ap = argparse.ArgumentParser()
ap.add_argument("q")
ap.add_argument("--max", type=int, default=24)
ap.add_argument("--tope", type=float, default=0.2)
ap.add_argument("--out", required=True)
a = ap.parse_args()
token = os.environ.get("APIFY_TOKEN") or sys.exit("Falta APIFY_TOKEN.")
ads = run_actor(token, a.q, a.max, a.tope, True)
os.makedirs(a.out, exist_ok=True)
with open(os.path.join(a.out, a.q.replace(" ", "_") + ".json"), "w") as f:
    json.dump(ads, f, ensure_ascii=False)
print(f"{a.q}: {len(ads)}", file=sys.stderr)
