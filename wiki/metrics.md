---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados (confirmados/marcados) | 7 | **0 nuevos** |
| Falsos positivos sospechados en backlog (no ingestados aún) | ~7-10 (ver diagnóstico 2026-09-06) | 0 al momento de ingestar |
| Páginas en wiki/ | 26 (9 topics, 3 entities, 11 summaries, resto overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (según `_gdelt_windows` en processed.json) | cobertura 2015→hoy |
| Días sin artículos nuevos | 0 (último fetch: 2026-09-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-09-06 (commit 24cfc3c: "6 artículos nuevos descargados")
Resultado              : 6 artículos nuevos el día de la última corrida — el fetch SÍ está funcionando
Ventanas GDELT          : 79 completadas (ver sources/processed.json._gdelt_windows)
Hallazgo nuevo (2026-09-06): el backlog de 57 artículos descargados incluye varios
                         falsos positivos por colisión de sigla/keyword (p.ej. "MIDA" de Malasia,
                         noticias de EE.UU./Arabia Saudita/Brasil/Mozambique no relacionadas con
                         Panamá). Ninguno fue ingestado; deben filtrarse manualmente al aparecer
                         en pending_ingest.md. Ver wiki/log.md 2026-09-06 14:05 para detalle completo.
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
| **TOTAL** | **79/46 (ver nota)** | **57** | **En progreso** |

> 2026-09-06: `sources/processed.json._gdelt_windows` reporta 79 ventanas completadas y 57 artículos
> descargados en total, confirmando que el backfill está en marcha. No se dispone de un desglose
> por trimestre/año en el estado actual del script, por lo que la tabla de arriba (por período) no
> se actualiza línea por línea para evitar inventar cifras — solo se actualiza el TOTAL con el dato
> real disponible. El total de 79 ventanas supera la estimación original de 46, lo que sugiere que
> el script cuenta reintentos/subventanas distinto a la estimación inicial; revisar en una futura
> sesión de mantenimiento si se requiere granularidad por trimestre.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-06 | 5 (0 falsos positivos) | 39 | Lote 100% arroz/MIDA panameño; detectada contaminación de falsos positivos en backlog (ver log) |

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
