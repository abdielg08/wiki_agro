---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-29
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 51 | ↑ continuo |
| Artículos ingestados (incl. falsos positivos marcados para retirarlos de la cola) | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 33 | 0 |
| Falsos positivos acumulados | 8 (7 previos "MIDA Malasia" + 1 nuevo "MITI Malasia" 2026-08-29) | **0 nuevos por sesión, idealmente** |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes, 2 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 (superó el estimado de ~45-46) | rango agotado — ver diagnóstico |
| Días sin artículos nuevos en sources/ | 2 (última descarga real: 2026-08-27) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions exitosa : 2026-08-27 20:51 UTC (run #93, 1 artículo nuevo)
Últimas 2 corridas             : 2026-08-28 21:16 UTC (run #94) → FALLO
                                  2026-08-29 15:23 UTC (run #95) → FALLO
Duración de corridas fallidas  : ~3-4 segundos (vs. ~6 min en corridas normales)
Diagnóstico                    : el job "Fetch artículos → Commit a sources/" nunca
                                  llegó a asignarse un runner (sin runner_id/runner_name,
                                  sin pasos ejecutados — falla antes de "Set up job").
                                  No es un error del script Python (fetch/ingest tienen
                                  continue-on-error: true y ni siquiera se alcanzaron).
Causa más probable              : cuota de minutos de GitHub Actions agotada para la
                                  cuenta/organización, o Actions deshabilitado/restringido
                                  a nivel de repo — no se puede confirmar sin acceso a
                                  Settings → Billing / Settings → Actions del repositorio.
Ventanas GDELT                  : 76 ventanas completadas, superando el estimado de ~45-46
                                  necesarias para cubrir 2015→hoy. El rango de fechas del
                                  backfill histórico está efectivamente agotado; nuevas
                                  ventanas GDELT ya no deberían aportar artículos nuevos
                                  hasta que se expanda la lógica de generación de ventanas.
Acción recomendada (usuario)    : 1) revisar github.com/settings/billing (o el billing de
                                  la organización) por minutos de Actions agotados;
                                  2) revisar Settings → Actions → General del repo por
                                  restricciones; 3) si el backfill GDELT está agotado,
                                  revisar/expandir la lógica de ventanas en el script de
                                  fetch para cubrir vacíos o repetir con distinta granularidad.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

```
Ventanas GDELT completadas (sources/processed.json → _gdelt_windows) : 76
Estimado original (quarters 2015-2026)                                : ~46
```

> **Nota (2026-08-29)**: la tabla trimestral anterior (`Período | Ventanas | Artículos | Estado`)
> quedó desactualizada y contradecía el conteo real (`_gdelt_windows` ya tiene 76 entradas,
> no 0/46 como decía la tabla). `_gdelt_windows` almacena rangos de fecha en formato
> `YYYYMMDD_YYYYMMDD` sin desglose de artículos por ventana ni orden cronológico garantizado,
> por lo que no es posible reconstruir aquí una tabla trimestral fiel sin instrumentar el
> script de fetch para que registre esa granularidad. Se retira la tabla fabricada para no
> reportar datos falsos; el número real de ventanas (76) ya superó el estimado de ~46,
> lo que indica que el rango de fechas 2015→hoy está cubierto o el criterio de generación
> de ventanas necesita revisión (posibles duplicados o solapamientos).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-29 | 4 reales + 1 falso positivo documentado | 33 | Routine automática; detectado y corregido bug de desalineación entre `ingest --limit N` (orden por score) y `mark-all-ingested --limit N` (orden alfabético) — ver wiki/log.md 16:20. Diagnosticado: Actions falla 2 días seguidos sin asignar runner (probable cuota agotada); GDELT en 76/~46 ventanas (rango agotado) |

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
