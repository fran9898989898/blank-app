"""Visor del Barrido R: un solo HTML sin dependencias a partir de anuncios.json (lo genera datos_r.py).

Uso:  python tools/visor_r.py barridos/AAAA-MM-DD-R --gasto 1.72
Semáforo (resumen, no recomendación): VERDE = filtro base + genérico <$12 + persona en pantalla "sí"
en algún anuncio; AMARILLO = entró por escalera o le falta una cosa; GRIS = fuera de filtro.
"""
import argparse
import html
import json
import os

ORDEN = {"VERDE": 0, "AMARILLO": 1, "GRIS": 2}


def semaforo(t, ads):
    if t["escalon"] == "Fuera de filtro":
        return "GRIS"
    persona = any(a["persona"] == "sí" for a in ads)
    if t["escalon"] == "Base" and persona and t["precio_ali"] < 12 and (t["landed_pct"] or 99) <= 25:
        return "VERDE"
    return "AMARILLO"


def money(x):
    return "—" if x is None else f"${x:,.2f}"


def card(t, a, sem):
    e = html.escape
    ads = "".join(
        f"""<li><div class="ad-meta"><b>{e(x['inicio'])}</b> · {x['dias']} días · {e(x['formato'])} · persona: <span class="chip">{e(x['persona'])}</span></div>
        <div class="ad-text">“{e(x['frase'])}”</div>
        <a class="btn" href="{e(x['link'])}" target="_blank" rel="noopener">Ver en la Biblioteca</a></li>"""
        for x in a["top3"]) or "<li>Sin anuncios del líder en la muestra.</li>"
    ang = "".join(f"<li>{e(x)}</li>" for x in a["angulos"])
    nu = " · precio de nuevo usuario (no firme)" if t["ali_nuevo_usuario"] else ""
    tach = f" · tachado ${t['ali_tachado']}" if t.get("ali_tachado") else ""
    checks = "".join(
        f'<label><input type="checkbox" data-k="{e(t["k"])}-{i}"> {e(c)}</label>'
        for i, c in enumerate(["lo entiendo en 5 s sin texto", "sale una persona usándolo",
                               "no hay una marca conocida que ya venda esto en Walmart/Target",
                               "me lo compraría mi madre a $35"]))
    return f"""<article class="card {sem.lower()}" data-sem="{sem}" data-cat="{e(t['categoria'])}">
  <img class="foto" src="{e(t['ali_foto'])}" alt="Genérico de AliExpress" loading="lazy">
  <div class="body">
    <h2>{e(t['tipo'])}</h2>
    <div class="tags"><span class="sem">{sem}</span><span class="tag">{e(t['escalon'])}</span><span class="tag">{e(t['categoria'])}</span></div>
    <p class="falla">{e(t['falla'])}</p>
    <div class="nums">
      <div><span>PRECIO RIVALES</span><b>{money(t['precio_rivales'])}</b><small>{e(t['precios_leidos'])}</small></div>
      <div><span>PRECIO ALI</span><b>{money(t['precio_ali'])}</b><small>landed {t['landed_pct'] if t['landed_pct'] is not None else '—'} %</small></div>
      <div><span>MARGEN BRUTO EST.</span><b>{money(t['margen_bruto'])}</b><small>rivales − Ali − $8 envío</small></div>
    </div>
    <p class="meta"><b>{t['anunciantes_21d']}</b> anunciantes ≥21 días · anuncio más antiguo del tipo: <b>{t['dias_mas_antiguo']} días</b><br>
    Líder: <a href="https://{e(t['lider'])}" target="_blank" rel="noopener">{e(t['lider'])}</a> · {str(t['lider_stt_activos']) + ' anuncios activos (STT)' if t['lider_stt_activos'] is not None else 'anuncios activos en STT: no consultado'}</p>
    <h3>3 anuncios más antiguos del líder (muestra)</h3><ul class="ads">{ads}</ul>
    <h3>3 ángulos</h3><ol class="ang">{ang}</ol>
    <p class="ali"><a href="{e(t['ali_url'])}" target="_blank" rel="noopener">Genérico en AliExpress</a> — {e(t['ali_titulo'][:80])} · {e(t['ali_vendidos'] or 'sin ventas')}{tach}{nu}</p>
    <fieldset class="check"><legend>CHECK HUMANO</legend>{checks}</fieldset>
  </div>
</article>"""


