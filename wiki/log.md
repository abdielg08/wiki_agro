---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-16
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

## 2026-07-16 00:00
ROUTINE: 9 pendientes revisados — 9/9 FALSOS POSITIVOS (0 ingestados al wiki)

  **Falsos positivos documentados** (ninguno trata sobre agro de Panamá):
    1. "MITI working on simplified NCM..." — https://paultan.org/2026/07/07/miti-working-on-simplified-ncm-customised-incentive-mechanism-to-build-real-local-industrial-capabilities/
       Es sobre MITI/MIDA/MARii de **Malasia** (incentivos industriales), no MIDA Panamá.
    2. "Box Elder data center opponents..." — https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/
       MIDA = Military Installation Development Authority de **Utah, EE.UU.**
    3. "Utah Gov. Cox issues order..." — https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/
       Mismo MIDA de Utah; nada que ver con Panamá.
    4. "Timeline: Kevin O'Leary data center..." — https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/
       Mismo caso, Utah.
    5. "Utah wants to process uranium..." — https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/
       Mismo MIDA de Utah (energía nuclear).
    6. "The Persian Qanat" — https://whc.unesco.org/en/list/1506
       Ficha UNESCO sobre sistema de riego ancestral en **Irán**.
    7. "New York Farm Bureau" — https://www.nyfb.org/
       Gremio agrícola de **Nueva York, EE.UU.**
    8. "'Reef Saudi'..." — https://www.spa.gov.sa/en/N2096157
       Programa de agricultura de secano en **Arabia Saudita**.
    9. "Ambient IoT: Communications Enabling Precision Agriculture" — https://ieeexplore.ieee.org/document/10945742
       Paper técnico IEEE sobre 6G/IoT, sin mención de Panamá.

  Los 9 se marcaron `ingested: true` (vía `mark-ingested`) para sacarlos de pendientes,
  sin crear páginas de wiki — cumpliendo la regla de 0% falsos positivos.

  **Causa raíz identificada y corregida** (`scripts/fetch_news.py`):
    Los 9 (y 7 más ya marcados `ingested:true` en sesiones previas — thestar.com.my ×4,
    fox13now.com, ieeexplore.org/11018750, worldbank.org/development-topics) llegaron
    todos por la fuente `web_searches: prensa_agro` (`fetch_ddg_search`), que arma la
    consulta a DuckDuckGo como `site:prensa.com <query>`. DDG **no respeta de forma
    confiable el operador `site:`** en su backend de noticias, así que la búsqueda
    devolvía resultados de cualquier dominio que matcheara términos genéricos como
    "MIDA" o "agricultura" — sin el filtro de dominio/Panamá que sí tiene `fetch_rss`
    (`_is_panama_related`, `_is_blocked_domain`).
    Impacto real: **16 de los 22 artículos descargados hasta hoy (73%) vinieron de
    esta fuente rota, y los 16 fueron falsos positivos.** Desde la semilla manual del
    2026-05-24, el backfill automático no ha aportado NINGÚN artículo real al wiki
    (0 avance neto en ~7 semanas de fetches diarios).
    **Fix aplicado**: se agregó `_domain_matches_site()` en `scripts/fetch_news.py` y
    se aplica en `fetch_ddg_search()` junto con `_is_blocked_domain()`, forzando
    localmente la restricción de dominio que DDG ignora.

  **Bug adicional corregido** (`scripts/ingest.py`):
    `mark_ingested()` iteraba `processed.items()` directo, sin filtrar la clave interna
    `_gdelt_windows` (una lista), causando `AttributeError` en cada llamada. Se cambió
    a `article_entries(processed).items()` (mismo helper que ya usa `mark_all_ingested`).

  **Diagnóstico de backfill GDELT**:
    `_gdelt_windows` en processed.json tiene 49 ventanas marcadas completas (≥45 →
    "rango agotado" según CLAUDE.md). Cobertura real: trimestres 2017-Q2 a 2026-Q2
    completos; **faltan 2015-02-19 → 2017-Q1** (~9 ventanas) para cumplir el objetivo
    de cobertura 2015→hoy. Además hay 13 ventanas con fecha de inicio fija
    (2026-06-18) y fin incremental día a día — parecen redundantes/duplicadas y no
    ventanas trimestrales reales; no se tocaron en esta sesión.
    Se intentó `fetch-historical --years 2015-2016 --mode gdelt` desde esta sesión:
    falló con `ProxyError 403` — confirma que GDELT solo es alcanzable desde runners
    de GitHub Actions (como ya advertía el propio workflow), no desde sesiones locales
    de Claude Code. **Acción pendiente para el usuario**: disparar manualmente el
    workflow `Wiki Agropecuario — Crawl Histórico 15 Años` con `years=2015-2017,
    mode=gdelt` para cerrar el hueco de cobertura inicial.

  Total páginas wiki: 20 (sin cambios — 0 artículos reales para ingestar esta sesión)
  Artículos descargados: 22 | Ingestados (procesados): 22 | Pendientes: 0
