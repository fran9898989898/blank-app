"""Genera visor.html (un fichero, sin dependencias) a partir de datos.py. Uso: python visor.py"""
import json
import pathlib

from datos import NOPASAN, PASAN, RADAR

AQUI = pathlib.Path(__file__).parent
STYLE = (AQUI / "_style.css").read_text(encoding="utf-8").replace(
    "</style>",
    ".ad video,.ad img{width:100%;max-height:360px;border-radius:6px;background:#000;object-fit:contain}\n"
    ".resumen{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:0 0 14px}\n"
    ".resumen li{margin:4px 0}\n</style>")

HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Visor barrido A 29-sep</title>
__STYLE__
</head>
<body>
<div class="wrap">
<h1>Barrido A · Escala general · 29 sep 2026</h1>
<p class="sub">Fuente: SearchTheTrend (US, ≥30 días, visto desde el 25-sep) + Biblioteca de Meta vía Apify (30 anuncios por consulta, frase exacta) + precios de Shopify vía Apify + AliExpress US. Agrupado por TIPO. <b>Sin recomendación: elijo yo mirando los anuncios.</b></p>
<div class="warnbox"><b>Resultado: 0 tipos con escala + gate PRIORIDAD/POSIBLE.</b> Los 4 que pasan escala caen en el gate (≥6 dropshippers del genérico en la Biblioteca). Según la skill, cero es un resultado válido. Toca el siguiente barrido del orden o revisar el gate (ver pestaña «Siguiente paso»).<br>
<b>No verificado:</b> ancla de Amazon (el lector no devolvió resultados tras 3 intentos; mírala a mano) · landed real (lo da tu agente) · coste de envío de Ali.<br>
<b>Gasto Apify real</b> (API de Apify, ejecuciones de este barrido): ≈ $2,03 de $3 de tope.</div>

<div class="tabs" role="tablist">
  <button class="tab" role="tab" aria-selected="true" data-tab="pasan">Pasan escala (__NP__)</button>
  <button class="tab" role="tab" aria-selected="false" data-tab="radar">Vivos que no pasan, con creativo (__NR__)</button>
  <button class="tab" role="tab" aria-selected="false" data-tab="nopasan">Descartes rápidos (__NN__)</button>
  <button class="tab" role="tab" aria-selected="false" data-tab="sig">Siguiente paso</button>
</div>

<section id="pasan">
<div class="bar">
  <label>Orden <select id="fOrd"><option value="anun">Nº anunciantes</option><option value="crec">Crecimiento líder</option><option value="dias">Días del líder</option></select></label>
</div>
<div id="cards"></div>
</section>

<section id="radar" class="hidden"><div id="radarcards"></div></section>

<section id="nopasan" class="hidden">
<div class="tblwrap"><table><thead><tr><th>Tipo</th><th>Anunciantes</th><th>Motivo</th></tr></thead><tbody id="nprows"></tbody></table></div>
</section>

<section id="sig" class="hidden">
<div class="resumen">
<h3>Lectura por la skill</h3>
<ul>
<li><b>Barrido con 0.</b> Ya se hicieron A (27-sep), D (27-sep), E y F (28-sep), B momentum (28-sep) y cesta/bolsitas (29-sep). Con este A, la regla de parada aplica: <b>no fuerces otro A</b>.</li>
<li><b>Revisión (c) de la regla de parada:</b> el gate se come todo. De los que pasan escala, el menos saturado tiene 6 operadores. La skill dice que POSIBLE (3–5) también se testea; aquí no hay ninguno.</li>
<li><b>Siguiente del orden:</b> G (reseñas 1★ del líder) sobre una categoría que te guste de este visor, p. ej. conducto de secadora o copa navideña: buscar la queja que el genérico actual no resuelve.</li>
<li><b>Ojo con shopmoderny.com</b> (percha, bandeja, cajas, botella): escala con falsa escasez («we are closing, 60% OFF») desde 2024. El volumen de anuncios no prueba ventas.</li>
<li>Añade a EXCLUIDOS: conducto de secadora, rivet nut, copa 3D navideña, mopa flexible, estante de fregadero, cajas apilables, tacos de pared, key decoder.</li>
</ul>
</div>
</section>

<footer>Datos crudos en esta carpeta: meta_ops_*.csv (Biblioteca), precios.csv (Shopify), ali.csv (AliExpress). Los creativos se cargan del CDN de SearchTheTrend; si uno no carga, ábrelo en la Biblioteca.</footer>
</div>

