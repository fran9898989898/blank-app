# Cómo leer el visor (campo a campo) y lecturas reales

El visor es un `visor.html` en `barridos/<fecha>/`. Una tarjeta por tipo de producto, con filtros por subnicho y gate, y pestañas si el barrido tenía partes. Se abre con `start visor.html` desde la carpeta (o doble clic).

## Campos de la tarjeta

| Campo | Qué es | Cómo se lee |
|---|---|---|
| **Tipo** | El producto agrupado por función, no por tienda | Si dos tipos son el mismo producto con otro nombre, júntalos mentalmente |
| **Anunciantes (≥30 d)** | Nº de tiendas distintas con ≥30 días anunciando ese tipo en US | ≥3 = hay demanda. 1 = un superviviente, no valida. 5 que entraron la misma semana = enjambre (ver abajo) |
| **Líder** | Dominio con más ads activos: días, nº ads, tendencia (serie semanal) | Marca DTC con muchos ads y meses = categoría real. Dropshipper con 60 ads y 190 días = el genérico vende con Meta |
| **Serie semanal** | `adsFound` por semana (STT) | Creciendo = está escalando ahora. Plana alta = madura. Cayendo = se apaga |
| **PVP medio rivales** | Precio de los competidores (desde su Shopify) | Fija tu techo de precio y tu pack. "NO VERIFICABLE" = la tienda no deja leer precios; míralo a mano |
| **Genérico Ali** | Precio, envío US, link, SKUs | El landed real lo da tu agente; esto es la primera estimación. "No firme" = no verificado |
| **Landed %** | genérico / PVP | ≤18 % deseable, 25 % techo. 46 % = pedirle al agente alternativa antes de descartar |
| **Gate** | Dropshippers del genérico en la Biblioteca: ≤2 PRIORIDAD · 3–5 POSIBLE · ≥6 KILL | KILL no se mira. PRIORIDAD "no firme" es una duda, no un sí |
| **Hueco de ejecución** | Lo que los rivales hacen mal: packs, demo, landing, ángulo | Es tu criterio de entrada entre los que ya escalan |
| **3 anuncios más antiguos del líder** | Fecha inicio, días, formato, variaciones, texto, botón a la Biblioteca | Un vídeo con 300 días y 2 variaciones = creativo que ha pagado una temporada. Ábrelo: dolor, demo, precio, pack |
| **3 anuncios más recientes** (momentum) | Lo que el líder está probando este mes | Ángulo nuevo + temporada arrancando |
| **Marca de referencia** (C, D) | ¿Existe "la de Amazon/Walmart" para esto? | Sí = tu creativo tiene que responder "¿por qué a ti?". Si no puede, fuera |
| **Regalo Q4** (B, C, D) | ¿Se regala en Navidad? Por qué | Decide la ventana y el ángulo ("one per car, one per driver") |
| **Comprador** (D) | Aficionado / pareja que regala | La pareja no compara precios; el aficionado sí |
| **Ventana** (B) | Semanas hasta el pico | ¿Te da tiempo a tener producto, landing y creativos antes? Si no, no es para ti |
| **Gasto Apify** | Leído del panel, no estimado | Si supera el tope, revisa el script antes del siguiente barrido |

## Orden de descarte al abrir (lo que se hizo en la sesión)

