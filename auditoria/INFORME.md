# Autoauditoría + arranque — 1-oct-2026

## 1. Gasto Apify (ciclo completo: 569 runs, $14,50; límite del panel $19)
| Actor | Uso del resultado | Runs | Items | Coste |
|---|---|---|---|---|
| facebook-ads-scraper | usado | 46 | 1.028 | $5,14 |
| facebook-ads-scraper | sesión anterior | 38 | 809 | $4,12 |
| rag-web-browser | NO: reintento/repetida | 223 | 223 | $1,81 |
| rag-web-browser | usado | 97 | 97 | $1,40 |
| rag-web-browser | NO: candidato descartado/repetido | 76 | 76 | $1,26 |
| rag-web-browser | sesión anterior | 46 | 46 | $0,42 |
| shopify | usado / anterior | 39 | 174 | $0,29 |
| otros | — | 4 | 142 | $0,06 |
Detalle por run: auditoria/apify_runs.csv. Desperdicio directo: **$3,07 (21 %)**.
Por qué se pasaron los topes: (1) el tope era un contador estimado en el script, no el gasto real; estimaba $0,0025/página y el real es $0,009–0,016; (2) reintentos automáticos (Amazon: 260 runs para 59 búsquedas); (3) resultados vacíos guardados como [] y vueltos a pedir; (4) cada script nuevo empezaba el contador en 0.
Arreglo: tools/apify_guard.py (única puerta). Demo (auditoria/demo_guard.txt): caché, recorte a 30 items/$0,50, corte a $2 y 0 runs nuevos. Esta sesión, partes 5–6: 5 runs, $0,053 reales.

## 2. Embudo (143 tipos)
| Criterio | Muertes |
|---|---|
| Ancla Amazon (equivalente Prime ≥100 reseñas < $25) | 75 |
| Precio / margen | 15 |
| Gate / enjambre | 14 |
| Regla de producto | 14 |
| Escala | 10 |
| Marca de referencia | 9 |
| Antigüedad | 3 |
| AliExpress, sin verificar, otro | 3 |
Asesino: Ancla Amazon (52 %). Simulación relajando SOLO ese: ≥$20 → 0 pasan; ≥$18 → 1; ≥$15 → 4; ≥$12 → 8. No es demasiado estricto: los productos pequeños y no electrónicos cuestan $5–12 en Amazon. El fallo es el universo de búsqueda, no el umbral.

## 3. Capacidades y viabilidad
Puedo: STT, Apify con guard, AliExpress directo, leer tiendas vía Apify, Gmail, escribir landing/políticas/creativos.
No puedo: entrar en el admin de Shopify, Meta Business, Cloudflare ni pagar; no hay tokens de Shopify ni Meta.
¿3 productos testeables esta semana con los criterios actuales? **No**: en 143 tipos ninguno pasa todos.

## 4. TOP 3 (no pasan al 100 %)
Ver la tabla del chat. Datos: barridos/2026-10-01-ECO/eco.json.

## 5. Tienda
tienda/infra.md (estado) + tienda/politicas/*.md.

## 6. Landing del #1 (banda de pedal)
tienda/landing-banda-pedal.md + tienda/lideres/*.md.
