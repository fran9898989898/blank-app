"""Barrido B (momentum Q4) del 21-oct-2026. Fuentes: STT (US, ≥30 d, ≥10 ads, visto desde el 17-oct, orden crecimiento 30 d),
Biblioteca de Meta vía Apify (30 anuncios por consulta, frase exacta), precios Shopify vía Apify, AliExpress US, Amazon US (1 búsqueda).
Lo no verificado va marcado."""

CDN = "https://searchthetrend.b-cdn.net/"

PASAN = [
 dict(
  tipo="Planificador de fin de vida («I'm dead, now what»)", en="end of life planner", sub="Papelería / regalo",
  anun=4, escala=["ok", "Escala: pasa (líder con 413 d)"], gate="POSIBLE", gateN=5, mercado=["ok", "US 80–91 %"],
  lider=dict(dom="cozyhoome.com", dias=413, ads=8, g30=-16.7, serie=[]),
  rivales="Biblioteca 21-oct (30 anuncios, frase exacta): 6 operadores, 4 con ≥30 d: lamorial.com (24 anuncios, 58 d, 4 páginas-persona «Anna Reid», «Helen Cartwright»; no está en STT), cozyhoome.com (413 d), mytrendyes.com (75 d), buildyourwill.com (servicio, no producto). "
           "STT: mindsparkl.com (129 ads, 37 d, +2.950 % 30d), perpetualing.com (25 ads, 31 d) y 4 tiendas-catálogo más con 1–6 ads y la misma foto.",
  pvp="VERIFICADO (Shopify vía Apify): cozyhoome $12,95 · mindsparkl y perpetualing $19,99 (1) · $37,99 (2) · $54,99 (3).",
  ali="No firme: la búsqueda de AliExpress devuelve libretas genéricas ($2–6), no el planificador exacto. Pide al agente el mismo libro que venden las tiendas.",
  alilink="",
  marca="AMAZON (leído 21-oct): «I'm Dead Now What» genérico $11,08 (563 reseñas, 600+/mes), otros $9,99–11,99 con 154–641 reseñas; «Peace of Mind Planner» $11,33 (9,7K reseñas). A $19,99 estás a ~2× Amazon: precaución.",
  q4="Débil como regalo navideño; vende a mayores de 60 («I'm 68 and love this»).",
  hueco=["Cozyhoome lleva 413 días con el mismo vídeo («Avoid family chaos»): ángulo probado.",
         "Lamorial escala con páginas-persona en primera persona (advertorial), como Mellow con el antifaz.",
         "Nadie vende el pack «uno para mí, otro para mis padres» con ángulo de regalo a hijos adultos."],
  riesgos=["Gate POSIBLE no firme: 5 tiendas con la misma foto; mindsparkl entró hace 37 días con 129 anuncios (enjambre en formación).",
           "Ancla Amazon $10–12 con cientos de reseñas.",
           "Genérico de Ali no verificado; papel = envío pesado para el precio."],
  ads=[
   dict(src="Cozy Hoome (líder por antigüedad)", id="780659771794914", d="2025-09-03", dias=413, fmt="vídeo", var=2, txt="Avoid family chaos. Our planner ensures your wishes are known and respected. ⚰️", cr=CDN+"humorous-end-of-life-planner/780659771794914/creative.mp4"),
   dict(src="Cozy Hoome", id="1537861234238315", d="2025-09-08", dias=408, fmt="vídeo", var=1, txt="Avoid family chaos. Our planner ensures your wishes are known and respected. ⚰️", cr=CDN+"humorous-end-of-life-planner/1537861234238315/creative.mp4"),
   dict(src="De-Mindsparkl (líder por volumen)", id="1060513803560273", d="2026-09-13", dias=37, fmt="vídeo", var=1, txt="💖✨I'm 68 and love this The End of Life Planner.❤️ It makes future planning easier and even fun.", cr=CDN+"i-m-dead-end-of-life-planner/1060513803560273-fd2ebfa72d5049daa0b6738a9c2145fc/creative.mp4"),
  ]),
 dict(
  tipo="Rotulador de juntas antimoho para azulejo", en="grout pen", sub="Hogar / baño",
  anun=10, escala=["warn", "Escala: pasa, pero enjambre (todos 37–54 d)"], gate="KILL", gateN=15, mercado=["ok", "US 98–100 %"],
  lider=dict(dom="mindsparkl.com", dias=50, ads=51, g30=2600, serie=[]),
  rivales="Biblioteca 21-oct: 15 operadores, 10 con ≥30 d (novthra, mindsparkl, norbbshop, dailyardmall 141 d, mytrendyes, kariney, perpetualing, pineapplea 111 d, bisnftwrem, dailyardpro) + Amazon. STT: bisnftwrem 54 ads, mindsparkl 51, perpetualing 36, todas con la misma foto.",
  pvp="VERIFICADO: mindsparkl y bisnftwrem $22,99 (tachado $44,99), 11 colores.",
  ali="Rotulador de juntas $1,09–2,26 (10.000+ vendidos). Landed ≈5–10 % de $22,99 antes de envío.",
  alilink="https://www.aliexpress.us/item/3256806811108291.html",
  marca="Commodity de ferretería (Home Depot/Amazon): no verificado el precio.",
  q4="No.",
  hueco=["Ninguno: mismo vídeo y misma foto en todas las tiendas."],
  riesgos=["Gate KILL: 15 operadores.", "Commodity: se ve por pocos dólares en ferretería."],
  ads=[
   dict(src="Bisnftwrem/D", id="1759390685548681", d="2026-09-03", dias=47, fmt="vídeo", var=1, txt="💧 Tired of looking at dark, stained grout lines that make your bathroom feel dirty no matter how much you scrub?", cr=CDN+"anti-mould-and-waterproof-joint-pen-for-ceramic-tiles/1759390685548681-e99097ec394b454ca3d38dd8aa3d0f57/creative.mp4"),
  ]),
 dict(
  tipo="Kit de reparación de grietas del parabrisas", en="windshield repair kit", sub="Auto",
  anun=4, escala=["warn", "Escala: pasa por STT; Biblioteca solo 2 con ≥30 d"], gate="KILL", gateN=12, mercado=["ok", "US mayoritario"],
  lider=dict(dom="beforesprouted.com", dias=34, ads=16, g30=-26.7, serie=[]),
  rivales="STT ≥30 d: colody (70 d), thegiftnorth (51 d), pinkdiyprint (50 d, 14 ads), beforesprouted (34 d, 16 ads), misma foto. Biblioteca 21-oct: 12 operadores (colody, definitein, botheloquent, perpetualing, joygrova, jaags…) + marcas Ultra Bond (121 d) y AutoZone.",
  pvp="VERIFICADO: beforesprouted y pinkdiyprint $21,99 (1) · $29,99–39,99 (3) · $39,99–49,99 (5).",
  ali="Kit de resina $0,33–4,49 (5.000+ vendidos; $0,33 es precio de nuevo usuario).",
  alilink="https://www.aliexpress.us/item/3256807958493950.html",
  marca="Sí: Rain-X, Permatex y Ultra Bond en AutoZone/Walmart (precio no verificado).",
  q4="No.",
  hueco=["UGC «I used to think a tiny chip wasn't a big deal» es el único ángulo; nadie enseña el antes/después en primer plano."],
  riesgos=["Gate KILL: 12 operadores.", "Marca de referencia en cualquier tienda de recambios."],
  ads=[
   dict(src="Beforesprouted.com", id="1330079182344020", d="2026-09-16", dias=34, fmt="vídeo UGC", var=1, txt="I used to think a tiny chip in my windshield wasn't a big deal… until I saw it start spreading.", cr=CDN+"fast-acting-windshield-crack-chip-repair-kit/1330079182344020-da6aa8ed5b094c119f6fdc90f9cdf2da/creative.mp4"),
  ]),
 dict(
  tipo="Guantes sin dedos de punto con gato", en="cat fingerless gloves", sub="Accesorios / regalo Q4",
  anun=3, escala=["warn", "Escala: dudosa (líder 43 d)"], gate="KILL", gateN=19, mercado=["ok", "US 95 %"],
  lider=dict(dom="bisnftwrem.com", dias=43, ads=44, g30=4200, serie=[]),
  rivales="Biblioteca 21-oct («fingerless gloves»): 19 operadores, 10 con ≥30 d, mezcla de tiendas de punto artesanal, marcas (Willis Judd, Five and Diamond), Amazon y tiendas-catálogo.",
  pvp="VERIFICADO: bisnftwrem $19,99, 8×8 combinaciones de color.",
  ali="Guantes de gato $2,79–3,59 (3.000–5.000+ vendidos).",
  alilink="https://www.aliexpress.us/item/3256807120381934.html",
  marca="No hay una referencia única: commodity de ropa de invierno.",
  q4="Sí: regalo «para amantes de los gatos».",
  hueco=["Pack «madre e hija» o «para tus 3 amigas gateras» que nadie hace."],
  riesgos=["Gate KILL: 19 operadores.", "Colores = muchos SKUs; textil barato en cualquier tienda."],
  ads=[
   dict(src="Bisnftwrem9-", id="1396139528608488", d="2026-09-08", dias=43, fmt="vídeo", var=1, txt="Warmth and style perfectly combined! 🐱✨ … 🎁 The perfect gift for cat lovers 👉", cr=CDN+"women-s-knitted-fingerless-gloves-with-cute-cat-cozy-stylish-practical-winter-ha/1396139528608488-448b5511ed9e44308aae2e2cb4751629/creative.mp4"),
  ]),
]

