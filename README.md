# product-radar · barridos de producto

**Empieza aquí.** Todo lo necesario está en la rama `main` de este repo.

| Qué | Dónde |
|---|---|
| Skill (método, filtros, orden de barridos) | `.claude/skills/barridos-searchthetrend/` |
| Scripts (Biblioteca de Meta, AliExpress, Amazon, Walmart, Shopify) | `tools/` |
| Resumen de todos los barridos | `barridos/radar.html` (ábrelo en Chrome) |
| Visor de cada barrido | `barridos/<fecha>/visor.html` |

## Cómo se usa

1. Abre Claude Code sobre este repo en la rama `main` (en la nube desde la web o el móvil, o en tu PC tras `git pull`).
2. Escribe: **«haz el siguiente barrido»**.
3. Claude aplica la skill y al terminar te entrega: visor del barrido, `radar.html` actualizado y un resumen (vivos, dudosos, KILL, fuera, siguiente barrido, gasto de Apify).

Requisitos la primera vez: SearchTheTrend conectado como MCP y `APIFY_TOKEN` configurado (ver `.claude/skills/barridos-searchthetrend/references/setup.md`).
