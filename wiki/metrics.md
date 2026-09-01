---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-01
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 33 | 0 |
| Falsos positivos acumulados | 8 (7 previos + 1 nuevo: MITI/Malasia, no ingestado) | **0 nuevos por sesión** |
| Páginas en wiki/ | 26 (10 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 | rango agotado — necesita expansión (>45) |
| Días sin artículos nuevos en sources/ | 5 (último: 2026-08-27) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa con artículos  : 2026-08-27 (run #93, "1 artículos nuevos descargados")
Últimas 4 corridas (#94–#97)          : FALLARON — 2026-08-28, 08-29, 08-30, 08-31
Duración de las corridas fallidas     : ~3 segundos, sin runner asignado (runner_id: 0)
Causa probable                        : startup_failure — límite de minutos/gasto de GitHub Actions
                                         agotado, o problema de configuración/permisos del repositorio.
                                         No es un error del script de fetch (nunca llegó a ejecutarse).
Ventanas GDELT                        : 76 completadas — por encima del umbral 45+ de CLAUDE.md,
                                         sugiere que el rango de fechas GDELT disponible ya se agotó
                                         y requiere expansión (además del problema de Actions).
Acción requerida (fuera del alcance
de un commit de código)               : el usuario debe revisar Settings → Actions / facturación del
                                         repositorio o cuenta de GitHub para restaurar la ejecución
                                         del workflow "Wiki Agropecuario — Fetch Diario".
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015–2026 | 76 completadas | Rango agotado — pendiente expansión de años/fuentes adicionales |

> Nota: la tabla trimestral anterior (0/46) quedó obsoleta — el fetch ya avanzó a 76 ventanas GDELT
> desde entonces. Pendiente reconstruir el detalle por período con datos de `sources/processed.json`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Falsos positivos | Pendientes restantes | Nota |
|-------|---------------------|-------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-01 | 4 | 1 (MITI/Malasia, no ingestado) | 33 | GitHub Actions con 4 corridas fallidas consecutivas (ver log.md) |

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

**Estado 2026-09-01**: umbral de alarma superado (5 días sin artículos nuevos, 4 corridas de
Actions fallidas consecutivas). Diagnóstico completo en `wiki/log.md`. Requiere intervención del
usuario en la configuración de GitHub Actions — no resoluble con un commit de código.
