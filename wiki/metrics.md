---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** (9 nuevos detectados hoy, ver nota) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 73 | 45 (2015→hoy) — meta superada |
| Días sin artículos nuevos | 0 (2026-08-23: 0 nuevos, pero fetch corrió) | máx 3 antes de diagnosticar |

> **Nota 2026-08-23**: "0 nuevos" no cuenta como falla del fetch — el problema es calidad,
> no cantidad. La fuente `prensa.com` (DDG search) sigue trayendo ~100% falsos positivos
> por falta de filtro Panamá. Ver `wiki/log.md` 2026-08-23 08:15 para diagnóstico completo
> y recomendación de fix en `scripts/fetch_news.py::fetch_ddg_search()`.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-23 (commit previo a esta sesión)
Resultado               : Fetch SÍ está trayendo artículos (30 descargados, 73 ventanas
                          GDELT completadas) — el fetch en sí funciona.
Problema actual         : Calidad, no cantidad. scripts/fetch_news.py::fetch_ddg_search()
                          (fuente "prensa.com" vía DuckDuckGo) NO aplica el filtro
                          _is_panama_related() que sí usan fetch_rss() y fetch_gdelt_batch().
                          Resultado: ~100% de los 17 pendientes de esta sesión eran de
                          fuera de Panamá (Utah, Malasia, España/Aragón, Brasil, Arabia
                          Saudita, papers académicos genéricos) — coinciden por palabras
                          agro genéricas o por la sigla "MIDA"/"MITI" usada por entidades
                          de otros países.
Bug relacionado          : mark-all-ingested (find_pending, orden por fecha de archivo)
                          no usa el mismo orden que ingest (prioritize.py, orden por score),
                          por lo que puede marcar artículos distintos a los mostrados en
                          pending_ingest.md. Ver wiki/log.md 2026-08-23 08:15 para detalle.
Fix pendiente            : (1) aplicar _is_panama_related(title, url) dentro de
                          fetch_ddg_search() antes de yield; (2) corregir el campo "source"
                          para reflejar el dominio real, no el site: buscado; (3) alinear
                          el orden de find_pending() con prioritize.py.
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
| 2026-08-23 | 0 reales (9 falsos positivos marcados) | 8 | Root cause: fetch_ddg_search() sin filtro Panamá. Ver log.md |

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
