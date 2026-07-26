---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-26
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 15 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 55 / ~45-65 estimadas | cobertura 2010/2015 → hoy |
| Días sin artículos nuevos en sources/ | 3 (2026-07-23, 24, 25) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-25 (wiki_daily.yml, cron diario 11:00 UTC)
Resultado              : 0 artículos nuevos — 3er día consecutivo en 0
                         (2026-07-23, 2026-07-24, 2026-07-25)
Causa identificada     : DOS bugs en el pipeline de descarga, no un fallo del
                         Action en sí (el workflow SÍ corre y hace commit diario):
                         1. fetch_ddg_search() (scripts/fetch_news.py) filtraba
                            solo por is_agro_relevant() (coincidencia de término,
                            ej. "MIDA") pero NO por _is_panama_related(), a
                            diferencia del fetcher RSS. Resultado: de los 11
                            artículos pendientes acumulados, 11/11 (100%) eran
                            falsos positivos de fuera de Panamá (Utah MIDA,
                            Malasia MITI, granjas de NY, Arabia Saudita, Irán).
                         2. mark_ingested() (scripts/ingest.py) lanzaba
                            AttributeError al iterar la clave no-artículo
                            "_gdelt_windows" (lista) de processed.json,
                            impidiendo marcar artículos ya revisados.
                         3. Ventanas GDELT en 55 (por encima del estimado de
                            ~45-65 para 2010/2015→hoy): el backfill histórico
                            por trimestre está cerca de agotar el rango
                            configurado; seguirá sin traer artículos "nuevos"
                            de años ya cubiertos, solo of nuevas fechas.
Fix aplicado (sesión 2026-07-26): se agregó _is_panama_related(title, url) en
                         fetch_ddg_search(); se blindó mark_ingested() contra
                         valores no-dict en processed.json.
Estado post-fix        : Pendiente validación en próxima corrida de wiki_daily.yml
                         (cron 11:00 UTC). Si sigue en 0 artículos reales tras el
                         fix, revisar próximo si RSS (IICA/La Prensa) sigue activo
                         y si conviene ejecutar wiki_historical.yml con un rango
                         de años expandido (ej. 2026-2027) para el tramo reciente.
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
| 2026-07-26 | 0 reales (11 revisados, 11 falsos positivos) | 0 | Fix de causa raíz: filtro Panamá faltante en fetch_ddg_search() + bug en mark_ingested() |

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
