---
name: "barridos-searchthetrend"
description: "Barridos de producto para dropshipping con SearchTheTrend (MCP) + Apify desde Claude Code: protocolo en orden (A escala → D vía lateral → E Biblioteca directa → F geo-lag → B momentum → G reseñas → C familia), filtro por ESCALA para hogar/auto, VÍA LATERAL para nichos de hobby, Biblioteca como radar cuando STT no indexa. Úsala cuando el usuario quiera buscar producto nuevo, \"hacer un barrido\", \"pasar por searchthetrend\", \"qué barrido toca\", candidatos Q4, por línea/familia, nichos apasionados, o pida \"el visor\" o \"la ficha\"."
---

# Barridos de producto con SearchTheTrend + visor

Método de sesiones reales (24–28 sep 2026). Siete barridos, dos filtros (uno por tipo de nicho), un visor y **un orden de ejecución**. El objetivo NO es que Claude recomiende: es que el visor te ponga delante los datos y los anuncios de los rivales y **tú decidas mirando**. Claude filtra números; el ojo lo pones tú.

Expectativa realista: en la sesión de origen salieron 2 productos testables de ~40 tipos mirados en 6 barridos; dos barridos enteros dieron 0 de 10. **Cero es un resultado normal.** Más barridos no fabrican ganadores; sirven para cambiar la pregunta cuando la anterior no tenía respuesta.

## 0. Dónde se trabaja (una sola copia)

**Una sola fuente de verdad: la rama `main` del repo `blank-app` en GitHub.** Skill, scripts (`tools/`), barridos y `barridos/radar.html` viven ahí. Cualquier copia que no esté al día con `main` da resultados viejos.

Dos formas de trabajar, las dos valen (también desde el móvil la primera):
- **Nube (web o app de Claude, también móvil)**: sesión de Claude Code sobre `blank-app`, rama `main`. El entorno ya tiene STT conectado y `APIFY_TOKEN`. Al terminar, Claude sube el barrido y abre un PR a `main`; se fusiona desde GitHub.
- **PC (Windows)**: en la carpeta donde esté clonado el repo (la ruta no importa), `git checkout main` y `git pull` **antes de cada barrido**; luego `claude`. Atajo opcional: `notepad $PROFILE` → `function radar { Set-Location <tu carpeta>; git pull; claude }`.

Antes de empezar, Claude comprueba que está en `main` y al día (`git status`, `git pull`). Si está en otra rama o atrasado, lo dice y lo arregla antes de barrer.

Requisitos (solo la primera vez en un equipo nuevo; ver `references/setup.md`): STT conectado como MCP (`/mcp` → `searchthetrend · Connected`) y `APIFY_TOKEN` en el entorno con límite mensual en Apify → Settings → Usage. El pipeline ya existe en `tools/`: no hay que construirlo.

## 1. El orden de ejecución (qué barrido toca)

Un barrido por sesión. Se pasa al siguiente solo si el anterior deja **menos de 2 tipos** que te llamen tras leer el visor. Cada producto descartado entra en EXCLUIDOS del siguiente.

| Paso | Barrido | Cuándo | Si sale 0 |
|---|---|---|---|
| 1 | **A — Escala general** | Primer barrido, sin dirección | → 2 |
| 2 | **D — Nichos apasionados (vía lateral)** | Siempre como segundo: STT indexa mal los hobbies y el filtro cambia | → 3 |
| 3 | **E — Biblioteca directa por keywords** | Verticales que STT no ve (seguridad, digital, servicios, funnels propios) | → 4 |
| 4 | **F — Geo-lag** | Lo que escala en UK/AU/DE/CA y aún no en US, o al revés | → 5 |
| 5 | **B — Momentum** | Q4 o cualquier ventana estacional a 6–10 semanas | → 6 |
| 6 | **G — Reseñas 1★ del líder** | Tienes una categoría que te gusta pero ningún tipo pasa | → revisar filtro |
| — | **C — Familia de producto** | Solo cuando ya tienes una venta real; explota el mismo comprador | → volver al que vende |

**Regla de parada**: tres barridos seguidos con 0 → el problema no es el método. Antes del cuarto, revisa en este orden: (a) ¿estás descartando en el visor por gusto y no por los 7 puntos de lectura (§5)? (b) ¿ticket $15–40 demasiado estrecho? Prueba $15–60 una vez. (c) ¿gate ≤2 demasiado duro? POSIBLE (3–5) también se testea. (d) ¿estás en un vertical que STT no indexa? → E. Un producto que vende vale más que tres que igual venden: si tienes uno vivo, vuelve a él.

## 2. Filtro por escala (hogar, cocina, baño, auto, jardín, herramientas…)

