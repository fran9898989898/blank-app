# Barrido R (rookie) — un solo barrido que siempre te da algo que testear

Esto sustituye a los siete barridos. Es UN barrido, con UN prompt, que termina en UN visor con 10 productos ordenados. No sale para encontrar ganadores: sale para que tengas 10 productos testables delante y aprendas a testear con uno. Un producto que testeas y muere te enseña más que un mes buscando el perfecto.

Orden obligatorio: **Paso 0 (prueba de vida) → Paso 1 (barrido) → Paso 2 (elegir mirando el visor) → Paso 3 (ficha de test y kill)**. No saltes el paso 0. El 90 % de los "me da todo a cero" es que algo del paso 0 está roto.

---

## Paso 0 — Prueba de vida (haz esto antes de nada)

### 0.1 Lo que necesitas instalado (una vez)

1. **Claude Code** funcionando. Abre PowerShell y escribe `claude`. Si no arranca, esto va antes que nada.
2. Una carpeta de trabajo: `C:\Proyectos\radar\`. Créala vacía.
3. **SearchTheTrend (STT)** en plan Pro (~$49/mes). Con el trial de $1 el barrido no funciona: se queda sin créditos a la segunda consulta y te devuelve vacío, que es lo que tú ves como "cero".
4. **Apify**: cuenta en apify.com → Settings → Integrations → copia el API token. En Settings → Usage pon un **límite mensual de $10**. Es el único freno real.
5. Dentro de `C:\Proyectos\radar\` crea el archivo `.env` con una línea:
   ```
   APIFY_TOKEN=tu_token_aqui
   ```

### 0.2 Conectar STT a Claude Code

En PowerShell (fuera de claude):
```
claude mcp add --transport http searchthetrend https://www.searchthetrend.com/api/mcp --header "Authorization: Bearer TU_TOKEN_DE_STT" -s user
```
El token de STT lo sacas en searchthetrend.com → tu cuenta → API / MCP.

Comprobación: `cd C:\Proyectos\radar`, `claude`, y dentro escribe `/mcp`. Tiene que poner `searchthetrend · Connected`. Si no:

| Lo que ves | Qué es | Qué haces |
|---|---|---|
| No aparece searchthetrend en `/mcp` | No se añadió | Repite el `claude mcp add` y reinicia `claude` |
| Aparece pero `Failed` / `Unauthorized` | Token mal o viejo | `claude mcp remove searchthetrend -s local` y `claude mcp remove searchthetrend -s user`, luego vuelve a añadirlo con el token nuevo. Un token viejo en scope local manda sobre el nuevo |
| `Login expired` | Es tu sesión de Anthropic, no STT | `/login` |
| Conectado pero las consultas devuelven vacío o error de cuota | Sin créditos | Mira el plan en STT. Trial = no sirve |

### 0.2b Carpetas (que Code te lo organice, no tú)

Pega esto una sola vez, antes de la prueba de vida, dentro de `C:\Proyectos\radar`:

```
Organiza esta carpeta para los barridos de producto y no toques nada fuera de ella. Crea:
- .env (ya existe; no lo muevas ni lo leas en voz alta)
- scripts/  → aquí van todos los .py que construyas (STT, AliExpress, Apify, generador del visor). Reutilízalos en cada barrido en vez de reescribirlos.
- barridos/AAAA-MM-DD/  → una carpeta por barrido con tipos.csv, anuncios.json y visor.html
- tests/<producto>/  → una carpeta por producto que decida testear, con ficha-test.txt y resultados.txt
- EXCLUIDOS.md  → lista de tipos ya probados o descartados; léela al empezar cada barrido y añade lo que yo te diga
- README.md  → tres líneas: cómo se lanza la prueba de vida, cómo se lanza un barrido, dónde queda el visor
Confírmame la estructura con `tree` y nada más.
```

A partir de aquí, cada prompt de barrido empieza con "Reutiliza los scripts de scripts/ y lee EXCLUIDOS.md". No borres carpetas de barridos viejos: son tu historial.

### 0.2c Móvil y PC

Los barridos se lanzan **solo desde el PC** con Claude Code: STT está conectado en tu PC, Apify lee el `.env` de tu PC y el visor se genera ahí. Desde el móvil no se lanza nada.

Lo que sí puedes hacer desde el móvil:
- **Ver el visor**: `visor.html` es un solo fichero. Pide a Code que, al terminar cada barrido, suba `barridos/` a un repo privado de GitHub (o lo copie a tu Drive). Lo abres en el móvil desde ahí y los botones "Ver en la Biblioteca" funcionan igual. Añade al final del prompt del barrido: "Al terminar, haz commit y push de barridos/ al repo".
- **Mirar los anuncios**: los links a la Biblioteca de Meta y a las tiendas de los rivales se abren mejor en el móvil que en ningún sitio. El paso 2 (elegir mirando) es de sofá.
- **Chat con Claude** (la app): para pensar la ficha de test, los ángulos o leer un resultado. Pégale la tarjeta o la ficha; no le pidas que busque producto, no tiene STT.

Regla: PC ejecuta, móvil mira y decide. Si intentas ejecutar desde el móvil, vuelves a "no arranca".

### 0.3 El prompt de prueba de vida (pégalo en Claude Code dentro de `C:\Proyectos\radar`)

```
Prueba de vida del radar. No busques producto todavía. Haz exactamente esto y escribe el resultado en prueba-de-vida.txt:
1. Lista las herramientas del MCP searchthetrend (nombres exactos). Si el MCP no responde, para y dime el error literal y cómo arreglarlo.
2. Lanza UNA consulta pequeña a STT: productos con anuncios activos en US, mínimo 30 días, límite 5 resultados. Pega los 5 nombres y sus días. Si devuelve vacío o error de cuota, para y dime que STT no tiene créditos.
3. Lee APIFY_TOKEN de .env. Lanza UNA corrida mínima del actor de Meta Ads Library de Apify (búsqueda "car organizer", país US, 5 anuncios, activos). Pega el nombre de la página y la fecha de inicio de los 5. Si falla, para y dime el error literal.
4. Si los tres pasos salen bien, escribe "OK — listo para el barrido R" al final del fichero y dímelo.
No construyas nada más. No me pidas que mire nada a mano.
```

Si los tres pasos dan OK, sigue. Si uno falla, arregla ese y repite la prueba. **No pases al barrido con la prueba en rojo**: el barrido te dará cero y no sabrás por qué.

### 0.4 Camino B si STT nunca te funciona

Si tras dos intentos STT no conecta o no tiene créditos, el barrido R funciona solo con Apify (pierdes las series de días por marca, pero el resto sale igual). En el prompt del paso 1, sustituye la FASE A por la línea marcada como "FASE A (camino B)". No te quedes parado por STT.

---

## Paso 1 — El barrido R

### 1.1 El filtro (no lo toques la primera vez)

| Criterio | Regla | Por qué |
|---|---|---|
| Mercado | US | Es donde testeas |
| Antigüedad | El anuncio más antiguo del tipo de producto lleva **entre 21 y 120 días** activo | Menos de 21 = nadie ha demostrado nada. Más de 120 = o es una marca contra la que no puedes, o está quemado |
| Competencia | **3 a 8 anunciantes distintos** con ≥21 días anunciando el mismo tipo de producto | Menos de 3 = no validado. Más de 8 = demasiada gente para un primer test |
| Ticket | Los rivales lo venden a **$20–45** | Margen para pagar el anuncio |
| Coste | Equivalente funcional en AliExpress **<$12** con envío a US | Landed ≤25 % del precio de venta |
| Demo | Se entiende qué hace en un vídeo de 5 segundos sin leer nada | Si hay que explicarlo, no es para un primer test |
| Visual humano | En al menos uno de los 3 anuncios más antiguos **aparece una persona usando el producto** (manos o cara) | Los anuncios que funcionan en frío enseñan a alguien usándolo |
| Tallas | 1–3 variantes máximo | Sin tallas, sin colores infinitos |

**Fuera siempre**: suplementos e ingeribles; cualquier cosa con claim de salud (dolor, ansiedad, sueño, peso, piel "cura"); ropa, calzado y todo lo que tenga tallas; cosmética con promesa; cualquier cosa que necesite app, Bluetooth o emparejamiento. **Dentro**: hogar, cocina, baño, coche, mascotas, jardín, viaje, organización, gadgets simples (pila o USB, sin app), belleza sin promesa (accesorios, herramientas).

**Escalera automática (para que nunca salga cero)**: si con el filtro tal cual salen menos de 10 tipos, Claude baja UN escalón cada vez y lo escribe en el visor:
- Escalón 1: antigüedad 14–180 días.
- Escalón 2: anunciantes 2–12.
- Escalón 3: ticket $15–60.

Cada tarjeta del visor dice con qué escalón entró. Un producto que entró por el escalón 3 es peor candidato que uno que pasó el filtro base, y lo vas a ver.

### 1.2 El prompt (pégalo tal cual en Claude Code dentro de `C:\Proyectos\radar`; cambia solo la fecha y los excluidos)

```
Barrido R (rookie), fecha AAAA-MM-DD. Carpeta de salida: barridos/AAAA-MM-DD/. Tope de gasto en Apify: $2 (lee APIFY_TOKEN de .env; para al llegar al tope y dímelo). STT está conectado como MCP: lista sus herramientas al empezar y usa las que correspondan. No me pidas mirar nada a mano hasta el visor.