CSS = """
:root{--bg:#f6f5f2;--card:#fff;--ink:#1d1d1b;--mut:#6b6b66;--line:#e3e1dc;--acc:#2f5bd3;
--verde:#1f8a4c;--amar:#b7791f;--gris:#7a7a74}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#141413;--card:#1e1e1c;--ink:#ecebe6;--mut:#a3a29c;--line:#34332f;--acc:#8fb0ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}
header{padding:20px 16px 8px;max-width:1100px;margin:auto}h1{margin:0 0 6px;font-size:24px}
.sub{color:var(--mut);font-size:14px}.bar{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
select{font:inherit;padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
main{max-width:1100px;margin:auto;padding:0 16px 40px;display:grid;gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--gris);border-radius:14px;display:grid;grid-template-columns:260px 1fr;overflow:hidden}
.card.verde{border-left-color:var(--verde)}.card.amarillo{border-left-color:var(--amar)}
.foto{width:100%;height:100%;min-height:220px;object-fit:cover;background:#ddd}
.body{padding:16px 18px}h2{margin:0 0 8px;font-size:22px}h3{font-size:14px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:16px 0 6px}
.tags{display:flex;flex-wrap:wrap;gap:6px}.tag,.sem,.chip{font-size:12px;padding:3px 8px;border-radius:999px;border:1px solid var(--line)}
.verde .sem{background:var(--verde);color:#fff}.amarillo .sem{background:var(--amar);color:#fff}.gris .sem{background:var(--gris);color:#fff}
.falla{color:var(--mut);font-size:14px;margin:8px 0}
.nums{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}
.nums div{border:1px solid var(--line);border-radius:10px;padding:8px 10px}.nums span{display:block;font-size:11px;color:var(--mut);letter-spacing:.04em}
.nums b{font-size:26px}.nums small{display:block;color:var(--mut);font-size:12px}
.meta{font-size:14px}a{color:var(--acc)}.ads{list-style:none;padding:0;margin:0;display:grid;gap:8px}
.ads li{border:1px solid var(--line);border-radius:10px;padding:8px 10px}.ad-meta{font-size:13px;color:var(--mut)}.ad-text{margin:4px 0 6px}
.btn{display:inline-block;padding:6px 12px;border-radius:8px;background:var(--acc);color:#fff;text-decoration:none;font-size:14px}
.ang{margin:0;padding-left:20px}.ali{font-size:14px}
.check{border:2px dashed var(--line);border-radius:10px;margin-top:12px;display:grid;gap:6px}.check legend{font-weight:700;font-size:13px}
@media (max-width:720px){.card{grid-template-columns:1fr}.foto{height:220px}.nums b{font-size:20px}}
"""

JS = """
const s=document.getElementById('fs'),c=document.getElementById('fc');
function f(){document.querySelectorAll('.card').forEach(k=>{k.style.display=(!s.value||k.dataset.sem==s.value)&&(!c.value||k.dataset.cat==c.value)?'':'none'})}
s.onchange=f;c.onchange=f;
document.querySelectorAll('.check input').forEach(i=>{try{i.checked=localStorage.getItem(i.dataset.k)==='1'}catch(e){}
 i.onchange=()=>{try{localStorage.setItem(i.dataset.k,i.checked?'1':'0')}catch(e){}}});
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--gasto", type=float, required=True, help="gasto real de Apify leído del panel")
    a = ap.parse_args()
    d = json.load(open(os.path.join(a.carpeta, "anuncios.json")))
    items = []
    for t in d["tipos"]:
        ad = d["anuncios"][t["k"]]
        items.append((semaforo(t, ad["top3"]), t, ad))
    items.sort(key=lambda x: (ORDEN[x[0]], -x[1]["anunciantes_21d"]))
    cats = sorted({t["categoria"] for _, t, _ in items})
    cuenta = {k: sum(1 for s, _, _ in items if s == k) for k in ORDEN}
    fecha = os.path.basename(a.carpeta.rstrip("/")).removesuffix("-R")
    out = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Barrido R {fecha}</title><style>{CSS}</style></head><body>
<header><h1>Barrido R · {fecha}</h1>
<div class="sub">US · Biblioteca de Meta (Apify) + SearchTheTrend + AliExpress · {len(items)} tipos · VERDE {cuenta['VERDE']} · AMARILLO {cuenta['AMARILLO']} · GRIS {cuenta['GRIS']} · gasto Apify del barrido: <b>${a.gasto:.2f}</b> (panel)</div>
<div class="sub">Sin recomendación: eliges tú mirando las tarjetas. "Persona: verificar" = ábrelo en la Biblioteca. Precios Ali = precio de nuevo usuario salvo que se diga otra cosa.</div>
<div class="bar"><select id="fs"><option value="">Todos los semáforos</option><option>VERDE</option><option>AMARILLO</option><option>GRIS</option></select>
<select id="fc"><option value="">Todas las categorías</option>{''.join(f'<option>{html.escape(c)}</option>' for c in cats)}</select></div></header>
<main>{''.join(card(t, ad, s) for s, t, ad in items)}</main><script>{JS}</script></body></html>"""
    open(os.path.join(a.carpeta, "visor.html"), "w").write(out)
    print(os.path.join(a.carpeta, "visor.html"), cuenta)


if __name__ == "__main__":
    main()
