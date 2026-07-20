---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 15 (7 previos + 8 hoy) | **0 nuevos** — ver fix aplicado 2026-07-20 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 51 / ~46 estimadas | 45+ (backfill agotado bajo query actual) |
| Días sin artículos nuevos reales | ~57 (desde 2026-05-24, semilla) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-20 13:08 UTC (commit a41daf4)
Resultado               : 2 artículos nuevos descargados — AMBOS falsos positivos
Causa identificada      : fetch_ddg_search() (fuente web "prensa_agro" y análogas en
                          config/sources.yaml) solo filtraba con is_agro_relevant()
                          (keywords genéricos: "MIDA", "agricultura"...) sin los guards
                          _is_blocked_domain() / _is_panama_related() que ya protegen
                          a fetch_rss() y fetch_gdelt_batch(). El operador site: de
                          DDGS tampoco se respeta de forma confiable — la búsqueda
                          "site:prensa.com ..." devolvía resultados de sltrib.com,
                          thestar.com.my, ieeexplore.ieee.org, archive.org, etc.,
                          todos mal-etiquetados como fuente "prensa.com".
                          Esto explica ~15 falsos positivos acumulados (todas las
                          entradas de la fuente "prensa.com" hasta ahora).
Fix aplicado            : fetch_ddg_search() ahora aplica _is_blocked_domain() y
                          _is_panama_related() igual que RSS/GDELT (commit 2026-07-20).
                          También se corrigió mark_ingested() en scripts/ingest.py,
                          que fallaba con AttributeError al toparse con la clave
                          _gdelt_windows (lista, no dict) en processed.json.
Estado post-fix         : Pendiente validación en próxima corrida Actions —
                          debería reducir drásticamente los falsos positivos de
                          la fuente "prensa_agro" y análogas (DDG web search).
GDELT                   : 51 ventanas completadas, 0 artículos reales aprovechados
                          hasta ahora — requiere revisión futura de query/filtro
                          sourcecountry:PA (posible causa: GDELT indexa poca prensa
                          panameña pequeña, o el filtro es demasiado estricto).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

```
Ventanas completadas (processed.json["_gdelt_windows"]) : 51
Estimado original (2015-01-01 → 2027-12-31, trimestral) : ~46-52
Artículos reales incorporados al wiki desde GDELT        : 0
```

> El backfill de ventanas está esencialmente completo (51 ≥ 45, umbral de
> "rango agotado" según CLAUDE.md Paso 4). Sin embargo, ninguna ventana ha
> producido un artículo que haya llegado a `wiki/` — los 6 summaries actuales
> son datos semilla manuales, no resultado de GDELT. Diagnóstico pendiente:
> revisar si `sourcecountry:PA` + los términos de `_AGRO_QUERY` son
> demasiado restrictivos, o si GDELT simplemente no indexa suficiente
> prensa panameña pequeña. Próxima sesión: correr `fetch_gdelt_batch()`
> manualmente contra una ventana conocida y verificar el conteo crudo de
> `data["articles"]` antes del filtro `_is_panama_related`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-20 | 0 reales (8 revisados, 8 falsos positivos) | 0 | Root-cause: `fetch_ddg_search()` sin guards Panamá; fix aplicado — ver Estado del Fetch |

---

## Instrucciones para la Routine

Al ejecutar, la routine DEBE:

1. Correr `python wiki_agro.py stats` y copiar los números aquí
2. Si ingestó artículos: actualizar la tabla "Historial de Sesiones"
3. Si pendientes = 0: actualizar "Estado del Fetch" con diagnóstico
4. Actualizar "last_updated" en el frontmatter
5. Si `Ventanas GDELT completadas` subió: actualizar tabla de Backfill

**Señal de alarma**: si "Días sin artículos nuevos" llega a 3, la routine debe:
- Revisar el último log de GitHub Actions (ver wiki/log.md para contexto)
- Identificar si el problema es GDELT rate-limit, RSS caído, o config
- Documentar el diagnóstico en wiki/log.md con pasos para resolverlo
