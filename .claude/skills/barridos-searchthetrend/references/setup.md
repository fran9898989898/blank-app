# Setup: STT (MCP), Apify y pipeline `product-radar`

## 1. SearchTheTrend como MCP (una vez, scope user)

Plan recomendado: **STT Pro (~$49/mes)**; el trial de $1 sirve para probar el feed, no para el protocolo. Los créditos se gastan por consulta: un barrido grande puede consumir ~un tercio de la cuota mensual, por eso STT se usa para pre-filtrar y no para explorar sin criterio.

1. searchthetrend.com → cuenta → API / MCP → generar Bearer token.
2. PowerShell:
```
claude mcp add --transport http searchthetrend https://www.searchthetrend.com/api/mcp --header "Authorization: Bearer TU_TOKEN" -s user
```
3. `claude` en cualquier carpeta → `/mcp` → `searchthetrend · Connected`.

**Fallo típico**: cambias de token y Code sigue con el viejo. El viejo quedó en scope local (por carpeta) y manda sobre el user:
```
claude mcp list
claude mcp get searchthetrend
claude mcp remove searchthetrend -s local
claude mcp add --transport http searchthetrend https://www.searchthetrend.com/api/mcp --header "Authorization: Bearer TOKEN_NUEVO" -s user
```
Repite el `remove -s local` en cada carpeta donde se hubiera añadido. Reinicia `claude`.

Otros: `Login expired · /login` es la sesión de Anthropic, no el MCP. Error de cuota del MCP → parar y mirar el plan.

Herramientas que usan los barridos (los nombres exactos pueden cambiar; pide a Code que las liste con `/mcp` al empezar): `search_brands` (ordenar por meta_ads, filtrar US), `search_products` (`minDaysRunning=30`, `countries=US`), `search_ads` (sort `start_date`), serie semanal `adsFound` por marca, `myshopifyDomain` para colapsar tiendas gemelas, `request_brand_scan` para clasificar dropshipper vs marca (ilimitado en Pro; en planes inferiores gasta 300 créditos → solo con autorización).

Limitación conocida: STT no indexa marcas grandes de retail ni todos los verticales (seguridad, suplementos de marca). Sesgo hacia operadores medianos de Shopify. Un cero en un vertical puede ser sesgo de la herramienta, no ausencia de mercado.

## 2. Apify

1. Cuenta en apify.com → Settings → Integrations → API token → guárdalo en `C:\Proyectos\product-radar\content\.env` como `APIFY_TOKEN=...`.
2. **Settings → Usage → límite mensual** (p. ej. $15). Es el único freno que un script con un bug no se salta. En una sesión anterior un error de cálculo gastó $16 en una corrida.
3. Actor: busca "facebook ads library scraper" en Apify Store; deja que Code elija y lo configure. Se usa para contar operadores (dominios distintos, ≥30 días) por consulta de la Biblioteca, unos 30 anuncios por consulta. Coste real: se lee del panel de Apify después de cada barrido, no del script.

Regla: STT pre-filtra gratis. A Apify solo van tipos con ≤5 anunciantes según STT (los ≥6 se marcan KILL con la cifra de STT sin gastar).

## 3. Construir el pipeline si la carpeta está vacía

Pega esto en Claude Code dentro de `C:\Proyectos\product-radar` (con `.env` ya creado). Después, los barridos de `prompts.md` reutilizan estos scripts.

```
Construye en esta carpeta un pipeline de barridos de producto para dropshipping en US. Lee la clave de STT y de Apify desde content/.env. STT está conectado como MCP (lista sus herramientas y úsalas). No me pidas mirar nada a mano hasta el visor.

Estructura:
- barrido_a.py — FASE A (STT, $0): dado un listado de subnichos/verticales, search_brands ordenado por meta_ads con US ≥50 % y search_products con minDaysRunning=30 y countries=US. Agrupar resultados por TIPO DE PRODUCTO (función, no tienda; colapsar tiendas gemelas por myshopifyDomain). Por tipo: nº anunciantes distintos ≥30 días, líder (dominio, días, ads activos), serie semanal de adsFound del líder, tendencia (media últimas 4 semanas vs media semanas 5-8; crecimiento %). Aplicar validación por ESCALA (≥3 anunciantes ≥30 d y uno con ≥15 ads o serie creciendo). Guardar tipos.csv en barridos/<fecha>/.
- barrido_b.py — FASE B: por tipo, buscar el equivalente funcional en AliExpress (precio, envío a US, nº SKUs, link) y calcular landed % sobre el PVP medio de los rivales. Contar dropshippers del genérico en la Biblioteca de Meta con el actor de Apify (30 anuncios por consulta, operadores = dominios distintos con ≥30 días). Gate: ≤2 PRIORIDAD · 3-5 POSIBLE · ≥6 KILL. Marcar "firme" si el genérico está verificado y "no firme" si no. Pre-filtrar por STT: si STT ya da ≥6 anunciantes, KILL sin Apify. Tope de gasto por barrido configurable (por defecto $3): parar al alcanzarlo y decirlo.
- barrido_c.py — FASE C: ficha por tipo con: tipo, subnicho, anunciantes, líder (dominio, días, ads, tendencia y serie), PVP medio de rivales (leído de la tienda Shopify: /products.json), genérico Ali (precio, link, landed %), gate y firmeza, hueco de ejecución observado (packs / demo / landing / ángulo), 3 anuncios más antiguos del líder (fecha, días, formato, variaciones, texto, link a la Biblioteca) y, si se pide, 3 más recientes. Columnas opcionales por parámetro: estacionalidad Q4, ventana (semanas), marca de referencia (sí/no), regalo Q4 (sí/no), comprador.
- visor.py — genera barridos/<fecha>/visor.html: UN fichero sin dependencias externas, tarjeta por tipo, pestañas por parte del barrido si las hay, filtros por subnicho y gate, orden configurable (anunciantes / crecimiento / días del líder), textos de los anuncios y botón a la Biblioteca para cada anuncio, gasto de Apify del barrido. Al terminar ejecuta start visor.html.
- Un README corto con cómo lanzar cada fase y el formato de EXCLUIDOS (lista de tipos que no se vuelven a evaluar).
Sin recomendación en el visor: yo elijo mirando los anuncios.
```

Una vez construido, cada barrido de `prompts.md` empieza con "Reutiliza barrido_a*.py, b*.py, c.py" y solo cambia la pregunta.

## 4. Atajos de PowerShell

`notepad $PROFILE` → añade:
```
function radar { Set-Location C:\Proyectos\product-radar; claude }
```
Guarda, cierra, abre PowerShell nuevo, escribe `radar`.

## 5. Higiene de sesión

- Un barrido por sesión de Code. Dos sesiones abiertas = dos colas; apunta cuál tiene qué.
- Bash con timeout de 10 min: si pasa de 7, `ctrl+b` lo manda a segundo plano.
- No hagas `/clear` hasta tener el resumen del barrido pegado. Retomar: `claude --continue`.
- Cada producto probado o descartado entra en EXCLUIDOS del siguiente prompt.