Antes se buscaba "≤20 ads y un anunciante con ≥5". Los dos últimos productos que pasaron ese filtro murieron; el que dio dinero salió de una marca escalando a lo grande. **El unicornio por sistema es perdedor. Entra donde ya hay tres o más ganando y gana por ejecución.**

| Criterio | Regla | Qué hace |
|---|---|---|
| **Escala** | ≥3 anunciantes distintos con ≥30 días anunciando el mismo TIPO de producto en US, y al menos uno con ≥15 ads activos **o** serie semanal de `adsFound` creciendo en las últimas 8 semanas | Filtra. Un solo superviviente no valida, ni con 13 meses |
| **Mercado** | US ≥50 % de los anuncios | Filtra |
| **Ticket** | PVP $15–40 | Filtra |
| **Genérico** | equivalente funcional en AliExpress <$10; landed ≤18 % del PVP deseable, 25 % techo | Filtra |
| **Producto** | sin claims médicos, sin suplementos/ingeribles, sin electrónica compleja (ni Bluetooth, ni LED, ni resistencias), sin tallas/modelos (1–3 SKUs), demo visual en 5 s, packs posibles | Filtra |
| **Gate de dropshippers del genérico** | ≤2 → PRIORIDAD · 3–5 → POSIBLE · ≥6 → KILL (contado en la Biblioteca de Meta) | Filtra |
| **Hueco de ejecución** | rivales sin packs, demo floja, landings sucias, ángulo obvio sin usar | **Se anota, no filtra.** Es lo que tú miras para elegir |
| Amazon como techo | no filtra; se mira a mano en finalistas: genérico Prime a un tercio de tu PVP = cuidado | Manual |

Dinero: **tope Apify por barrido $3**, gasto real leído del panel. STT pre-filtra gratis; Apify solo cuando STT deja dudosos.

## 3. Vía lateral (nichos de hobby y apasionados)

En camping, pesca, caza, RV, DIY, BBQ, huerto, golf, arte, jeep, moto, caballos… **el filtro "≥3 anunciantes" no sirve**: manda **una marca DTC única por producto** (tobioskits 229+ ads y ~$101K/mes; blackbeardfire; rodarmour; sawinery; finalputt). La señal cambia:

- **Señal de demanda** = una marca sola con ≥100 anuncios activos y ≥90 días, creciendo. No hacen falta tres.
- **El trabajo no es copiar a la marca**: (1) ¿qué JOB compra su cliente? ("empezar a pintar sin saber", "encender fuego sin gasolina"); (2) ¿qué genérico de AliExpress <$10 hace ese JOB? (3) **gate por dropshippers del genérico** (≤2 PRIORIDAD · 3–5 POSIBLE · ≥6 KILL). Así salieron TankFresh y Tintlet.
- **Hueco típico**: entrada más barata que la marca (<$20), kit por motivo/ocasión, pack que la marca no hace.
- **Sin vía lateral** si la marca ES la referencia de la categoría (Scorch Marker, Emson Car Cane) o vende un kit pro a $90 con accesorios.
- "Regalo Q4 / comprador (aficionado vs pareja)" son columnas informativas, no filtros.
- Claims de la marca (therapy, anxiety, stress relief, dopamine) **no se copian**.

## 4. Los siete barridos

A–D están para pegar en `references/prompts.md`. E–G van aquí. Todos usan la misma anatomía (§6): cambia solo la pregunta y las columnas.

| Barrido | Pregunta | Filtro |
|---|---|---|
| **A — Escala general** | ¿Qué tipos tienen ≥3 anunciantes escalando ahora en hogar/cocina/baño/auto/jardín/outdoor/herramientas/bebé/belleza/viaje? | §2 |
| **B — Momentum + línea** | ¿Qué marcas han crecido ≥50 % en anuncios activos en 4 semanas? + ¿qué segundo producto compra el cliente de mi producto vivo? | §2 + ventana en semanas |
| **C — Familia** | ¿Qué comparte comprador y motivación con lo que ya vende? Columnas: marca de referencia, regalo Q4 | §2 |
| **D — Nichos apasionados** | ¿Qué marcas DTC únicas escalan en hobbies? Columnas: JOB, genérico Ali, gate, marca de referencia | §3 |
| **E — Biblioteca directa** | STT no ve el vertical: descubrir anunciantes por keyword en la Biblioteca de Meta | §2 sobre lo que devuelva la Biblioteca |
| **F — Geo-lag** | ¿Qué escala en UK/AU/DE/CA con ≥60 días y en US tiene ≤2 anunciantes? (o US → UK/AU si vendes allí) | §2 aplicado al geo destino |
| **G — Reseñas 1★** | En una categoría elegida, ¿qué se quejan los compradores del líder (Amazon 1–2★) y qué genérico resuelve esa queja? | §3 (JOB → genérico → gate) |

