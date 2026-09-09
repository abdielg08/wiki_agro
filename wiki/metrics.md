---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7+ (ver nota) | **0 nuevos** |
| Páginas en wiki/ | 25 (8 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2016-2025 (artículos reales ingestados) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45 (2015→hoy) — meta superada |
| Días sin artículos nuevos en sources/ | **3** (2026-09-07, 08, 09) | máx 3 antes de diagnosticar → **UMBRAL ALCANZADO** |

> **Nota falsos positivos**: entre los 39 pendientes actuales hay artículos claramente
> no relacionados con agro de Panamá (ej. "Reef Saudi", data centers en Utah, granjas en
> Aragón/España, Mozambique, Brasil, catálogo de dípteros), todos etiquetados incorrectamente
> con `source: prensa.com`. No se han ingestado — quedan pendientes de marcarse como falso
> positivo en una futura sesión que los reciba en su lote de `ingest --limit N`.
>
> **Causa raíz corregida (2026-09-09)**: `fetch_ddg_search()` en `scripts/fetch_news.py` no
> validaba que la URL devuelta por DuckDuckGo perteneciera realmente al dominio buscado
> (`site:prensa.com`), permitiendo que entraran artículos de dominios globales sin relación
> con Panamá. Se agregó validación de dominio + `_is_blocked_domain()`. También se corrigió
> `mark_all_ingested()` en `scripts/ingest.py` para que use el mismo criterio de prioridad
> (`prioritize()`) que `ingest`, evitando que marque como ingestados artículos distintos a los
> que realmente se procesaron. Ver `wiki/log.md` (2026-09-09) para el detalle completo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida CON artículos nuevos : 2026-09-06 13:56 UTC (6 artículos, run #103, success, ~5.5 min)
Corridas siguientes                 : #104 (09-07), #105 (09-08), #106 (09-09) → conclusion=FAILURE
Duración de las corridas fallidas   : ~4-7 segundos (vs. ~5 min de una corrida normal)
Detalle                             : runner_id=0, sin runner asignado, sin logs de steps (404 al pedirlos)
                                       → el job NO llegó a ejecutar checkout/pip/fetch
Causa identificada                  : el cron SÍ dispara el workflow (evento "schedule" presente),
                                       pero el job falla antes de arrancar. No es GDELT, no es RSS,
                                       no es el código de wiki_agro.py — es un problema de asignación
                                       de runner a nivel de cuenta/repo (cuota de minutos de Actions
                                       agotada, o política que bloquea runners ubuntu-latest).
Fix aplicado                        : ninguno (fuera del alcance de una sesión de Claude Code — requiere
                                       revisión de Settings → Billing/Actions por el usuario)
Estado                               : PENDIENTE de que el usuario revise cuota/permisos de Actions
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **79/~46 estimadas** | 57 en sources/ (todas las fuentes, no solo GDELT) | **Backfill completado en número de ventanas; meta de cobertura 2015→hoy superada en ventanas** |

> **2026-09-09**: `sources/processed.json._gdelt_windows` reporta **79 ventanas completadas**,
> muy por encima de las ~46 estimadas para cubrir 2015→hoy. La tabla trimestral anterior (0/46,
> "Backfill no iniciado") estaba desactualizada — `wiki_agro.py` no expone un desglose por
> trimestre en `processed.json`, así que no se reconstruye aquí fila por fila para evitar
> inventar cifras. El cuello de botella actual no es GDELT: es que GitHub Actions dejó de
> asignar runners al workflow desde 2026-09-07 (ver "Estado del Fetch" arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-09 | 5 | 39 | Backfill arroz/MIDA 2022-2025; 0 falsos positivos en el lote; diagnosticado fallo de Actions (3 días sin runner) |

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
