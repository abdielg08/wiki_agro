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
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** ⚠️ meta incumplida hoy (ver diagnóstico) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 49 / ~46 estimadas | 45 (2015→hoy) — rango cubierto |
| Días sin artículos nuevos reales (no-FP) | ≥54 (desde 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con datos : 2026-07-17 (9 artículos nuevos en sources/, los 9 = falsos positivos)
Resultado ingesta real   : 0 artículos nuevos al wiki en esta sesión
Ventanas GDELT           : 49 completadas — el backfill 2015→hoy vía GDELT está
                            esencialmente agotado en cobertura de ventanas.
Causa raíz identificada  : fetch_ddg_search() (scripts/fetch_news.py) — la fuente
                            web_searches "prensa_agro" (site:prensa.com) usa una
                            query OR amplia ("agropecuario OR agricultura OR
                            ganadería OR MIDA OR cosecha Panamá") contra la API de
                            noticias de DuckDuckGo. El operador `site:` de DDG NO
                            se aplica de forma confiable en ddgs.news(), y a
                            diferencia de fetch_rss(), esta función NO llamaba a
                            _is_panama_related() ni _is_blocked_domain() antes de
                            aceptar un resultado. Consecuencia: cualquier artículo
                            mundial que matcheara UN SOLO término OR (p.ej. "MIDA"
                            o "agricultura") se colaba, etiquetado incorrectamente
                            con source="prensa.com" aunque su URL real fuera
                            paultan.org, sltrib.com, ieeexplore.ieee.org,
                            whc.unesco.org, nyfb.org o spa.gov.sa.
Fix aplicado (hoy)       : scripts/fetch_news.py::fetch_ddg_search() ahora aplica
                            _is_blocked_domain(url) y _is_panama_related(title, url)
                            — mismo guard que fetch_rss() ya usaba. Sin validar aún
                            en una corrida real de fetch (próxima corrida de
                            GitHub Actions confirmará si esto reduce los FP a 0).
Bugs de tooling hallados : (1) `wiki_agro.py mark-ingested <url>` falla con
                            AttributeError al iterar `_gdelt_windows` (lista) en
                            processed.json — no filtra con article_entries().
                            (2) `mark-all-ingested --limit N` selecciona por orden
                            alfabético de archivo (find_pending), NO por score
                            (prioritize) como hace `ingest --limit N` — los N
                            artículos no coinciden. Ambos pendientes de fix; ver
                            wiki/log.md 2026-07-17 para detalle.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Calculado desde `_gdelt_windows` en `sources/processed.json` (49 ventanas registradas):

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | **0** | ⚠️ **Sin cubrir — hueco en el backfill** |
| 2016 | **0** | ⚠️ **Sin cubrir — hueco en el backfill** |
| 2017 | 4 | Completo |
| 2018 | 4 | Completo |
| 2019 | 4 | Completo |
| 2020 | 4 | Completo |
| 2021 | 4 | Completo |
| 2022 | 4 | Completo |
| 2023 | 4 | Completo |
| 2024 | 4 | Completo |
| 2025 | 4 | Completo |
| 2026 | 13 | Sobre-cubierto (ventanas cortas repetidas de catch-up reciente, no trimestrales) |
| **TOTAL** | **49** | **2015–2026 nominal, pero 2015 y 2016 están en 0 ventanas** |

> **Hallazgo de esta sesión**: pese a que el conteo total (49) supera la estimación
> de ~45-46, el desglose por año muestra que **2015 y 2016 nunca se corrieron** —
> todas las ventanas registradas empiezan en 2017 en adelante. El conteo agregado
> ocultaba este hueco. Próxima prioridad de backfill: `python scripts/fetch_historical.py
> --mode gdelt --years 2015-2016` (o el flag equivalente) para cerrar 2015-02-19 → 2016-12-31.
> Cero de los artículos descargados hasta ahora vía estas ventanas resultaron en
> ingesta real al wiki en esta sesión — todos eran ruido de otras fuentes (ver
> diagnóstico de causa raíz arriba, no relacionado a GDELT sino a fetch_ddg_search).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-17 | 0 | 0 | 9/9 pendientes = falsos positivos (colisión MIDA/agricultura genérica vía fetch_ddg_search). Fix aplicado en scripts/fetch_news.py. Hueco de backfill 2015-2016 detectado. |

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