1. **Fuera por reglas propias**: electrónica aunque venga PRIORIDAD (tarjeta localizadora Find My, mini plancha, luz con sensor, cualquier cosa con linterna LED).
2. **Fuera por commodity**: ganchos adhesivos, cinta de doble cara, plumero, bayeta mágica. Pasan el número pero nadie paga $20 por lo que ve por $3 en el Dollar Tree. La bayeta con landed al 10 % es la trampa del margen bonito sobre un producto sin razón de compra.
3. **Fuera por cercanía a lo que ya te falló**: mismo mercado que un producto muerto (quitacal ↔ limpieza de baño saturada).
4. **Fuera por nicho minúsculo**: quita-oxidación de latón.
5. **Fuera por marca de referencia**: cerrojo portátil (Addalock, 15.000 reseñas a $22 con Prime), kit de pinchazos de mechas (Slime/Fix-a-Flat en cualquier Walmart a $10), car cane (Original Car Cane, As Seen On TV).
6. **Fuera por enjambre**: 5 tiendas genéricas que entraron la misma semana hace 32–40 días = dropshippers copiándose un anuncio, no demanda. En 3 semanas estarán a 0 o a 15.
7. **Fuera por logística/formato**: joyería (landed 27 %), vaso térmico (Stanley detrás + envío pesado), cortina magnética (voluminosa, no firme), ropa/tallas.
8. **Quedan 2–3.** Esos son los que abres en la Biblioteca y miras anuncio a anuncio.

## Qué quedó y por qué (para calibrar el ojo)

- **Coating cerámico en spray para coche** → PRIORIDAD firme, 1 dropshipper, líder DTC con marca grande detrás (categoría real). Demo de 5 s perfecta (agua resbalando), packs naturales, ángulo claro. Pega: landed al 23 % pegado al techo; líquido (confirmar envío US con el agente); "por qué a mí y no a Turtle Wax" lo tiene que resolver el creativo. **Resultado del test: CTR 4–8 %, 8 carritos, 0 compras en ~€124** → commodity con precio ancla en Amazon matando el checkout. Se apagó.
- **Rompecristales + cortacinturones** → 5 anunciantes, 3 dropshippers, landed 22 %. Vende miedo (convierte en frío), packs obvios (uno por coche, uno por hijo). Pega: producto viejo que resucita cada año; comprobar en la Biblioteca si los antiguos son marcas creciendo o cadáveres con el anuncio encendido. **Resultado: 2 compras en horas a ~€10 CPA contra €14,5 breakeven.**
- **Toalla de secado de coche** → 4 dropshippers, dos de ellos escalando meses (66 ads/191 d, 31 ads/373 d): prueba de que el genérico vende con Meta. Hueco: nadie la vende con coating ("Wash. Dry. Coat."). Cayó por landed 46 % (arreglable con agente). Se guardó como segundo producto de línea; murió con el coating.
- **Repelente de lluvia para parabrisas** (+117 % momentum, anuncio de 308 días) → no era producto nuevo: era un **ángulo** para el coating ("works on glass"), temporada arrancando, cero riesgo.
- **Juego de cartas de conversación** (momentum, landed 16 %, ventana 9–11 semanas) → replicable con IA + print-on-demand US, sin China. Descartado por decisión personal: territorio desconocido antes de un viaje. Foso cero (cualquiera imprime cartas): se gana por temática y creativo.
- **Ganchos de levantamiento** (+125 %) → pico en enero y catálogo trillado; vigilar, no tocar; decidir en diciembre.
- **Delantal ignífugo $49,99 "Perfect Grillmaster Gift"** → regalo Q4 hombre, sin marca de referencia, demo 5 s, genérico $6–9. Pega seria: todo el producto es un claim (1.100 °F) que no puedes verificar sin muestra, y 7 reseñas = ni el líder lo tiene validado. Se apuntó, no se montó.

## Lo que se aprende de cada resultado

- Un barrido con **cero** (seguridad familiar: 0/10) dice que STT no indexa ese vertical o que está en manos de retail. No se fuerza: se cambia la pregunta.
- **CTR alto + carritos + 0 compras** = precio ancla o checkout, no producto ni creativo. Se audita el checkout con una compra de prueba US desde el móvil; si está bien, es el ancla.
- **CTR bajo** (nadie para el scroll) = producto sin razón de compra visual. Kill rápido.
- La landing en Netlify no aparece en Shopify: Shopify solo ve a los que pulsan comprar. El tráfico real está en Meta (visitas a la página de destino) o en Netlify Analytics.
- Un producto que vende vale más que tres que igual venden: cuando hay una venta real, la ronda 2 de ese producto (vídeo, regalo Q4, upsell) rinde más que otro barrido.