### Prompt E — Biblioteca directa por keywords
```
Barrido E (Biblioteca directa), fecha AAAA-MM-DD. Reutiliza product-radar (actor Apify de la Biblioteca, lateral.py, WebFetch). Tope Apify $3. Salida: barridos/AAAA-MM-DD-E/.
VERTICAL: <p. ej. seguridad en casa | organización de garaje | cuidado de plantas | productos digitales personalizados>.
KEYWORDS (8–12, en inglés, como las diría un anuncio): <lista>.
FASE A — Descubrimiento (Apify, una corrida): Biblioteca de Meta, country=US, activos, 30 anuncios por keyword. Agrupa por dominio de destino (sácalo del link del anuncio; si no hay, por página). Descarta retail (Amazon, Walmart, Home Depot), concesionarios, salud, cursos. Guarda candidatos.json.
FASE B — Landing (WebFetch, $0): por dominio: producto exacto, precio, packs, plataforma (Shopify sí/no), suscripción, país de envío, claims. Agrupa por TIPO de producto. Cruza cada dominio con STT (search_brands) para días y serie semanal si está indexado; si STT dice "brand not found", anota NO INDEXADO y usa la fecha del anuncio activo más antiguo como mínimo de días.
FASE C — Genérico + gate: para cada tipo con ≥3 anunciantes (o 1 marca con ≥100 ads), genérico en AliExpress <$10 y recuento de dropshippers del genérico (≤2 PRIORIDAD · 3–5 POSIBLE · ≥6 KILL).
ENTREGA: visor.html (un fichero) con tarjeta por tipo: anunciantes, líder, días mínimos, precio, genérico, gate, marca de referencia, hueco; textos de los 3 anuncios más antiguos con link a la Biblioteca; filtros por gate y por "STT indexado sí/no". Gasto real de Apify del panel. Sin recomendación: elijo yo.
```

### Prompt F — Geo-lag
```
Barrido F (geo-lag), fecha AAAA-MM-DD. Reutiliza product-radar. Tope Apify $3. Salida: barridos/AAAA-MM-DD-F/.
GEO ORIGEN: <GB, AU, DE, CA> · GEO DESTINO: US (o al revés).
FASE A (STT, $0): search_products con countries=[origen] y minDaysRunning=60, por subnicho (hogar, cocina, baño, auto, jardín, herramientas, bebé, viaje). Agrupa por TIPO. Quédate con tipos con ≥2 anunciantes en origen y serie estable o creciendo.
FASE B (STT, $0): para cada tipo, repite la búsqueda con countries=[destino]. Conserva solo los tipos con ≤2 anunciantes en destino (el lag es el hueco). Anota ticket en cada geo.
FASE C: genérico Ali <$10, envío al destino, gate de dropshippers del genérico en la Biblioteca del destino.
ENTREGA: visor.html con tarjeta por tipo: anunciantes origen vs destino, días, líder en origen (dominio, ads, 3 anuncios más antiguos con link), precio en cada geo, genérico, gate, marca de referencia en destino. Ordenado por (anunciantes origen − anunciantes destino). Gasto Apify del panel. Sin recomendación.
```

### Prompt G — Reseñas 1★ del líder
```
Barrido G (reseñas del líder), fecha AAAA-MM-DD. Reutiliza product-radar (actor Apify de reseñas de Amazon si existe; si no, WebFetch de las páginas de reseñas filtradas por 1–2 estrellas). Tope Apify $3. Salida: barridos/AAAA-MM-DD-G/.
CATEGORÍA: <p. ej. limpieza de cisterna | organización de maletero | cuidado de cuero>. LÍDERES: <3–5 ASIN o marcas>.
FASE A: 150–300 reseñas de 1–2★ por líder. Agrupa las quejas en JOBS no resueltos ("no llega a X", "se rompe al Y", "hay que Z cada día"). Cuenta frecuencia por JOB.
FASE B: para cada JOB con ≥10 menciones, ¿qué genérico de AliExpress <$10 lo resuelve o lo evita? (equivalente funcional, no la misma referencia).
FASE C: para cada genérico, ¿quién lo anuncia ya en US? (STT search_products + Biblioteca): anunciantes, días, gate de dropshippers.
ENTREGA: visor.html con tarjeta por JOB: frecuencia, 5 citas literales de reseñas, genérico propuesto (precio, link), anunciantes actuales, gate, ángulo de creativo sugerido a partir de las citas (solo texto; sin claims de salud). Sin recomendación.
```

Y un **mini-check** de $0,30 para un tipo suelto (en `references/prompts.md`).

