---
name: barridos-searchthetrend
description: Barridos de producto para dropshipping con SearchTheTrend (MCP) + Apify desde Claude Code, con el filtro de validación por ESCALA (≥3 anunciantes escalando) y entrega en un visor HTML para que el usuario elija mirando los anuncios. Úsala cuando el usuario quiera buscar producto nuevo, "hacer un barrido", "pasar por searchthetrend", buscar candidatos por momentum/Q4, por línea de producto (mismo comprador), por familia (seguridad, hogar) o por nichos apasionados; o cuando pida "el visor", "la ficha" o quiera modificar un barrido anterior.
---

# Barridos de producto con SearchTheTrend + visor

Método de una sesión real (24–26 sep 2026). Cuatro barridos, un filtro, un visor. El objetivo NO es que Claude recomiende: es que el visor te ponga delante los datos y los anuncios de los rivales y **tú decidas mirando**. Claude filtra números; el ojo lo pones tú.

## 0. Qué necesitas antes (una vez)

1. **Claude Code** instalado y una carpeta de trabajo, p. ej. `C:\Proyectos\product-radar\`.
2. **SearchTheTrend (STT)** conectado como MCP en scope user. Ver `references/setup.md`. Comprobación: dentro de `claude`, escribe `/mcp` → `searchthetrend · Connected`.
3. **Apify** con un actor de Meta Ads Library y la clave en `.env`. Ver `references/setup.md`. Fija un **límite mensual en Apify → Settings → Usage** (los scripts se equivocan; el límite de la cuenta no).
4. Si la carpeta está vacía, el primer prompt de `references/setup.md` construye el pipeline (scripts de fase A/B/C + generador del visor). Después, los barridos lo reutilizan.

Para entrar (PowerShell):
```
cd C:\Proyectos\product-radar
claude
```
Espera al prompt de Claude Code (deja de salir `PS C:\...>`) y **entonces** pega el barrido entero. Error típico: hacer el `cd` y pegar el prompt en PowerShell sin arrancar `claude`. Atajo: `notepad $PROFILE` → añade `function radar { Set-Location C:\Proyectos\product-radar; claude }` → a partir de la siguiente ventana escribes `radar`.

## 1. El filtro (sustituye al de "poca competencia")

Antes se buscaba "≤20 ads y un anunciante con ≥5". Los dos últimos productos que pasaron ese filtro murieron; el que dio dinero salió de una marca escalando a lo grande. Conclusión: **el unicornio por sistema es perdedor. Entra donde ya hay tres o más ganando y gana por ejecución.**

| Criterio | Regla | Qué hace |
|---|---|---|
| **Escala** | ≥3 anunciantes distintos con ≥30 días anunciando el mismo TIPO de producto en US, y al menos uno con ≥15 ads activos **o** serie semanal de `adsFound` creciendo en las últimas 8 semanas | Filtra. Un solo superviviente no valida, ni con 13 meses |
| **Mercado** | US ≥50 % de los anuncios | Filtra |
| **Ticket** | PVP $15–40 | Filtra |
| **Genérico** | equivalente funcional en AliExpress <$10; landed ≤18 % del PVP deseable, 25 % techo | Filtra (el landed lo baja tu agente después; en STT solo se estima) |
| **Producto** | sin claims médicos, sin suplementos/ingeribles, sin electrónica compleja (ni Bluetooth, ni LED, ni resistencias), sin tallas/modelos (1–3 SKUs), demo visual en 5 s, packs posibles | Filtra |
| **Gate de dropshippers del genérico** | ≤2 → PRIORIDAD · 3–5 → POSIBLE · ≥6 → KILL (contado en la Biblioteca de Meta) | Filtra |
| **Hueco de ejecución** | rivales sin packs, demo floja, landings sucias, ángulo obvio sin usar | **Se anota, no filtra.** Es lo que tú miras en el visor para elegir |
| Amazon como techo | descartado como criterio (descartaba demasiado). Se mira a mano en los finalistas: si el genérico Prime está a un tercio de tu PVP, cuidado | Manual |

Regla de dinero: **tope Apify por barrido $3** y se lee el gasto real del panel de Apify, no del script. STT pre-filtra gratis; Apify solo entra cuando STT deja dudosos.

## 2. Los cuatro barridos (prompts en `references/prompts.md`)

Todos comparten pipeline y filtro; cambia la **pregunta**:

| Barrido | Pregunta | Cuándo usarlo |
|---|---|---|
| **A — Escala general** | ¿Qué tipos de producto tienen ≥3 anunciantes escalando ahora en hogar/cocina/baño/auto/jardín/outdoor/herramientas/bebé/belleza/viaje? | Primer barrido, o cuando no tienes dirección |
| **B — Momentum + línea** | Parte A: ¿qué marcas han crecido ≥50 % en anuncios activos en las últimas 4 semanas? (lo que alguien escala *ahora* = Q4). Parte B: ¿qué segundo producto compra el mismo cliente de mi producto vivo? | Tienes un producto en test y quieres recámara Q4 o upsell |
| **C — Familia de producto** | ¿Qué otros productos comparten comprador y motivación con el que ya vende (p. ej. seguridad familiar tras un rompecristales)? Añade columnas "marca de referencia en la cabeza del comprador" y "regalo Q4" | Tienes una venta real y quieres explotar el mismo comprador |
| **D — Nichos apasionados** | ¿Qué venden a aficionados (camping, pesca, caza, RV, DIY, BBQ, huerto, golf, jeep, moto, caballos…)? Columnas extra: marca de referencia, regalo Q4, comprador (aficionado vs pareja que regala) | Cuando STT no indexa tu vertical o quieres Q4 con comprador que no compara |

Y un **mini-check** de $0,30 para un tipo suelto que te haya llamado la atención (también en `references/prompts.md`).

## 3. Anatomía del prompt (para que lo modifiques)

Cada prompt tiene los mismos bloques. Cambia el bloque, no el resto:

1. **Cabecera**: nombre del barrido y fecha, tope Apify, carpeta de salida (`barridos/AAAA-MM-DD/`), "reutiliza los scripts". → Cambia fecha y tope.
2. **FILTRO**: el de la tabla de arriba. → Si aflojas algo (p. ej. ticket $15–60), hazlo aquí y en ningún otro sitio.
3. **EXCLUIDOS**: todo lo ya fichado o probado. → Añade cada producto que descartes; si no, Claude te lo vuelve a sacar.
4. **FASE A — Candidatos (STT, $0)**: `search_brands` ordenado por meta_ads y `search_products` con `minDaysRunning=30` y `countries=US`, por subnicho. **Agrupa por TIPO de producto, no por tienda** (una toalla de secado con 4 tiendas es un tipo con 4 anunciantes). Guarda `tipos.csv`. → Cambia la lista de subnichos/verticales.
5. **FASE B — Genérico**: para cada tipo, equivalente en AliExpress (precio, envío US, SKUs) y recuento de dropshippers del genérico en la Biblioteca (gate). Apify solo si STT deja dudas. → No tocar salvo el tope.
6. **FASE C — Ficha**: tipo, nº anunciantes, líder (dominio, días, ads, tendencia), PVP medio de rivales, genérico Ali (precio, link), gate, hueco de ejecución observado, y los **3 anuncios más antiguos del líder** con link a la Biblioteca. → Aquí añades columnas ("regalo Q4", "marca de referencia", "comprador", "ventana en semanas", "3 anuncios más recientes").
7. **ENTREGA**: `visor.html`, un solo fichero sin dependencias, tarjeta por tipo, filtros por subnicho y gate, pestañas si hay varias partes, `start visor.html` al terminar, gasto real de Apify del panel, **"Sin recomendación: elijo yo mirando los anuncios"**. → Cambia pestañas y orden (por nº de anunciantes, por crecimiento, por días).

## 4. Cómo leer el visor (`references/leer-visor.md` tiene el detalle y casos reales)

Orden de lectura por ficha:
1. **Gate y "firme/no firme"**: KILL se ignora. "No firme" = el genérico no está verificado; cuenta como duda.
2. **Anunciantes y líder**: ¿es una marca DTC con demanda real o 5 tiendas genéricas que entraron la misma semana? Lo segundo es un **enjambre** copiándose un anuncio, no demanda: en 3 semanas estarán a 0 o a 15.
3. **Los 3 anuncios más antiguos del líder**: un vídeo con 300 días encendido y 2 variaciones es un creativo que ha pagado una temporada entera → ángulo probado. Ábrelos en la Biblioteca y mira qué venden (dolor, formato, precio, packs).
4. **Marca de referencia en la cabeza del comprador**: si existe "la de Amazon/Walmart" (Addalock, Slime, Turtle Wax, Car Cane As Seen On TV) el creativo tiene que responder "¿por qué a ti y no a ellos?". Si no puede, fuera.
5. **Commodity**: si el producto pasa el filtro numérico pero se ve por $3 en el Dollar Tree (ganchos, cinta, bayeta), no hay hueco posible; el margen bonito es una trampa.
6. **Electrónica disfrazada**: linterna LED, Find My, resistencia → fuera aunque STT lo marque PRIORIDAD.
7. **Hueco de ejecución**: packs que nadie hace, demo que nadie enseña, landing sucia, ángulo obvio sin usar. Esto es lo que decide entre los que pasan.

Salida de un barrido: **2–3 tipos** que te llamen. Con ellos se hace la ficha de decisión (breakeven por pack, ángulo, mensaje al agente) antes de montar nada. Cero de diez también es un resultado válido: STT no indexa todos los verticales (seguridad, por ejemplo).

## 5. Reglas operativas

- Un barrido = una sesión de Claude Code. No metas otro prompt hasta que entregue el visor.
- Si el Bash pasa de 7 min, `ctrl+b` lo manda a segundo plano; no hagas `/clear` hasta tener el resumen.
- Autopsia con datos: pide el resumen completo pegado y relee los números; no te fíes del veredicto de Claude ("Code lo tumba por $0,96 de ticket" es una formalidad, no un motivo).
- Cada producto descartado va a EXCLUIDOS del siguiente prompt.
- **Kill del research**: barrido sin ningún tipo con escala + hueco → no se fuerza; se cambia la pregunta (otro de los cuatro barridos) o se vuelve al producto que ya vende. Un producto que vende vale más que tres que igual venden.

## Referencias
- `references/prompts.md` — los cuatro barridos + mini-check, para pegar tal cual.
- `references/leer-visor.md` — campo a campo del visor y lecturas reales de la sesión (qué se descartó y por qué).
- `references/setup.md` — MCP de STT, Apify, y prompt para construir el pipeline si la carpeta está vacía.
