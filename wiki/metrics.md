---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-17
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 49 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos reales | 2 (fetch trajo basura, no artículos reales) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-15 (trajo 1 artículo "nuevo" — resultó falso positivo)
Resultado 2026-07-17   : 9/9 artículos pendientes eran falsos positivos (100%)
Causa identificada     : fetch_ddg_search() y fetch_world_bank() en scripts/fetch_news.py NO
                         aplicaban los filtros _is_blocked_domain()/_is_panama_related() que sí
                         usan fetch_rss() y fetch_gdelt_historical(). La query DDG "site:prensa.com
                         ... MIDA ..." no es honrada de forma confiable por el backend de ddgs,
                         y "MIDA" colisiona con siglas de organismos no panameños (Malaysia
                         MITI/MIDA, Utah Military Installation Development Authority), trayendo
                         artículos de paultan.org, sltrib.com, ieeexplore.org, nyfb.org, spa.gov.sa,
                         whc.unesco.org mal etiquetados con source:prensa.com.
Fix aplicado 2026-07-17 : Se agregaron los mismos filtros a fetch_ddg_search() y fetch_world_bank()
                         (scripts/fetch_news.py). También se corrigió scripts/ingest.py::mark_ingested
                         (comando CLI roto por no filtrar la clave interna _gdelt_windows).
Estado post-fix         : Pendiente validación en próxima corrida Actions.
Ventanas GDELT          : 49 completadas ≥ 45 estimadas → rango de fechas agotado, considerar
                         expandir gdelt.date_range en config/sources.yaml (actualmente 2015-01-01
                         a 2027-12-31) o verificar si ya cubre todo el histórico disponible.
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
| 2026-07-17 | 0 | 0 | 9/9 pendientes = falsos positivos (colisión sigla "MIDA"). Fix en fetch_ddg_search/fetch_world_bank + fix de mark_ingested roto |

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
