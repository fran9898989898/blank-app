#!/usr/bin/env bash
# Pinta las fichas dentro del HTML (para visores que no ejecutan JavaScript, como la vista previa del chat).
# Uso: tools/prerender.sh barridos/radar.html [otro.html ...]   → reescribe cada fichero ya renderizado.
set -euo pipefail
CH=${CHROME:-$(ls -d /opt/pw-browsers/chromium*/chrome-linux*/chrome 2>/dev/null | head -1)}
[ -x "$CH" ] || { echo "No encuentro Chromium (exporta CHROME=/ruta/a/chrome)"; exit 1; }
for f in "$@"; do
  abs=$(realpath "$f")
  tmp=$(mktemp)
  "$CH" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=4000 --dump-dom "file://$abs" 2>/dev/null > "$tmp"
  n=$(grep -o "<article" "$tmp" | wc -l)
  [ "$n" -gt 0 ] || { echo "$f: 0 fichas renderizadas, no lo toco"; rm -f "$tmp"; exit 1; }
  printf '<!doctype html>\n' | cat - "$tmp" > "$abs"; rm -f "$tmp"
  echo "$f: $n fichas escritas en el HTML"
done