RADAR = [
 dict(tipo="Bóveda de semillas de supervivencia", dom="tryrivanta.com", dias=72, nads=932, pvp="No leído",
      motivo="Escala real (Biblioteca: 5 operadores con ≥30 d: rivanta, nuvera, tryfrdy, gardenspulse) pero fuera por regla: no hay genérico de AliExpress (importar semillas a EE. UU. está regulado por USDA/APHIS) y los anuncios venden miedo a la guerra.",
      ads=[dict(id="4536642759911959", d="2026-08-26", dias=56, fmt="imagen", var=1, txt="I asked my neighbor Clifford if this war with Iran worries him, and the retired Navy man answered by pointing at my chest freezer.", cr=CDN+"rivanta-survival-seed-vault/4536642759911959/creative.jpg")]),
 dict(tipo="Adorno navideño de alas de ángel con pájaros", dom="pinkdiyprint.com", dias=35, nads=1346, pvp="$16,99 · set de 8 $75,92",
      motivo="Un solo operador (1.346 anuncios en 35 días, testeo masivo). La Biblioteca solo devuelve 6 anuncios con la frase. No valida escala; vigilar si entra un segundo.",
      ads=[dict(id="2132756977452456", d="2026-09-16", dias=35, fmt="imagen", var=1, txt="❤️ Two little birds. A pair of angel wings. A beautiful way to say, \"You're close to my heart.\"", cr=CDN+"2026-angel-wing-heart-christmas-ornaments/2132756977452456-ec14212dcba643d6bce79ac437fe55b2/creative.jpg")]),
]

