---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-13
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~48 estimadas | backfill histórico completo |
| Días sin artículos reales nuevos | ~50 (desde 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-13 — descargó artículos, pero 100% falsos positivos
Resultado               : 0 artículos reales nuevos desde 2026-05-24 (~7 semanas);
                          14 falsos positivos acumulados en ese período, todos vía
                          la búsqueda web "prensa_agro" (DuckDuckGo)
Causa identificada      : (1) site:prensa.com no lo respeta de forma confiable la
                          librería `ddgs` — se colaron resultados de sltrib.com,
                          thestar.com.my, fox13now.com, nyfb.org, spa.gov.sa,
                          whc.unesco.org, worldbank.org, ieeexplore.ieee.org.
                          (2) is_agro_relevant() hace substring matching naive:
                          "agricultura" es substring de "agricultural" (inglés);
                          "MIDA" sin contexto matchea instituciones homónimas en
                          Malasia/Utah. Ver diagnóstico completo en wiki/log.md
                          (entrada 2026-07-13).
                          GDELT: 48 ventanas = backfill histórico ya está al día,
                          no es la causa del estancamiento.
Fix aplicado             : fetch_ddg_search() ahora valida que el dominio real de
                          la URL coincida con `site` antes de aceptar el resultado.
                          Query de prensa_agro reagrupada para requerir "Panamá".
                          2 bugs corregidos en scripts/ingest.py (mark_all_ingested
                          usaba orden distinto a `ingest`; mark_ingested crasheaba
                          con la clave _gdelt_windows).
Estado post-fix          : Pendiente validación en próxima corrida Actions —
                          confirmar que prensa_agro trae artículos reales.
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
| **TOTAL** | **0/46** | **0** | **Backfill no iniciado** |

> Una vez que Actions corra con el código corregido, actualizar esta tabla con los datos reales.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-13 | 0 | 0 | 8 falsos positivos revisados y descartados (0 reales). Causa raíz diagnosticada y corregida (site: no aplicado en DDG + is_agro_relevant demasiado laxo). 2 bugs de ingest.py corregidos. Ver wiki/log.md. |

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
