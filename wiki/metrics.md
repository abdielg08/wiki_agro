---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) + 2017-2018 (backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 52 (solo 4 son backfill histórico real; ver nota) | 45 (2015→hoy) |
| Días sin artículos nuevos (reales, no falsos positivos) | desde 2026-05-24 (semilla) | máx 3 antes de diagnosticar |

> **Nota sobre ventanas GDELT**: de las 52 registradas, solo 4 corresponden al
> backfill histórico real (`wiki_historical.yml`) y cubren únicamente
> 2017-03-30 → 2018-06-27. Las ~48 restantes son ventanas del fetch diario
> incremental (`wiki_daily.yml`), no del backfill. El workflow histórico
> nunca se ha disparado manualmente — ver `wiki/log.md` 2026-07-22 16:10.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida wiki_daily.yml  : 2026-07-21 — 0 artículos nuevos
Últimos 4 días                 : 07-18:0, 07-19:0, 07-20:2, 07-21:0 nuevos
wiki_historical.yml            : NUNCA ejecutado (workflow_dispatch manual,
                                  requiere acción humana) — backfill 2015→hoy
                                  prácticamente sin iniciar

Causa raíz de falsos positivos (2026-07-22): fetch_ddg_search() en
scripts/fetch_news.py no aplicaba _is_blocked_domain() ni
_is_panama_related() antes de guardar resultados de búsqueda DuckDuckGo,
a diferencia de fetch_rss() y fetch_gdelt_batch(). El operador "site:" de
la query no es respetado de forma confiable por el backend de ddgs,
así que resultados de dominios no-panameños (Malasia, Utah, Arabia
Saudita, IEEE, archive.org) se guardaban etiquetados con source:"prensa.com"
(el nombre configurado de la búsqueda, no el dominio real).
Fix aplicado           : se agregaron ambos filtros a fetch_ddg_search()
                          (commit de esta sesión)
Estado post-fix         : pendiente validación en próxima corrida de
                          wiki_daily.yml
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
| 2026-07-22 | 0 | 0 | 11 revisados, 11/11 falsos positivos (colisión "MIDA" + fetch_ddg_search sin filtro Panamá). 3 bugs de tooling encontrados y corregidos: mark_all_ingested (selección incorrecta), mark_ingested (crash en _gdelt_windows), fetch_ddg_search (sin filtro geográfico) |

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
