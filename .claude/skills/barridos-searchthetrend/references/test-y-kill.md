# Del visor al test: `tests.md`, checklist de lanzamiento, kill criteria y ronda 2

El barrido termina en el visor; el dinero empieza en el test. Esta parte no cambia el filtro ni el orden de barridos: cubre lo que pasa entre elegir 2–3 tipos y saber si venden.

## 1. `tests.md` (raíz de `product-radar`)

Claude lo crea vacío si no existe y lo lee antes de cada barrido. Una fila por producto elegido en un visor a partir de ahora; los tests antiguos solo entran si siguen encendidos:

```markdown
# Tests

| Producto | Barrido origen | Lanzado | PVP / pack | Landed % | CPA breakeven | Gasto | CTR | ATC | Compras | CPA | Estado | Motivo | Ronda 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| <producto del visor> | <A–G + fecha> | | | | | | | | | | PENDIENTE | | |
```

Estados: `PENDIENTE` (elegido en el visor, sin lanzar) · `EN TEST` · `VIVO` (CPA ≤ breakeven con ≥2 compras) · `ITERAR` · `MUERTO` (con el kill criterion que se cumplió).

Antes de un barrido nuevo, Claude avisa si hay: un `VIVO` sin ronda 2, candidatos `PENDIENTE` sin lanzar, o un `MUERTO` sin motivo. No bloquea: lo dice y deja constancia en la cabecera del visor. Las celdas vacías se rellenan con el Administrador de anuncios y Shopify; no se inventan.

## 2. CPA de breakeven (antes de lanzar)

```
Margen por pedido = PVP del pack − landed del pack − comisión de pago − devoluciones estimadas
CPA breakeven     = margen por pedido
CPA objetivo      = 0,7 × CPA breakeven
```

Por pack (1, 2, 3 unidades). Sin datos de mix, usa el pack intermedio. Comisión y devoluciones: las reales de tu pasarela e histórico.

## 3. Checklist de lanzamiento (si falla uno, no se lanza)

1. **Compra de prueba real** desde el móvil con dirección US, pack intermedio, hasta la página de gracias. Reembolsar después.
2. **Eventos** en el Administrador de eventos de Meta: `ViewContent`, `AddToCart`, `InitiateCheckout`, `Purchase`. Pixel + CAPI deduplicados por `event_id`. La compra de prueba tiene que aparecer como `Purchase`.
3. **Permalinks** de cada pack abren el carrito con la variante y cantidad correctas.
4. **Mismo precio en landing y checkout.**
5. **Plazo de entrega real** del agente visible en landing y checkout.
6. **Amazon a mano** (la skill lo deja como comprobación manual en finalistas): genérico Prime a ≤⅓ de tu PVP → piénsalo dos veces.

## 4. Estructura del test

- 2–3 productos del visor **en paralelo**, no uno detrás de otro.
- 1 campaña por producto, 3 creativos (demo 5 s, dolor, regalo/pack).
- Presupuesto por producto: hasta **3× CPA breakeven** antes de juzgar compras. Optimización a `Purchase`.

## 5. Kill criteria (con cifras en `tests.md` antes de gastar)

| Señal | Umbral | Acción |
|---|---|---|
| CTR enlace | <1 % tras ~1.000 impresiones por creativo | Cambiar creativo; 3 creativos <1 % → kill |
| Compras | 0 con gasto ≥ 3× CPA breakeven | Kill |
| Carritos sin compra | ≥5 ATC y 0 compras | Auditar checkout y eventos antes de matar. Funciona → precio ancla → kill. Falla → arreglar y relanzar |
| CPA | 1×–1,5× breakeven | Una ronda más cambiando oferta/pack |
| CPA | ≤ breakeven con ≥2 compras | VIVO → ronda 2 |

No son motivo de kill: mala espina, un día malo, CPM alto un día, que salga otro producto en un barrido.

Umbrales de partida, no ley: ajústalos cuando tengas ≥5 tests registrados (tuyos y de tus compañeros).

## 6. Ronda 2 de un producto VIVO

1. Vídeo nuevo con el ángulo que convirtió + 1 ángulo nuevo (regalo Q4 si hay ventana).
2. Pack con anclaje al intermedio ("uno por coche", "uno por hijo").
3. Upsell o bundle del mismo comprador (aquí entra el Barrido C o la parte "línea" del B).
4. +20–30 % de presupuesto cada 48 h mientras el CPA siga ≤ breakeven.
5. CPA > 1,5× breakeven 3 días seguidos con gasto ≥ 3× breakeven → ITERAR o MUERTO con motivo.