<script>
const PASAN = __PASAN__;
const RADAR = __RADAR__;
const NOPASAN = __NOPASAN__;
const LIB = id => `https://www.facebook.com/ads/library/?id=${id}`;
const AMZ = q => `https://www.amazon.com/s?k=${encodeURIComponent(q)}`;
function esc(t){return String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function spark(s){if(!s||!s.length)return '<div class="v">Sin serie en STT</div>';const m=Math.max(...s);return `<div class="spark" title="${s.join(' · ')}">${s.map(x=>`<i style="height:${Math.max(4,x/m*100)}%"></i>`).join('')}</div>`}
function media(a){return /\\.mp4/.test(a.cr)?`<video controls preload="metadata" playsinline src="${a.cr}"></video>`:`<img loading="lazy" src="${a.cr}" alt="creativo">`}
function adbox(a,src){return `<div class="ad">${media(a)}<div class="meta"><b>${esc(src||a.src||'')}</b><br>Inicio ${a.d} · ${a.dias} d · ${a.fmt} · ${a.var} variación${a.var>1?'es':''}</div><p>${esc(a.txt)}</p><div class="btns"><a class="btn" target="_blank" rel="noopener" href="${LIB(a.id)}">Biblioteca de Meta</a><a class="btn" target="_blank" rel="noopener" href="${a.cr}">Abrir creativo</a></div></div>`}
function card(t){
 const g=t.gate==='PRIORIDAD'?'ok':t.gate==='POSIBLE'?'warn':'bad';
 return `<article class="card">
 <div class="head"><h2>${esc(t.tipo)}</h2>
  <div class="chips"><span class="chip ${t.escala[0]}">${esc(t.escala[1])}</span><span class="chip ${g}">Gate ${t.gate} · ${t.gateN} operadores</span><span class="chip ${t.mercado[0]}">${esc(t.mercado[1])}</span><span class="chip">${esc(t.sub)}</span></div></div>
 <div class="grid">
  <div><div class="k">Anunciantes ≥30 d</div><div class="v"><b>${t.anun}</b></div></div>
  <div><div class="k">Líder</div><div class="v">${t.lider.dom}<br>${t.lider.dias} d · ${t.lider.ads} ads · ${t.lider.g30>0?'+':''}${t.lider.g30}% 30d</div></div>
  <div><div class="k">Serie semanal ads activos (líder)</div>${spark(t.lider.serie)}</div>
  <div><div class="k">PVP rivales</div><div class="v">${esc(t.pvp)}</div></div>
  <div><div class="k">Genérico Ali / landed</div><div class="v">${esc(t.ali)}<br>${t.alilink?`<a class="btn" target="_blank" rel="noopener" href="${t.alilink}">Ficha Ali</a> `:''}<a class="btn" target="_blank" rel="noopener" href="${AMZ(t.en)}">Ancla Amazon (a mano)</a></div></div>
  <div><div class="k">Marca de referencia</div><div class="v">${esc(t.marca)}</div></div>
  <div><div class="k">Regalo Q4</div><div class="v">${esc(t.q4)}</div></div>
 </div>
 <div class="sec"><h3>Anunciantes del tipo</h3><div class="v">${esc(t.rivales)}</div></div>
 <div class="sec"><h3>Hueco de ejecución observado</h3><ul>${t.hueco.map(h=>`<li>${esc(h)}</li>`).join('')}</ul></div>
 <div class="sec"><h3>Riesgos</h3><ul>${t.riesgos.map(h=>`<li>${esc(h)}</li>`).join('')}</ul></div>
 <div class="sec"><h3>Anuncios más antiguos (activos)</h3><div class="ads">${t.ads.map(a=>adbox(a)).join('')}</div></div>
 </article>`}
function rcard(r){return `<article class="card"><div class="head"><h2>${esc(r.tipo)}</h2><div class="chips"><span class="chip bad">No pasa</span><span class="chip">${r.dom} · ${r.dias} d · ${r.nads} ads</span><span class="chip">PVP ${esc(r.pvp)}</span></div></div>
 <div class="sec"><h3>Motivo</h3><div class="v">${esc(r.motivo)}</div></div>
 <div class="sec"><h3>Creativos activos</h3><div class="ads">${r.ads.map(a=>adbox(a,r.dom)).join('')}</div></div></article>`}
function render(){
 const o=document.getElementById('fOrd').value;
 const key={anun:t=>t.anun,crec:t=>t.lider.g30,dias:t=>t.lider.dias}[o];
 document.getElementById('cards').innerHTML=[...PASAN].sort((a,b)=>key(b)-key(a)).map(card).join('');
}
document.getElementById('fOrd').addEventListener('change',render);
render();
document.getElementById('radarcards').innerHTML=RADAR.map(rcard).join('');
document.getElementById('nprows').innerHTML=NOPASAN.map(r=>`<tr>${r.map(c=>`<td>${esc(c)}</td>`).join('')}</tr>`).join('');
document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{
 document.querySelectorAll('.tab').forEach(x=>x.setAttribute('aria-selected',x===b));
 ['pasan','radar','nopasan','sig'].forEach(id=>document.getElementById(id).classList.toggle('hidden',b.dataset.tab!==id));
}));
</script>
</body>
</html>
"""

out = (HTML.replace("__STYLE__", STYLE)
       .replace("__NP__", str(len(PASAN))).replace("__NR__", str(len(RADAR))).replace("__NN__", str(len(NOPASAN)))
       .replace("__PASAN__", json.dumps(PASAN, ensure_ascii=False))
       .replace("__RADAR__", json.dumps(RADAR, ensure_ascii=False))
       .replace("__NOPASAN__", json.dumps(NOPASAN, ensure_ascii=False)))
(AQUI / "visor.html").write_text(out, encoding="utf-8")
print("visor.html", len(out), "bytes")
