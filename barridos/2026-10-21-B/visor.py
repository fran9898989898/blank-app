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
<title>Visor barrido B 21-oct</title>
__STYLE__
</head>
<body>
<div class="wrap">
<h1>Barrido B · Momentum Q4 · 21 oct 2026</h1>
<p class="sub">Fuente: SearchTheTrend (US, ≥30 días, ≥10 anuncios, visto desde el 17-oct, ordenado por crecimiento de anuncios en 30 días) + Biblioteca de Meta vía Apify (30 anuncios por consulta, frase exacta) + precios Shopify vía Apify + AliExpress US + Amazon US. Agrupado por TIPO. <b>Sin recomendación: elijo yo mirando los anuncios.</b></p>
<div class="warnbox"><b>Resultado: 1 dudoso (planificador de fin de vida, gate POSIBLE no firme), 3 KILL por gate, 2 vivos que no pasan.</b> Casi todo lo que crece este mes lo copian las mismas tiendas-catálogo (mindsparkl, perpetualing, pinkdiyprint, bisnftwrem, mygrandhearth): enjambre, no demanda.<br>
<b>No verificado:</b> genérico exacto del planificador en AliExpress · landed real · Amazon de los KILL.<br>
<b>Gasto Apify real</b> (API de Apify, ejecuciones de este barrido): ≈ $0,80 de $3 de tope.</div>

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
<li><b>Barrido B con 1 dudoso.</b> El planificador pasa escala (cozyhoome con 413 días) y el gate da POSIBLE (5 tiendas, no firme), pero Amazon lo vende a $10–12 con cientos de reseñas: tu PVP de $19,99 es ~2× Amazon.</li>
<li>Si lo miras: abre el vídeo de 413 días de cozyhoome y los de lamorial (páginas-persona). Si te convence, pide al agente el mismo libro y el landed antes de nada.</li>
<li><b>Q4:</b> Black Friday en ~5 semanas. Un producto nuevo necesita muestra, landing y creativos: si no lo lanzas antes del 7-nov, llegas tarde al pico.</li>
<li>Siguiente del orden: G (reseñas 1–2★) sobre una categoría del radar, o cerrar los dudosos que ya tienes.</li>
<li>Añade a EXCLUIDOS: rotulador de juntas, kit de parabrisas, guantes de gato, bóveda de semillas, adorno de alas de ángel.</li>
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