NOPASAN = [
 ["Cesta de freír plegable de acero", "1 (mygrandhearth, 92 ads, 36 d)", "Un solo operador."],
 ["Soplete de cocina BlazeTrigger", "1 (ventrafinds, 33 d)", "Un solo operador; gas: envío complicado."],
 ["Funda de sofá-cama para perro", "1 (teamk9, 110 d, marca)", "Un solo operador; tallas."],
 ["Set sensorial squishy / PolySquish", "2 distintos", "No es el mismo tipo; sin escala."],
 ["Kit de parches para neumáticos, tapones LED, cinta de doble cara", "—", "EXCLUIDOS o commodity (ya evaluados)."],
 ["Llave offset (wildgrizzly 162 ads), coating cerámico (ethos, 13supplies, bisnftwrem), soporte magnético (armotech)", "—", "EXCLUIDOS: evaluados en septiembre."],
 ["Personalizados (pinkdiyprint, prints10, macorner, trendingcustom, andyokay)", "—", "Fuera: print-on-demand."],
 ["Suplementos para perro, mascarillas EMS/LED, mangas EMS, sillas, patinetes, calefactores", "—", "Fuera: ingerible, claims o electrónica."],
 ["Gorro de punto, guantes, gorro de dormir", "—", "Commodity textil / tallas."],
]
