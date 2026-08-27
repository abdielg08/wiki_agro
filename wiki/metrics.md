---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-27
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 50 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 (7 previos + 1 hoy: paultan.org/MITI Malasia) | **0 nuevos** |
| Pendientes de ingesta | 32 | 0 |
| Páginas en wiki/ | 24 (8 topics, 3 entities, 10 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, en progreso) | 2015 → hoy real |
| Ventanas GDELT completadas | 75 | ~45-46 estimadas (objetivo ya superado) |
| Días sin artículos nuevos | 0-3 (ver diagnóstico abajo) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-26 (run #92, completed/success)
Resultado               : 0 artículos nuevos ese día
Corrida previa          : 2026-08-25 (run #91) → 20 artículos nuevos
Corrida 2026-08-24      : (run #90) → 0 artículos nuevos
Diagnóstico             : El workflow wiki_daily.yml SÍ está corriendo diariamente sin errores
                          (últimas 10+ corridas: conclusion=success). La variabilidad 0/20/0
                          artículos es consistente con la naturaleza intermitente de RSS
                          (IICA, La Prensa) + GDELT, no con una falla del pipeline.
                          Ventanas GDELT completadas (75) ya superan el estimado original de
                          ~45-46 para cobertura 2015→hoy — el backfill histórico vía GDELT
                          parece estar mayormente agotado/cubierto; las ventanas nuevas que se
                          siguen agregando corresponden a tracking incremental de días recientes.
Corrida de hoy (2026-08-27, 11:00 UTC) : aún no reflejada en el historial de Actions al momento
                          de esta sesión (la sesión corrió antes de esa hora) — no se puede
                          confirmar todavía si trajo artículos nuevos.
Acción recomendada       : sin acción correctiva por ahora — monitorear si el patrón de 0
                          artículos se repite 2+ días más seguidos, lo cual sí ameritaría revisar
                          si las fuentes RSS (IICA, La Prensa) dejaron de publicar contenido
                          nuevo o si el filtro de relevancia se volvió demasiado estricto.
```

### Bug corregido en esta sesión (2026-08-27)
`mark-all-ingested --limit N` selecciona artículos por orden alfabético de archivo
(`find_pending()`), mientras que `ingest --limit N` los selecciona por score de prioridad
(`prioritize()`). Ambos usan "--limit 5" pero pueden devolver conjuntos distintos. Esto causó
que 5 artículos nunca procesados fueran marcados `ingested: true` por error; se revirtieron
manualmente en `sources/processed.json` y se marcaron correctamente los 5 realmente procesados.
Ver detalle completo en `wiki/log.md` (entrada 2026-08-27 08:35). Recomendación: usar
`mark-ingested <url>` individual (inmune al bug) en vez de `mark-all-ingested --limit N` hasta
que se corrija el código, o unificar el criterio de orden entre ambas funciones.

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | Pendiente |
| 2016 Q1-Q4 | 0/4 | ? | Pendiente |
| 2017 Q1-Q4 | 0/4 | ? | Pendiente |
| 2018 Q1-Q4 | 0/4 | ? | Pendiente |
| 2019 Q1-Q4 | 0/4 | ? | Pendiente |
| 2020 Q1-Q4 | 0/4 | ? | Pendiente |
| 2021 Q1-Q4 | 0/4 | ? | Pendiente |
| 2022 Q1-Q4 | 0/4 | ? | Pendiente |
| 2023 Q1-Q4 | 0/4 | ? | Pendiente |
| 2024 Q1-Q4 | 0/4 | ? | Pendiente |
| 2025 Q1-Q4 | 0/4 | ? | Pendiente |
| 2026 Q1-Q2 | 0/2 | ? | Pendiente |
| **TOTAL** | **0/46** | **0** | **Backfill no iniciado** |

> Una vez que Actions corra con el código corregido, actualizar esta tabla con los datos reales.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-27 | 4 (+1 falso positivo detectado) | 32 | Rutina programada; corregido bug de `mark-all-ingested` (ver arriba) |

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
