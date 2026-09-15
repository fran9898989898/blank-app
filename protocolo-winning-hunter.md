# Protocolo de búsqueda en Winning Hunter

Reconstruido a partir de dos chats del 26 de agosto ("Búsqueda de producto nuevo" y "Verificación de productos y dominios AliExpress") y consolidado el 4 de septiembre. Caso de referencia: FluidVac.

## 1. Origen de la señal — Winning Hunter

- **Filtro guardado en Ads**: Countries US · Ad creation date últimos 14 días · Days Running ≤21 · Media video · Niche Home & Garden · Scaling activado. Sin filtro Min Days.
- **Brand Tracker** con watchlist de ~18 tiendas: achate, sofyre, celinva, mellowsleep; uprootclean, speedcleaning, krazyklean, geniecloth, everythingscrubber; statik, tryhills, ripplimpactgear; Norbbshop, Coozy land.
- Del paseo salieron 4 candidatos; se priorizaron 2 para verificar: White Furniture Touch-Up Paste (ypzvx.com) y Leak-Proof Fluid Extractor (cozyllio.com).
- Formato de shortlist en texto: `producto | dominio | días | active ads | qué te llamó`. Sin capturas del feed.

## 2. Embudo de verificación (manual, 48h)

1. Biblioteca de anuncios de Meta: contar operadores y sus fechas de entrada, buscar copy duplicado.
2. AliExpress: ¿clon con reseñas/pedidos recientes o cola vacía?
3. Ficha en `radar-producto.xlsx` con veredicto.

## 3. Gate de kill — la clave de FluidVac

- **Touch-Up Paste**: 8+ operadores, copy idéntico → muerto.
- **Fluid Extractor**: 8 operadores en 14 días (17–30 julio), Mroace/Dailyzahuo con copy calcado, el líder con ads en "impresiones bajas". El gate lo mataba; se rebatió: eso es saturación temprana, no mercado maduro — nadie llevaba meses escalando. AliExpress sin cola (últimas reseñas en mayo, pre-enjambre) → subasta en su punto más barato → Fase 1.

**Regla corregida**: lo que mata es enjambre + operador validado escalando durante meses, no el recuento de operadores.

## 4. Filtro de producto que tuvo que pasar

- Ticket $15-40
- Coste <$10
- Demo visual en 5s
- Admite packs
- Cero claims de salud
- Sin ropa ni suplementos
- USA solo

## 5. Lección

El filtro "creación ≤14 días" del feed detecta la estampida, no al pionero; la "forma correcta" (barato, demo visual, household) ya no discrimina. Por eso el Brand Tracker manda sobre el feed de descubrimiento.

## 6. Kill criteria de la herramienta

30 días sin un candidato que sobreviva a biblioteca = se cancela Winning Hunter, sin pena.
