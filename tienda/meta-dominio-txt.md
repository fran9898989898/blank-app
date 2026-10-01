# Verificación del dominio en Meta (registro TXT)

El valor lo genera Meta para TU Business Manager: no se puede preparar sin entrar en él. Pasos y registro listos para copiar:

1. business.facebook.com → Configuración del negocio → Seguridad de la marca → Dominios → Añadir → `DOMINIO-NEUTRO.com` (dominio raíz, sin subdominio).
2. Elige "Actualizar el registro TXT de DNS". Meta muestra un código.
3. En el DNS del dominio (Cloudflare u OVH, donde esté el dominio neutro) añade:

| Tipo | Nombre / Host | Valor | TTL |
|---|---|---|---|
| TXT | `@` (raíz) | `facebook-domain-verification=CODIGO_QUE_DA_META` | Auto / 3600 |

4. Espera la propagación (minutos a 72 h) → "Verificar" en Meta.
5. Comprobación: `dig TXT DOMINIO-NEUTRO.com +short` debe devolver la línea.

Notas:
- El subdominio de la landing (p. ej. `fit.DOMINIO-NEUTRO.com`) hereda la verificación: no se verifica aparte.
- Cloudflare: el TXT con nube gris (los TXT no se proxifican).
- Sin acceso al BM, alternativa: metaetiqueta `<meta name="facebook-domain-verification" content="CODIGO">` en el `<head>` del tema de Shopify (solo cubre el dominio que sirve Shopify).
- Subdominio de la landing: CNAME `fit` → `<sitio>.netlify.app` (ver la skill, deploy-netlify.md).
