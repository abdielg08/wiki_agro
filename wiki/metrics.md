---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-12
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
| Falsos positivos acumulados | 7 | **0 nuevos** (0 nuevos esta sesión) |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2007–2026 (mezcla histórica + reciente, aún no continua) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45 (2015→hoy) — **superado**, ya no es el cuello de botella |
| Días sin artículos nuevos en sources/ | **6** (último commit: 2026-09-06) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions (exitosa)  : 2026-09-06 13:50 UTC — run #103, 6 artículos nuevos, ~329s
Corridas desde entonces           : #104-#109 (2026-09-07 a 2026-09-12), TODAS conclusion=failure
Duración de las corridas fallidas : ~3-4 segundos (demasiado corto para llegar a ejecutar
                                     `python wiki_agro.py fetch`; falla temprana en el workflow —
                                     checkout, permisos o setup, no lógica de fetch_gdelt.py)
Logs disponibles                  : NO — HTTP 404 al intentar descargarlos (expirados/fuera de
                                     retención) al momento de este diagnóstico (2026-09-12)
Causa raíz                        : NO DETERMINADA desde esta sesión por falta de logs
Acción recomendada                : el usuario debe revisar
                                     https://github.com/abdielg08/wiki_agro/actions/runs/34697444719
                                     (o correr un workflow_dispatch manual) ANTES de que expiren
                                     también los logs de runs más recientes
Nota GDELT                        : las ventanas completadas (79) ya superan el umbral de 45 de
                                     CLAUDE.md, pero eso es irrelevante mientras el workflow falle
                                     antes de invocar el fetch — no es un problema de rango de fechas
```

---

## Hallazgo de esta sesión: bug en `mark-all-ingested`

`ingest --limit N` selecciona artículos por score de relevancia (prioritize.py),
pero `mark-all-ingested --limit N` recalculaba con `find_pending()` (orden
alfabético por nombre de archivo) — un lote distinto casi siempre. Esto llevó
a marcar como "ingestados" artículos que Claude nunca procesó (incl. uno
totalmente ajeno al agro), mientras los artículos realmente procesados
seguían apareciendo como pendientes indefinidamente. Corregido en
`scripts/ingest.py` (ver `wiki/log.md`, entrada BUGFIX 2026-09-12) guardando
el lote exacto mostrado por `ingest` en `sources/.last_ingest_batch.json` y
haciendo que `mark-all-ingested` lo use. También se corrigió un
`AttributeError` en `mark-ingested` al iterar la clave interna
`_gdelt_windows` de `processed.json`.

Adicionalmente se detectó que ~28% de la cola de pendientes (11/39 al
momento del diagnóstico) son artículos claramente ajenos a Panamá que GDELT
etiqueta genéricamente como `source: prensa.com` (agricultura de España,
Brasil, Arabia Saudita, EE.UU., etc.). Se agregó un filtro heurístico
(`looks_like_false_positive` en `prioritize.py`) que los excluye de la
priorización de `ingest`. Es una mitigación, no una solución completa:
colisiones de sigla (p.ej. "MIDA" = Ministerio panameño, pero también
Malaysian Industrial Development Authority) pueden seguir colándose — la
verificación humana/LLM del Paso 3 de CLAUDE.md sigue siendo necesaria.

---

## Progreso del Backfill GDELT (2015 → hoy)

> Pendiente de reconstrucción con datos reales de `sources/processed.json._gdelt_windows`
> (79 ventanas completadas). La tabla anterior (0/46, "Backfill no iniciado") quedó
> desactualizada desde la sesión de 2026-06-22 y no se llenó en sesiones posteriores.
> Próxima routine: derivar la tabla real a partir de `_gdelt_windows` en vez de
> reescribirla a mano.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-12 | 5 | 39 | Routine programada; bugfix mark-all-ingested + filtro de falsos positivos en prioritize.py; diagnosticado fallo de GitHub Actions desde 2026-09-07 |

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

**Estado al 2026-09-12: alarma ACTIVA (6 días sin artículos nuevos).** Ver
sección "Estado del Fetch" arriba — causa raíz no determinada por falta de
logs; requiere revisión humana en la UI de GitHub Actions.
