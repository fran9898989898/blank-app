# Prompts de barrido — pegar tal cual en Claude Code (carpeta `product-radar`)

Sustituye la fecha, la carpeta de salida y la lista de EXCLUIDOS por las tuyas. Todo lo demás se puede pegar tal cual. Si es tu primer barrido y no existen los scripts `barrido_a*.py / b*.py / c.py`, quita la frase "Reutiliza…" y Claude Code los creará (ver `setup.md`).

---

## Barrido A — Escala general (primer barrido / sin dirección)

```
Barrido de producto nuevo con filtro de validación por ESCALA. Reutiliza product-radar (STT por MCP con la clave de content/.env, actor Apify de la Biblioteca de Meta). Tope Apify $3. Carpeta de salida: barridos/AAAA-MM-DD/.

FILTRO:
- Validación por ESCALA: ≥3 anunciantes distintos con ≥30 días anunciando el mismo tipo de producto en US, y al menos uno con ≥15 ads activos o serie semanal de adsFound creciendo en las últimas 8 semanas (STT).
- USA mercado dominante (≥50 % de los anuncios).
- Ticket $15-40. Genérico funcional en AliExpress <$10 (landed ≤18 % del PVP deseable, 25 % techo).
- Sin claims médicos, sin suplementos/ingeribles, sin electrónica compleja, sin tallas/modelos (cabe en 1-3 SKUs), demo visual en 5 s, packs posibles.
- Hueco de ejecución (se anota, no filtra): rivales sin packs, demo floja, landings DS con guarradas, ángulo obvio sin usar.

EXCLUIDOS (no volver a evaluar): <lista de todo lo que ya has probado o descartado>.

FASE A — Candidatos (STT, $0): en subnichos de hogar, cocina, baño, garaje/auto, jardín, outdoor, herramientas, bebé/niños (sin salud), belleza sin claims, viaje: search_brands por meta_ads y search_products con minDaysRunning=30 y countries=US. Agrupa por TIPO DE PRODUCTO (no por tienda): para cada tipo, nº de anunciantes distintos ≥30 días, el de más ads activos, días del más antiguo, serie semanal del líder. Quédate con los tipos que pasen la validación por escala. Guarda tipos.csv.
FASE B — Genérico (Apify solo si hace falta, $0 preferente): para cada tipo, buscar el equivalente funcional en AliExpress (precio, envío US, 1-3 SKUs) y contar dropshippers del genérico en la Biblioteca (gate: ≤2 PRIORIDAD · 3-5 POSIBLE · ≥6 KILL). Pre-filtra por STT antes de gastar.
FASE C — Ficha de los 10 mejores: tipo, anunciantes, líder (dominio, días, ads, tendencia), PVP medio de los rivales, genérico Ali (precio, link), gate, hueco de ejecución observado (packs/demo/landing/ángulo), y los 3 anuncios más antiguos del líder con link a la Biblioteca.
ENTREGA: barridos/AAAA-MM-DD/visor.html (un fichero, sin dependencias): tarjeta por tipo ordenada por nº de anunciantes, con todo lo anterior, textos de los anuncios y botón a la Biblioteca para ver el creativo; filtros por subnicho y gate. Al terminar: start visor.html. Gasto real de Apify leído del panel. Sin recomendación: elijo yo mirando los anuncios.
```

---

## Barrido B — Momentum (Q4) + línea de producto del mismo comprador

Úsalo cuando tienes un producto vivo y quieres (a) lo que se está escalando AHORA y (b) el segundo producto natural. Sustituye "MI PRODUCTO" y la lista de la parte B por tu categoría.

```
Barrido AAAA-MM-DD, dos partes, mismo filtro de ESCALA (≥3 anunciantes ≥30 días, uno con ≥15 ads o serie creciendo; US ≥50 %; ticket $15-40; genérico Ali <$10; sin claims, sin electrónica, sin tallas; demo 5 s; packs). Reutiliza barrido_a*.py, b*.py, c.py. Tope Apify $3. Salida en barridos/AAAA-MM-DD/. Excluidos: todo lo de barridos anteriores más los tipos ya fichados.

PARTE A — MOMENTUM (todos los nichos): en STT, marcas Shopify con US ≥50 % cuya serie semanal de adsFound haya crecido ≥50 % entre la media de hace 8-5 semanas y la de las últimas 4 (mínimo 10 ads activos hoy). Agrupa por tipo de producto como en la fase A. Para cada tipo que pase el filtro, añade dos columnas: "estacionalidad Q4" (sí/no y por qué: regalo, invierno, frío, fiestas) y "ventana" (semanas hasta el pico). Ordena por crecimiento del líder.

PARTE B — LÍNEA <MI CATEGORÍA> (solo <categoría>, sin electrónica): <lista de 8-10 tipos de producto que compra el mismo cliente de MI PRODUCTO>. Mismo pipeline; si algún tipo cae por landed, busca genérico alternativo que lo baje por debajo del 25 %. Marca cuáles comparten comprador con MI PRODUCTO y cuáles son upsell natural post-compra.

ENTREGA: visor.html con dos pestañas (Momentum / Línea), misma ficha de siempre (líder, serie, PVP rivales, genérico Ali, gate, hueco, 3 anuncios más antiguos con link a la Biblioteca). Gasto real de Apify del panel. Sin recomendación.
```

