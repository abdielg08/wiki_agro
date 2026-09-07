---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-07
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
| Falsos positivos acumulados (marcados) | 7 | **0 nuevos** |
| Falsos positivos detectados y AÚN sin marcar en la cola | 7 (ver nota) | 0 |
| Páginas en wiki/ | 25 | ↑ continuo |
| Cobertura temporal real (GDELT) | 2017–2026 | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 79 (ver detalle abajo) | cobertura completa 2015→hoy |
| Días sin artículos nuevos | 0 (última descarga: 2026-09-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-09-06 (6 artículos nuevos, prensa.com)
Resultado                           : Actions SÍ está corriendo diariamente (commits [skip ci] regulares)
Aún no hay corrida registrada hoy (2026-09-07) al momento de esta sesión — no es señal de falla (<3 días)
```

### Hallazgo de esta sesión (2026-09-07): backfill 2015-2016 en cero, ventanas 2026 anómalas

Al contar `_gdelt_windows` en `sources/processed.json` (79 ventanas totales) y agruparlas por año:

| Año | Ventanas completadas |
|-----|----------------------|
| 2015 | **0** |
| 2016 | **0** |
| 2017 | 4 |
| 2018 | 4 |
| 2019 | 4 |
| 2020 | 4 |
| 2021 | 4 |
| 2022 | 4 |
| 2023 | 4 |
| 2024 | 4 |
| 2025 | 4 |
| 2026 | 43 (anómalo — ver abajo) |

- **2015 y 2016 — el inicio real de la cobertura objetivo (2015-02-19) — tienen 0 ventanas GDELT completadas.** El backfill histórico nunca ha llegado a esos años pese a que `scripts/fetch_news.py::fetch_gdelt_historical()` itera secuencialmente desde `date_range.start = 2015-01-01`.
- Las 43 ventanas de "2026" no son trimestres reales: todas comparten el mismo inicio fijo `20260618` con fecha final creciente día a día (`20260618_20260623`, `..._20260624`, `..._20260702`, … hasta `..._20260903`). Esto sugiere que el fetch diario (`wiki_agro.py fetch --mode all`) está generando/consumiendo ventanas de "captura reciente" con inicio fijo en vez de avanzar el backfill histórico ordenado desde 2015.
- **Recomendación para el mantenedor**: correr manualmente el workflow `wiki_historical.yml` (crawl histórico, `workflow_dispatch`) con `years: 2015-2016`, `mode: gdelt` para forzar el backfill de los años faltantes; y revisar `fetch_gdelt_historical()` para confirmar por qué las ventanas de 2026 se regeneran con inicio fijo en lugar de avanzar cronológicamente. No se ejecutó el workflow desde esta sesión de ingest (acción de mayor alcance, fuera del flujo de 6 pasos de la routine).

### Falsos positivos detectados en la cola de pendientes (no ingeridos, aún sin marcar `skipped`)

Durante el diagnóstico de esta sesión se detectaron en `sources/processed.json` (`ingested: false`, sin `skip_reason`) los siguientes candidatos que **NO son sobre agro panameño** y deben marcarse/descartarse como falsos positivos la próxima vez que aparezcan en `pending_ingest.md` (probable causa: coincidencia de la palabra "MIDA" con la agencia malasia *Malaysian Investment Development Authority*, y consultas GDELT/RSS demasiado genéricas):

- `spa.gov.sa/en/N2096157` — "Reef Saudi" (agricultura de secano en Arabia Saudita, no Panamá)
- `sltrib.com/.../kevin-oleary-data-center-timeline` — centros de datos en Utah, EE.UU.
- `sltrib.com/.../utah-governor-issues-order-protect` — política ambiental de Utah, EE.UU.
- `sltrib.com/.../box-elder-data-center-opponents` — centros de datos en Utah, EE.UU.
- `nyfb.org` — página institucional de New York Farm Bureau (EE.UU.)
- `sltrib.com/.../utah-nuclear-energy-state` — energía nuclear en Utah, EE.UU.
- `ieeexplore.ieee.org/document/10945742` — paper técnico de IoT genérico, sin relación con Panamá

Estos ya están correctamente identificados aquí como falsos positivos y **no deben ingestarse** cuando el CLI los presente en un futuro `pending_ingest.md`.

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — prioridad alta** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — prioridad alta** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (parcial, ventanas anómalas) | 43 (no-trimestrales) | Ver hallazgo arriba |
| **TOTAL trimestres reales 2015-2025** | **36/44** | 2015-2016 faltantes |

> 2015 y 2016 deben tratarse como prioridad para el próximo crawl histórico manual.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-07 | 5 | 39 | Routine automatizada; 0 falsos positivos en el lote; diagnóstico: backfill 2015-2016 en cero, 7 falsos positivos adicionales detectados en la cola |

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