FILTRO BASE:
- País US.
- Tipo de producto (función, no tienda): el anuncio más antiguo del tipo lleva entre 21 y 120 días activo; entre 3 y 8 anunciantes distintos con ≥21 días.
- Precio de venta de los rivales $20-45. Equivalente funcional en AliExpress <$12 con envío a US (landed ≤25 % del precio de venta).
- Se entiende en 5 segundos sin texto. 1-3 variantes. En al menos uno de los 3 anuncios más antiguos aparece una persona usando el producto.
- FUERA: suplementos/ingeribles, cualquier claim de salud, ropa/calzado/tallas, cosmética con promesa, cualquier cosa con app/Bluetooth/emparejamiento.
- DENTRO: hogar, cocina, baño, coche, mascotas, jardín, viaje, organización, gadgets simples (pila/USB sin app), belleza sin promesa.
ESCALERA: si con el filtro base hay menos de 10 tipos, baja un escalón y anótalo en cada tarjeta: (1) antigüedad 14-180 días; (2) anunciantes 2-12; (3) ticket $15-60. Nunca entregues menos de 10 tipos: si tras el escalón 3 siguen faltando, rellena con los mejores que tengas y marca "fuera de filtro" con el motivo.

EXCLUIDOS (no volver a evaluar): <lista de lo que ya has probado o descartado; vacío la primera vez>.

