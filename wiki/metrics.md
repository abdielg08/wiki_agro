---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-04
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos procesados (ingested=true) | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 (7 previos + 1 el 2026-09-04) | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, en backfill) | 2015 → hoy real |
| Ventanas GDELT completadas | 78 | 45 (2015→hoy) — **YA SUPERADO** |
| Días sin artículos nuevos | 8 (última descarga real: 2026-08-27) | máx 3 antes de diagnosticar |

**⚠️ ALARMA ACTIVA**: 8 días sin artículos nuevos descargados por GitHub Actions — supera el umbral de 3 días. Ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con resultados : 2026-08-27 (commit 2e30165, 1 artículo nuevo)
Corridas recientes sin nuevos  : 2026-09-01 (df761f6, 0), 2026-09-03 (30074d2, 0)
Ventanas GDELT completadas     : 78 (>= 45 estimadas para cubrir 2015→hoy)
Diagnóstico (2026-09-04)       : Actions SÍ está corriendo (hay commits [skip ci] recientes),
                                  pero devuelve 0 artículos nuevos en las últimas 2 corridas.
                                  Con 78 ventanas GDELT ya completadas (> umbral de 45), el
                                  rango de fechas históricas parece agotado — GDELT ya no
                                  tiene ventanas nuevas que ofrecer con la configuración actual.
Causa más probable             : Rango de fechas de backfill agotado → necesita expansión
                                  (ventanas más recientes / reconfigurar límites de fecha) o
                                  las fuentes RSS (IICA, La Prensa) no están aportando artículos
                                  nuevos en el día a día.
Acción recomendada             : Revisar sources/processed.json → _gdelt_windows (78 entradas)
                                  y expandir/ajustar el rango de backfill en scripts de fetch;
                                  validar que las fuentes RSS activas sigan respondiendo.
Bug adicional detectado        : 1 artículo (paultan.org, sobre política industrial de Malasia)
                                  fue etiquetado incorrectamente con source="prensa.com" y
                                  country="PA" — ver falso positivo documentado en wiki/log.md
                                  2026-09-04. Revisar el scraper que asigna source/country.
```

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
| **TOTAL** | **78/46** | **51** | **Ventanas GDELT superan la meta original; desglose por trimestre pendiente de recomputar** |

> 2026-09-04: `sources/processed.json → _gdelt_windows` ya tiene 78 ventanas registradas (más que
> las 46 estimadas para cubrir 2015→hoy), pero el fetch automático lleva 8 días sin traer
> artículos nuevos. Esto sugiere que las ventanas se están re-generando o solapando sin cubrir
> rango nuevo real. La tabla por trimestre de arriba está desactualizada (asume 0 ventanas) y
> debe recalcularse a partir de las 78 entradas de `_gdelt_windows` en una próxima sesión de
> mantenimiento/lint.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-04 | 4 (+1 falso positivo rechazado) | 33 | Routine: arroz/maíz/inundaciones/subsidios; detectado bug de source/country mal asignado; ventanas GDELT (78) superan umbral 45 — backfill necesita expansión de rango |

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
