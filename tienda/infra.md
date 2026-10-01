# Infraestructura de tienda — estado verificado 1-oct-2026

Fuentes: Gmail (francasge@gmail.com) y lectura pública de fluidxtract.com. Sin acceso a admin de Shopify, Meta
Business ni Cloudflare desde esta sesión: lo que depende de esos paneles queda como "no verificable".

| Pieza | Estado | Evidencia |
|---|---|---|
| Dominio fluidxtract.com | Registrado | Email Cloudflare "Domain registered" 19-sep |
| Dominio → Shopify | Conectado | fluidxtract.com sirve la tienda "My Store 4" (lectura 1-oct) |
| Tienda Shopify | Creada, CERRADA con contraseña ("Opening soon") | Lectura 1-oct; facturas €1 "Mi tienda 3"/"My Store 4" 11-sep; recordatorios de lanzamiento hasta 30-sep |
| Nombre de tienda | "My Store 4" (genérico) | Lectura 1-oct |
| Plan de pago | No verificable (trial de €1 iniciado 11-sep) | Facturas Shopify |
| Shopify Payments | Sin configurar (Shopify recuerda activarlo) | Emails Shopify hasta 30-sep |
| Píxel de Meta | No verificable (la página de contraseña no lo expone); 0 emails de Meta Business | Gmail |
| CAPI | No verificable; requiere app "Facebook & Instagram" de Shopify conectada | — |
| Verificación de dominio en Meta | Sin evidencia | — |
| Políticas | Preparadas en tienda/politicas/ (pendiente rellenar [CORCHETES]) | Este commit |
| TankFresh | Sin rastro en Gmail ni en el repo | Gmail |
| FluidVac | Idea de producto (extractor de fluidos, referencia cozyllio.com); el dominio fluidxtract.com es para ella | Email "Así encontré fluidvac" |

## Falta (en orden) — lo haces tú en los paneles; yo no tengo acceso
1. Datos legales para las políticas: nombre legal, dirección, email de soporte, jurisdicción.
2. Decidir el dominio: fluidxtract.com es de extractor de fluidos; para una banda de ejercicio no encaja. Opción barata: tienda general con nombre neutro.
3. Shopify: elegir plan, activar Shopify Payments (o PayPal), impuestos US, zonas de envío US/CA con la tarifa de la política.
4. Pegar las 4 políticas (Ajustes → Políticas) y enlazarlas en el pie.
5. Meta: Business Manager → píxel → app "Facebook & Instagram" de Shopify (conecta píxel + CAPI en "Máximo") → verificar dominio (registro TXT en Cloudflare).
6. Banner de cookies (Ajustes → Privacidad del cliente).
7. Quitar la contraseña solo cuando haya producto, políticas y un pedido de prueba hecho.

## Prohibido en la tienda
- Reseñas que no vengan de compras reales (ni importadas de Amazon/Ali ni generadas).
- Toasts de "X acaba de comprar", contadores "41 personas viendo esto", temporizadores que se reinician.
- Suscripciones escondidas en el checkout.
