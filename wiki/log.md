---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-17
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

## 2026-07-17 16:06
ROUTINE: 9 artículos pendientes revisados — 9/9 FALSOS POSITIVOS (0 ingestados)

  **Falsos positivos rechazados (NO ingestados, marcados como revisados):**
    - "MITI working on simplified NCM..." (paultan.org) → Malasia (MITI/MIDA malasios), no Panamá
    - "Box Elder data center opponents..." (sltrib.com) → Utah, MIDA = Military Installation
      Development Authority (agencia de Utah, no el MIDA panameño)
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) → Utah
    - "Timeline: Kevin O'Leary data center..." (sltrib.com) → Utah
    - "Utah wants to process uranium..." (sltrib.com) → Utah, MIDA = Military Installation
      Development Authority
    - "The Persian Qanat" (whc.unesco.org) → sistema de riego histórico de Irán
    - "New York Farm Bureau" (nyfb.org) → agricultura de Nueva York, EE.UU.
    - "'Reef Saudi'..." (spa.gov.sa) → agricultura de secano en Arabia Saudita
    - "Ambient IoT: Precision Agriculture" (ieeexplore.ieee.org) → paper técnico sin país específico

  **Causa raíz identificada (CRÍTICA):** los 9 artículos estaban etiquetados con fuente
  "prensa.com" en sources/, pero sus URLs reales apuntaban a sltrib.com, paultan.org,
  unesco.org, nyfb.org, spa.gov.sa e ieeexplore.ieee.org — ninguno es prensa.com.
  `scripts/fetch_news.py::fetch_ddg_search()` construye la búsqueda DDG con el operador
  `site:prensa.com`, pero el operador `site:` de DDGS().news() no se hace cumplir de forma
  confiable y el código nunca validaba el dominio real de los resultados. Tampoco aplicaba
  los filtros `_is_blocked_domain()` / `_is_panama_related()` que sí usan el fetcher de RSS
  y el de GDELT (bug pre-existente, asimétrico entre fetchers).
  Con el término de búsqueda ambiguo "MIDA" (coincide con el MIDA panameño, la Military
  Installation Development Authority de Utah y el Malaysian Investment Development
  Authority), el filtro `is_agro_relevant()` (simple substring match) dejaba pasar
  cualquier artículo que mencionara "agriculture"/"agricultural"/"MIDA" en cualquier país.

  **Impacto:** los 16 artículos "prensa.com" acumulados desde 2026-05-24 (fuente de las
  9 revisadas hoy más 7 falsos positivos previos referenciados en metrics.md) son en su
  mayoría/totalidad producto de este mismo bug. El pipeline automático NO ha aportado
  contenido real al wiki desde los 6 artículos semilla del 2026-05-24 — 0% de señal útil,
  100% falsos positivos en todo el contenido vía DDG desde entonces.

  **Fix aplicado (scripts/fetch_news.py, fetch_ddg_search):**
    1. Rechaza resultados cuyo dominio real no contenga el `site` configurado.
    2. Aplica `_is_blocked_domain()` (TLDs no-Panamá conocidos).
    3. Aplica `_is_panama_related()` (exige término geográfico panameño en título/URL),
       igual que ya hacían fetch_rss() y fetch_gdelt_historical().

  **Bug adicional encontrado y corregido:** `mark_ingested` (comando singular, en
  scripts/ingest.py) iteraba processed.items() sin filtrar las claves internas
  (`_gdelt_windows`, una lista) y lanzaba AttributeError al intentar `.get()` sobre ella.
  Corregido para usar `article_entries()` como ya hace `mark_all_ingested`.

  Pendientes tras esta sesión: 0. Ingestados reales: 0 (todo lo pendiente era falso
  positivo). Ver diagnóstico de fetch en wiki/metrics.md.

## 2026-07-17 16:08
LINT: 20 páginas revisadas, 54 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:11, no_index:1
