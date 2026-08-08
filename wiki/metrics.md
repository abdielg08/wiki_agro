---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** (16 detectados en la sesión de hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 63 / ~46 estimadas | rango real 2017-03-30 → 2026-08-06 (falta 2015-01 → 2017-03) |
| Días sin artículos nuevos | 9 (desde 2026-07-30) | máx 3 antes de diagnosticar — umbral superado |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions  : 2026-08-07 (0 artículos nuevos)
Última con artículos    : 2026-07-30 (3 artículos nuevos)
Resultado               : 4 corridas consecutivas (07-31, 08-02, 08-04, 08-07) con 0 nuevos
Causa identificada #1   : ventanas GDELT 2015-01-01 a 2017-03-29 (~9 ventanas) nunca se
                          marcan completas (fetch_gdelt_historical recibe batch=None ahí)
                          y se reintentan sin éxito en cada corrida, sin avanzar la cobertura
                          histórica temprana. El resto del rango (2017-2026) ya está cubierto,
                          por eso las corridas recientes no encuentran ventanas nuevas.
Causa identificada #2   : 79% (23/29) de los artículos descargados son falsos positivos.
                          "MIDA" está en HIGH_PRIORITY_TERMS (scripts/prioritize.py) sin
                          filtro de país, capturando Malaysian Investment Development
                          Authority y la Utah Military Installation Development Authority,
                          además de noticias agrícolas genéricas de España/Brasil/Arabia
                          Saudita/Irán/EE.UU. sin relación con Panamá. Detalle en
                          wiki/log.md (entrada 2026-08-08 16:30).
Fix aplicado esta sesión: bug de selección en mark-all-ingested/mark-ingested corregido
                          (wiki/log.md 2026-08-08 16:20) — no afecta el fetch en sí.
Pendiente (fuera de alcance de hoy): filtrar el fetch por país=Panamá / topónimo
                          panameño, y diagnosticar el bloqueo de ventanas GDELT 2015-2017.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 (todo el año) | 0/4 | 0 | **Bloqueado** — GDELT no responde en este rango (batch=None cada corrida) |
| 2016 (todo el año) | 0/4 | 0 | **Bloqueado** — mismo problema que 2015 |
| 2017 | 4/4 | ? | Completo (arrancó ~2017-03-30, no desde 2015-01-01) |
| 2018 | 4/4 | ? | Completo |
| 2019 | 4/4 | ? | Completo |
| 2020 | 4/4 | ? | Completo |
| 2021 | 4/4 | ? | Completo |
| 2022 | 4/4 | ? | Completo |
| 2023 | 4/4 | ? | Completo |
| 2024 | 4/4 | ? | Completo |
| 2025 | 4/4 | ? | Completo |
| 2026 (hasta 2026-08-06) | 27 (ver nota) | ? | Ver nota — no son 27 ventanas reales |
| **TOTAL** | **63** | **0 días productivos desde 2026-07-30** | **2015-2017 (parcial) bloqueado; resto cubierto** |

> Nota sobre 2026: las 27 "ventanas" de 2026 no son 27 períodos distintos — son la MISMA
> ventana final (inicio fijo ~2026-06-18) recompletándose cada día con una fecha de fin que
> avanza (`end = min(config_end, ayer)`), porque aún no han transcurrido los 90 días completos
> del trimestre. Esto infla el conteo de "ventanas completadas" sin representar cobertura
> histórica real, y probablemente explica por qué el fetch diario re-consulta casi el mismo
> rango de fechas sin encontrar artículos nuevos. No requiere acción inmediata (se
> autocorrige cuando el trimestre se completa), pero conviene tenerlo presente al leer esta
> métrica. El bloqueo real y accionable es 2015-01-01 → 2017-03-29.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-08 | 0 | 0 | 16 artículos revisados, todos falsos positivos ("MIDA" ambiguo + agro genérico sin filtro de país); fix de bug en mark-all-ingested/mark-ingested; 9 días sin artículos nuevos — ver Estado del Fetch |

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