FASE A — Candidatos (STT, $0): para cada categoría DENTRO, busca productos y marcas con anuncios activos en US y mínimo 21 días. Agrupa por TIPO DE PRODUCTO, no por tienda (colapsa tiendas gemelas por dominio myshopify). Por tipo: nº de anunciantes distintos ≥21 días, líder (dominio, días, anuncios activos), días del anuncio más antiguo, precio de venta de 2-3 rivales (léelo de su tienda: /products.json si es Shopify). Aplica el filtro base y la escalera. Guarda tipos.csv.
FASE A (camino B, solo si STT no funciona): con el actor de Meta Ads Library de Apify, busca 25 anuncios activos en US por cada una de estas keywords: car organizer, kitchen gadget, pet grooming, bathroom organizer, garden tool, travel organizer, cleaning tool, closet organizer, car cleaning, dog toy, cat furniture, kitchen storage, desk organizer, drawer organizer, phone holder car, shoe organizer, cable organizer, water bottle accessory, baby organizer (sin salud), beauty tool. Agrupa por dominio de destino y luego por tipo de producto. Descarta retail (Amazon, Walmart, Target, Home Depot). Estima días con la fecha de inicio del anuncio más antiguo por dominio. Tope $2.
FASE B — AliExpress: para cada tipo, el equivalente funcional en AliExpress (precio, envío a US, nº de variantes, link, foto). Calcula landed % sobre el precio medio de los rivales. Si no encuentras genérico <$12, márcalo "sin genérico" pero no lo elimines.
FASE C — Anuncios y ángulos (Apify solo para los 10 finales, tope $2): para cada uno de los 10 tipos, los 3 anuncios MÁS ANTIGUOS del líder: fecha de inicio, días activo, formato (vídeo/imagen), primera frase del texto, link a la Biblioteca de Meta y, si el actor lo da, miniatura o link al vídeo. Marca "persona en pantalla: sí / no / verificar" según lo que puedas leer del anuncio. A partir de los textos, escribe 3 ÁNGULOS en una frase cada uno (qué problema vende, a quién, con qué gancho). Sin claims de salud.
FASE D — Semáforo simple por tipo (no es una recomendación, es un resumen): VERDE = pasa el filtro base y tiene genérico <$12 y persona en pantalla sí. AMARILLO = entró por escalera o le falta una cosa. GRIS = fuera de filtro (di cuál). No hay rojo: los rojos no entran en el visor.

