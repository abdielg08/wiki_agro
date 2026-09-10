---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-10
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/articles/ | 57 | ↑ continuo |
| Artículos marcados `ingested: true` | 18 | = total sin falsos positivos |
| — de los cuales, falsos positivos (`skipped`) | 7 | **0 nuevos** |
| — de los cuales, artículos reales ingestados al wiki | 11 | ↑ continuo |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 25 (8 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal real de sources/ | 2007-11-04 → 2026-08-21 | 2015-02-19 → hoy |
| Ventanas GDELT completadas (`_gdelt_windows`) | 79 | 45 (2015→hoy) — **superado** |
| Días sin commit de artículos nuevos en sources/ | 4 (último: 2026-09-06) | máx 3 antes de diagnosticar — **excedido** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con contenido  : 2026-09-06 ("6 artículos nuevos descargados")
Commits de sources/ desde     : ninguno entre 2026-09-07 y 2026-09-10 (hoy)
                                 — incluye ausencia de los commits habituales de
                                 "0 artículos nuevos" que el workflow genera a diario
Diagnóstico                   : posible fallo silencioso o interrupción del cron
                                 diario (.github/workflows/wiki_daily.yml, 11:00 UTC).
                                 No verificable desde esta sesión (sin acceso a los
                                 logs de ejecución de GitHub Actions).
Ventanas GDELT                : 79 completadas, muy por encima del umbral de 45 que
                                 CLAUDE.md usa como señal de rango histórico agotado.
                                 Puede requerir pasar a modo incremental (solo fetch
                                 de artículos nuevos, sin reprocesar ventanas ya
                                 cubiertas) si aún no ocurre así.
Acción recomendada            : revisar historial de ejecuciones de Actions en GitHub
                                 (fuera del alcance de esta sesión) para confirmar si
                                 el workflow corrió y falló, o no se disparó.
```

---

## Falsos Positivos — Hallazgo Adicional (2026-09-10)

Se detectó que, además de los 7 falsos positivos ya marcados `skipped` en sesiones
previas, la cola de pendientes (`ingested: false`) contiene URLs adicionales
claramente ajenas al agro panameño (Utah/EEUU, España, Brasil, papers IEEE, UNESCO,
etc.), todas mal etiquetadas con `source: "prensa.com"`. Esto apunta a un bug en el
pipeline de fetch. No se modificó `processed.json` para estas URLs en esta sesión
(fuera del alcance de "ingest --limit 5"); ver detalle en `wiki/log.md` (entrada
2026-09-10, punto 3). Pendiente de limpieza en una sesión de mantenimiento (LINT).

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Estado |
|---------|--------|
| 2015–2026 | Ventanas GDELT: **79/45+ completadas** (meta original superada) |

> El conteo detallado por trimestre de la tabla anterior ya no se mantiene manualmente:
> `_gdelt_windows` en `sources/processed.json` es la fuente de verdad del progreso de
> ventanas GDELT. Con 79 ventanas completadas, el backfill histórico parece cubierto;
> el cuello de botella actual es la **ingesta** (39 pendientes) y el **gap de fetch**
> descrito arriba, no la disponibilidad de ventanas GDELT.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-10 | 5 | 39 | Routine automatizada; 0 falsos positivos nuevos; detectado gap de fetch (4 días) y falsos positivos adicionales sin marcar en la cola |

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

> **Estado 2026-09-10**: esta señal de alarma ya se activó (4 días sin commits de
> sources/). Ver diagnóstico completo arriba y en `wiki/log.md`.