Ejemplo real de la parte B (producto vivo: coating cerámico de coche): `drying towel, wheel & tire cleaner, tire shine, headlight restoration, scratch/swirl remover, interior/dash cleaner, glass cleaner/rain repellent, foam cannon manual, microfiber sets, clay bar/mitt`.

**Complemento para momentum** (los 3 anuncios más antiguos dicen qué les funciona desde hace un año; faltaba ver qué están probando ahora):

```
barridos/AAAA-MM-DD: en la pestaña Momentum añade a cada ficha, junto a los 3 anuncios más antiguos, los 3 anuncios MÁS RECIENTES del líder (STT search_ads, sort start_date desc), con fecha, formato, texto y link a la Biblioteca. Regenera visor.html.
```

---

## Barrido C — Familia de producto (mismo comprador que una venta real)

Úsalo cuando un producto ya te ha dado compras y quieres explotar la misma motivación de compra. Ejemplo real: tras un rompecristales con ventas, la familia "seguridad familiar, sin marca en la cabeza del comprador".

```
Barrido AAAA-MM-DD, "<nombre de la familia>", mismo filtro de ESCALA (escala, US ≥50 %, ticket $15-40, Ali <$10, sin claims, sin electrónica, demo 5 s, packs). Tope Apify $2. Salida barridos/AAAA-MM-DD/. Tipos a validar, mismo comprador que <MI PRODUCTO CON VENTAS>: <lista de 8-12 tipos>. Para cada tipo: anunciantes ≥30 días, líder y serie, PVP medio, genérico Ali, gate por dropshippers (STT + Biblioteca si dudoso), hueco de ejecución, y dos columnas nuevas: "marca de referencia en la mente del comprador" (sí/no: ¿existe una marca que el comprador ya conozca en Amazon/Walmart para esto?) y "regalo Q4" (sí/no). Ficha al visor, sin recomendación.
```

Lista real usada: `fire blanket (cocina/coche), portable door lock (viaje/hotel), door security bar, emergency escape ladder, tire repair plug kit, car emergency kit sin electrónica, window breaker infantil, seatbelt cutter suelto, first aid kit compacto, whistle/emergency keychain`. Resultado: 0 de 10 (STT casi no indexa el vertical; en la Biblioteca lo que hay son marcas de retail). Un cero también es información.

---

## Barrido D — Nichos apasionados (regalo de la pareja al aficionado)

```
Barrido AAAA-MM-DD "nichos apasionados USA". Mismo filtro de ESCALA (≥3 anunciantes ≥30 días, uno con ≥15 ads o serie creciendo; US ≥50 %; ticket $15-40; Ali <$10; sin claims, sin electrónica, sin tallas; demo 5 s; packs). Tope Apify $3. Salida barridos/AAAA-MM-DD/. Excluidos: todo lo ya fichado.
Verticales: camping, pesca, caza, RV/autocaravana, DIY/herramientas de garaje, carpintería, BBQ/grill, jardín/huerto, gallinas/homestead, golf, ciclismo, barcos, jeep/offroad, moto, caballos. Amplía tú con 5-10 verticales más de hobby apasionado en US que STT tenga subnichos poblados; dilo en el informe.
Fase A por STT: search_brands por subnicho sort meta_ads + search_products minDaysRunning 30, agrupa por tipo. Fase B: genérico Ali y gate por dropshippers. Fase C: ficha del visor igual que siempre, más tres columnas: "marca de referencia en la mente del comprador" (sí/no), "regalo Q4" (sí/no; el comprador de estos nichos recibe regalos de su pareja en Navidad), y "comprador" (el propio aficionado / la pareja que regala). Visor con pestañas por vertical; sin recomendación.
```

Ángulo al abrir el visor: el regalo de la pareja al aficionado es el comprador de Q4 que menos compara (no sabe lo que vale una cosa de pesca).

---

## Mini-check de un tipo suelto (~$0,30)

Cuando un producto te llama la atención fuera del barrido:

```
barridos/AAAA-MM-DD: añade el tipo "<nombre en inglés del producto>". Biblioteca «<query 1>» + «<query 2>» (30 anuncios cada una), operadores ≥30 días, líder, PVP, genérico Ali (versión SIN electrónica si existe), gate, marca de referencia (¿existe una marca original conocida en Amazon?), regalo Q4. Ficha al visor.
```

Ejemplo real: car cane / asa de coche para mayores → "Original Car Cane" de Emson (As Seen On TV) en Amazon + solo 2 anunciantes con 30 días → fuera.

---

## Bloques que puedes cambiar sin romper nada

- **Ticket**: `$15-40` → lo que quieras, pero recuerda que <$15 no paga el CPA de Meta y >$40 exige más trust en la landing.
- **Subnichos/verticales** de la fase A: cualquier lista. Cuanto más concreta, mejor agrupa STT.
- **Columnas extra** de la fase C: añade las que te ayuden a decidir ("¿lo venden en Walmart?", "¿pesa >1 kg?", "¿temporada?").
- **Orden del visor**: por anunciantes (madurez), por crecimiento (momentum), por días del líder (antigüedad).
- **Tope Apify**: $2–3. No lo subas "para ver más": sube el filtro de STT primero.
- **Lo que NO cambies**: "agrupa por TIPO, no por tienda", "gate por dropshippers", "3 anuncios más antiguos con link a la Biblioteca", "sin recomendación". Son lo que te permite decidir tú.