## 5. Cómo leer el visor (`references/leer-visor.md` tiene casos reales)

1. **Gate y "firme/no firme"**: KILL se ignora. "No firme" = genérico no verificado; cuenta como duda.
2. **Anunciantes y líder**: marca DTC con demanda real, o 5 tiendas genéricas que entraron la misma semana = **enjambre**, no demanda (recortador de grasa, telar de zurcir).
3. **Los 3 anuncios más antiguos del líder**: un vídeo con 300 días encendido es un ángulo probado. Ábrelos.
4. **Marca de referencia en la cabeza del comprador** (Addalock, Slime, Turtle Wax, Car Cane): el creativo tiene que responder "¿por qué a ti y no a ellos?". Si no puede, fuera.
5. **Commodity**: se ve por $3 en el Dollar Tree → no hay hueco.
6. **Electrónica disfrazada** (LED, Find My, resistencia) → fuera aunque diga PRIORIDAD.
7. **Hueco de ejecución**: packs que nadie hace, demo que nadie enseña, landing sucia, ángulo sin usar. Esto decide entre los que pasan.

Salida: **2–3 tipos**. Con ellos, ficha de decisión (breakeven por pack, ángulo, mensaje al agente) antes de montar nada. Antes de montar: precio del genérico en Amazon Prime a mano; un competidor "vivo" no valida, tres escalando o una marca DTC grande sí.

Del visor al test: registro en `tests.md`, checklist de lanzamiento (compra de prueba US, eventos del pixel, permalinks), 2–3 tests en paralelo y kill criteria escritos antes de gastar → `references/test-y-kill.md`. Si hay un producto VIVO sin ronda 2, avísalo antes de barrer.

## 6. Anatomía del prompt (para modificarlo)

1. **Cabecera**: nombre, fecha, tope Apify, carpeta `barridos/AAAA-MM-DD-<letra>/`, "reutiliza los scripts".
2. **FILTRO**: §2 o §3 según el nicho. Si aflojas algo, aquí y en ningún otro sitio.
3. **EXCLUIDOS**: todo lo ya fichado o probado.
4. **FASE A — Candidatos (STT, $0)**: `search_brands` por meta_ads y `search_products` con `minDaysRunning=30` y `countries=US`. **Agrupa por TIPO, no por tienda.** "Brand not found" en cadena → barrido E.
5. **FASE B — Genérico**: AliExpress + gate. Apify solo si STT deja dudas.
6. **FASE C — Ficha**: tipo, anunciantes, líder, PVP, genérico, gate, hueco, 3 anuncios más antiguos con link. Añade columnas según barrido.
7. **ENTREGA**: `visor.html` un fichero, filtros, `start visor.html`, gasto real de Apify, **"Sin recomendación: elijo yo mirando los anuncios"**.
8. **RADAR (siempre, sin que el usuario lo pida)**: al terminar, añade cada tipo evaluado a `barridos/radar.html` (el acumulado de todos los barridos): una pestaña nueva en `BARRIDOS` y una entrada por tipo en `T` con el mismo formato que las existentes y estado `vivo` (pasa todo el filtro) · `duda` (pasa con dudas o datos sin verificar) · `kill` (falla escala, gate, ancla o ticket) · `fuera` (regla de producto: claim, electrónica, tallas, POD, mercado). Actualiza «Siguiente paso» y el gasto de Apify del ciclo. Solo datos leídos en el barrido; lo no verificado se escribe como «no verificado».

## 7. Reglas operativas

- Un barrido = una sesión de Claude Code. No metas otro prompt hasta tener el visor.
- Bash > 7 min → `ctrl+b` a segundo plano; no `/clear` hasta tener el resumen.
- Autopsia con datos: pide el resumen completo y relee los números; el veredicto de Claude no es un motivo.
- Cada descartado → EXCLUIDOS del siguiente.
- **Entrega final de cada barrido**: el visor del barrido + `barridos/radar.html` actualizado + en el chat un resumen corto: vivos, dudosos, KILL y fuera (con el total acumulado), qué barrido toca después según §1 y el gasto real de Apify. EXCLUIDOS del siguiente barrido = todo lo que ya está en el radar.
- **Kill del research**: sin tipos con escala + hueco no se fuerza; se pasa al siguiente barrido del orden (§1). Tres ceros seguidos → revisar filtro y lectura antes de seguir barriendo.

## Referencias
- `references/prompts.md` — barridos A–D + mini-check.
- `references/leer-visor.md` — campo a campo del visor y lecturas reales.
- `references/setup.md` — MCP de STT, Apify, pipeline inicial.
- `references/test-y-kill.md` — `tests.md`, checklist de lanzamiento, kill criteria y ronda 2.
