---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-11
---

# Log de Actividad

> Registro cronológico append-only de ingestas, consultas y operaciones de mantenimiento.

---

## 2025-05-24 00:00
INIT: Wiki Agropecuario de Panamá inicializado
  Estructura: topics/, entities/, summaries/, index.md, log.md
  Metodología: Karpathy LLM Wiki (3 capas: sources → wiki → schema)
  Cobertura objetivo: noticias agropecuarias de Panamá 2015–2025
  Fuentes configuradas: MIDA, IDIAP, BDA, IICA, FAO, La Prensa, Panamá América, TVN, La Estrella
  Método histórico: GDELT API (gratuito, sin clave, cobertura 2015–2025)

## 2026-05-24 13:38
LINT: 8 páginas revisadas, 39 issues encontrados
  frontmatter:0, huérfanas:0, broken_links:39, stale:0, no_index:0

## 2026-05-24 15:04
LINT: 8 páginas revisadas, 39 issues encontrados
  frontmatter:0, huérfanas:0, broken_links:39, stale:0, no_index:0

## 2026-05-24 16:00
INGEST: 6 artículos semilla procesados (sesión Claude Code — metodología Karpathy)
  Artículos:
    - 20230915_mida_produccion-arroz-panama-2023 → summaries/ + topics/arroz.md actualizado
    - 20180620_laprensaeco_gusano-cogollero-crisis-maiz-2018 → summaries/ + topics/maiz.md creado + topics/plagas_enfermedades.md actualizado
    - 20160301_tvnnoticias_sequia-azuero-nino-2015-2016 → summaries/ + topics/cambio_climatico.md actualizado
    - 20220410_iica_platano-banano-exportaciones-fusarium → summaries/ + topics/platano_banano.md actualizado + topics/plagas_enfermedades.md actualizado
    - 20210815_bda_credito-agropecuario-pandemia-2020-2021 → summaries/ + topics/credito_financiamiento.md creado + entities/bda.md actualizado
    - 20240305_mida_politica-agropecuaria-mulino-2024 → summaries/ + topics/politicas_agropecuarias.md creado + entities/mida.md actualizado
  Páginas creadas: maiz.md, credito_financiamiento.md, politicas_agropecuarias.md
  Páginas actualizadas: arroz.md, plagas_enfermedades.md, cambio_climatico.md, platano_banano.md, mida.md, bda.md
  Summaries: 6 nuevos archivos en wiki/summaries/

## 2026-05-24 22:58
INGEST: 6 artículos marcados como ingestados por sesión Claude Code

## 2026-05-27 00:00
MAINTENANCE: Verificación automática de artículos pendientes
  Sin artículos pendientes — 6/6 artículos ya ingestados
  Total páginas wiki: 19 (8 topics, 3 entities, 6 summaries, 2 overview)
  Fuentes con cobertura: MIDA (2), TVNNoticias (1), LaPrensaEco (1), BDA (1), IICA (1)

## 2026-07-11 08:00
ROUTINE: 7 pendientes revisados — 0 ingestados, 7 falsos positivos (0 páginas nuevas)
  Ninguno de los 7 artículos pendientes trataba de agro panameño. NO se ingestó ninguno:
    - https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/
      → Centro de datos en Utah. Coincidencia por acrónimo "MIDA" = Military
        Installation Development Authority (Utah), no Ministerio de Desarrollo
        Agropecuario de Panamá.
    - https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/
      → Mismo caso: oposición a centro de datos en Box Elder County, Utah (MIDA-Utah).
    - https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/
      → Orden del gobernador de Utah sobre calidad de aire/agua vs. centros de datos
        (MIDA-Utah).
    - https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/
      → Acuerdo de procesamiento de uranio en Utah (Utah National Guard + MIDA-Utah).
    - https://www.nyfb.org/
      → Página institucional de "New York Farm Bureau" (agricultura de EE.UU.,
        no Panamá).
    - https://whc.unesco.org/en/list/1506
      → "The Persian Qanat" — sistema de riego histórico de Irán (UNESCO), sin
        relación con Panamá.
    - https://www.spa.gov.sa/en/N2096157
      → Programa "Reef Saudi" de agricultura de secano en Arabia Saudita, sin
        relación con Panamá.
  Los 7 se marcaron `ingested: true` en sources/processed.json (vía mark-ingested)
  para sacarlos de la cola de pendientes sin crear contenido de wiki — igual que
  los 7 falsos positivos ya documentados en la sesión 2026-06-22.

DIAGNÓSTICO DE CAUSA RAÍZ: los 7 casos vienen de `fetch_ddg_search()` en
scripts/fetch_news.py (búsqueda "prensa_agro": `site:prensa.com agropecuario OR
agricultura OR ganadería OR MIDA OR cosecha Panamá` vía DuckDuckGo News). El
operador `site:` de DDG no se respeta de forma confiable y la búsqueda devuelve
resultados globales que matchean términos ambiguos como "MIDA" o "agricultura"
sin relación real con Panamá. A diferencia de `fetch_rss()` y `fetch_gdelt_batch()`
en el mismo archivo, `fetch_ddg_search()` NO aplicaba los filtros
`_is_blocked_domain()` / `_is_panama_related()` ya existentes en el código.

FIX APLICADO (scripts/fetch_news.py):
  - fetch_ddg_search() ahora aplica _is_blocked_domain() y _is_panama_related()
    antes de aceptar un resultado, igual que fetch_rss() y fetch_gdelt_batch().
FIX APLICADO (scripts/fetch_historical.py — mismo bug, backfill aún no usado):
  - fetch_gdelt_window() ahora exige mención de Panamá en la query GDELT
    (_PANAMA_QUERY_SUFFIX) y filtra por _is_blocked_domain()/_is_panama_related()
    en los resultados, igual que fetch_gdelt_batch() en fetch_news.py.
FIX APLICADO (scripts/ingest.py):
  - mark_ingested() fallaba con AttributeError al iterar processed.json porque
    no saltaba la clave interna `_gdelt_windows` (lista, no dict). Se agregó
    `isinstance(meta, dict)` guard.

Pendientes tras esta sesión: 0/20. Artículos reales ingestados con contenido de
wiki: 6 (sin cambios — 0 artículos nuevos y relevantes esta sesión).

## 2026-07-11 08:05
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