ENTREGA: barridos/AAAA-MM-DD/visor.html, UN solo fichero sin dependencias externas, que se abra con doble clic. Una tarjeta grande por tipo, ordenadas VERDE → AMARILLO → GRIS y dentro por nº de anunciantes. Cada tarjeta tiene, en este orden y con letra grande: foto del genérico de AliExpress; nombre del tipo; semáforo y escalón con el que entró; tres números grandes: PRECIO RIVALES / PRECIO ALI / MARGEN BRUTO ESTIMADO (precio rivales − landed − $8 de envío estimado); nº de anunciantes y días del anuncio más antiguo; líder (dominio con link a su tienda); los 3 anuncios más antiguos con fecha, días, formato, primera frase y botón "Ver en la Biblioteca"; los 3 ángulos; link al genérico de AliExpress; y una caja "CHECK HUMANO" con 4 casillas que marco yo: [ ] lo entiendo en 5 s sin texto · [ ] sale una persona usándolo · [ ] no hay una marca conocida que ya venda esto en Walmart/Target · [ ] me lo compraría mi madre a $35. Arriba del visor: filtro por semáforo y por categoría, y el gasto real de Apify de este barrido leído del panel. Al terminar ejecuta: start barridos/AAAA-MM-DD/visor.html. Sin recomendación final: elijo yo mirando las tarjetas.
```

### 1.3 Reglas del barrido

- Un barrido = una sesión de Claude Code. No pegues otro prompt hasta tener el visor abierto.
- Si un comando pasa de 7 minutos, `ctrl+b` lo manda a segundo plano. No hagas `/clear` hasta tener el visor.
- Si Claude Code te dice "brand not found" en cadena o STT devuelve vacío en todas las categorías: vuelve al paso 0. No es el filtro.
- Si el visor sale con 10 tarjetas y todas GRIS: el filtro está bien, el problema es que STT no indexa lo que tocaste. Repite con el camino B una vez.

---

## Paso 2 — Elegir mirando el visor (10 minutos, no 3 días)

Abre las tarjetas VERDES primero. Para cada una:

1. Pulsa "Ver en la Biblioteca" en el anuncio más antiguo del líder. Un anuncio con 60+ días encendido es un ángulo que funciona. Míralo entero.
2. Marca las 4 casillas del CHECK HUMANO. **Tres o cuatro marcadas = candidato. Dos o menos = siguiente tarjeta.**
3. Abre la tienda del líder. Mira precio, si vende packs, cómo es su landing. Lo que hace mal es tu hueco (pack que no ofrece, demo que no enseña, landing fea).

Elige **UNO**. No dos, no tres. El que tenga más casillas y el margen bruto más alto. Si dudas entre dos, el que tenga el anuncio más antiguo del líder con más días.

Regla de oro: si después de mirar las 10 tarjetas ninguna tiene 3 casillas, no busques más ese día. Repite el barrido mañana con las 10 en EXCLUIDOS. Dos barridos seguidos con nada de 3 casillas → estás marcando por gusto, no por las casillas. Elige el mejor AMARILLO y testea igual. El objetivo de tu primer mes es haber testeado, no haber acertado.

---

## Paso 3 — Ficha de test y kill (antes de montar nada)

Rellena esto en un `.txt` con el producto elegido. Si no puedes rellenarlo entero, no montes la tienda.

```
PRODUCTO: 
PRECIO DE VENTA: $   (el de los rivales o $2-5 menos)
COSTE ALI + ENVÍO A US: $   (landed)
MARGEN BRUTO POR VENTA: $   (venta − landed − $8 de envío estimado − 3 % de pasarela)
BREAKEVEN: gasto máximo por compra = margen bruto. Si el margen es <$15, no testees este producto.
ÁNGULO 1 (copiado del anuncio más antiguo del líder, con tus palabras):
ÁNGULO 2 (el hueco que le viste al líder):
ÁNGULO 3 (el que se te ocurra a ti):
ANUNCIOS: 3 vídeos, uno por ángulo, 15-30 s, persona usando el producto en los primeros 2 s.
PRESUPUESTO DEL TEST: $150 en total. $30-40/día. Una campaña, US, sin segmentar.
```

**Kill (se cumple, se para, sin negociar):**
- Día 2: si ningún anuncio tiene CTR >1 % → pausa ese anuncio. Si los tres están por debajo → kill del producto.
- Día 3: si hay clics pero cero añadidos al carrito → landing o precio. Cambia una cosa (precio −$5 o foto principal) y da 1 día más.
- Día 4 o $150 gastados, lo que llegue antes: sin ninguna venta → **kill**. Con 1-2 ventas y coste por compra por debajo del margen bruto → sigue 3 días más con el mismo presupuesto.
- Nunca subir presupuesto en el test. Nunca añadir un cuarto anuncio en el test.

Un producto muerto entra en EXCLUIDOS del siguiente barrido. Anota en una línea por qué murió (sin clics / sin carritos / sin ventas). A los tres productos muertos ya sabes leer un test, que es lo que vale.

---

## Resumen en cinco líneas

1. Prueba de vida en verde o no hay barrido.
2. Un prompt, un visor, 10 tarjetas, siempre.
3. Elige UNO con 3-4 casillas del check humano.
4. $150, 3 anuncios, 4 días, kill escrito antes de empezar.
5. Muerto → excluidos → siguiente barrido. Testear es el objetivo; acertar viene después.

---

## v2 (1-oct-2026) — Economía primero. Sustituye el filtro de la §1.1 donde choque

Lecciones de 4 barridos R (29-sep a 1-oct) que dieron 0 verdes reales:
- El precio de AliExpress que devuelve la búsqueda es de **nuevo usuario**: la olla salía a $6,33 y el real era $10,02. Con ese error se pintó un verde falso.
- «Días activo» no valida: hay anuncios de 32 días con 195 personas de alcance y $1,80 de gasto (tiendas-catálogo que dejan anuncios encendidos sin presupuesto).
- Ticket $20–45 + genérico ≤25 % + $8 de envío + margen ≥$15 casi no existe: con genérico real de $8–12 hace falta vender a **$35 o más**.
- Casi todo lo que STT enseña a $13–20 es la red mindsparkl/bisnftwrem/perpetualing/thegiftnorth (misma foto, mismo texto): enjambre, no validación.

**Orden nuevo (script `tools/barrido_eco.py`, candidatos en `candidatos.json`):**
1. Genérico AliExpress: 3 más vendidos que contengan las palabras del tipo → **precio real leyendo la ficha** (navegador de Apify, ~$0,0025). Se elige el equivalente funcional (mismas piezas que el pack del rival), no el más barato.
2. Precio de rivales: fichas Shopify de los anunciantes de la Biblioteca (Apify).
3. **Margen = mediana de rivales − Ali real − envío (8; 10 si pesa) − 3 %. Si <$15 → GRIS y se para ahí** (no se gasta más en ese tipo).
4. Ancla Amazon (Apify): mínimo con ≥50 reseñas <70 % de la mediana de rivales → aviso.
5. Biblioteca: 3–8 anunciantes con ≥21 d (redes gemelas unidas), **el líder** con ≤120 d (no el anuncio más antiguo del tipo), tiendas nuevas <21 d ≥5 → aviso «enjambre».
6. Persona en pantalla: clasificación del creativo en STT (`search_ads` / `get_ad`: formato UGC/demo/talking-head con avatar) o vista del fotograma. Sin verificar → no hay verde.

**Fuente de candidatos:** `search_ads` de STT en US (21–120 d, formatos ugc/demo/talking-head) ordenado por variaciones y rango del anuncio; el «gasto» de STT es alcance UE/UK (Meta no publica gasto de US): sirve para descubrir, no para validar. Priorizar tipos que los rivales venden a $35–70 o en pack de 2–3.

VERDE = margen ≥$15 con precios reales + Amazon ok + 3–8 anunciantes ≥21 d + líder ≤120 d + persona «sí». AMARILLO = margen ok y falla una. GRIS = margen <$15.

### Resultado del primer barrido v2 (1-oct, `barridos/2026-10-01-ECO/eco.json`, Apify $0,31)
12 candidatos con ticket alto, precios reales: **0 verdes**. 5 mueren por margen (tabla de cortar $14,66, proyector $6,47, plancha, aro de pilates $14,51, cadena de lluvia $2,17 con el genérico real de $19,89). Los que tienen margen (disuasor de ladridos, barra de pilates, rulo sin calor, banda de pedal, apliques, rueda abdominal) los tumba **Amazon**: el mismo producto a $4,99–16,99 con miles de reseñas (rulo CORATED $4,99 con 18.900 reseñas; disuasor $19,99 con 2.300), o solo 1–2 anunciantes.
**Lección:** en commodity de hogar/fitness el filtro que manda es el ancla de Amazon. Siguiente barrido: invertir el orden → buscar primero en Amazon US productos con precio ≥$30 y ventas altas («bought in past month») cuyo genérico real en AliExpress cueste ≤$10, y solo entonces mirar anunciantes en Meta.
