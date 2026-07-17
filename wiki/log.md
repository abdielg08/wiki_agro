---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2025-05-24
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

## 2026-07-17 00:00
FALSOS POSITIVOS: 5/5 artículos de la ronda de ingesta NO son sobre agro de Panamá — NO ingestados.
  - "MITI working on simplified NCM..." (paultan.org) → Malasia (MITI/MIDA = Ministry of Investment,
    Trade and Industry; MARii), nada que ver con Panamá.
  - "Box Elder data center opponents..." (sltrib.com) → Utah, EE.UU. MIDA = Military Installation
    Development Authority (autoridad de desarrollo de instalaciones militares de Utah).
  - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) → ídem, Utah MIDA.
  - "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com) → ídem, Utah MIDA.
  - "Utah wants to process uranium on the Wasatch Front..." (sltrib.com) → ídem, Utah MIDA.
  Marcados como `ingested` en processed.json (decisión tomada, no reingresan a la cola) pero SIN
  contenido agregado al wiki.

DIAGNÓSTICO: causa raíz identificada — colisión de la sigla "MIDA".
  `config/sources.yaml` usa "MIDA" como término de búsqueda (search_terms.primary) y como parte de
  la query de DuckDuckGo "prensa_agro" ("agropecuario OR agricultura OR ganadería OR MIDA OR cosecha
  Panamá"). "MIDA" también es la sigla de organismos no panameños (Malaysian Investment Development
  Authority / MITI de Malasia, Military Installation Development Authority de Utah), y el filtro
  `site:prensa.com` de DDG News no se está respetando de forma confiable por el backend — los
  resultados venían de paultan.org, sltrib.com, ieeexplore.org, nyfb.org, spa.gov.sa, whc.unesco.org,
  todos re-etiquetados con `source: prensa.com`.
  Se revisaron las 9 URLs pendientes en `sources/articles/`: las 9 (100%) son falsos positivos por
  esta misma causa (el resto — IEEE, NY Farm Bureau, SPA Arabia Saudita, UNESCO Qanat — coinciden con
  términos agro genéricos pero no son sobre Panamá).

FIX APLICADO: `scripts/fetch_news.py::fetch_ddg_search` y `fetch_world_bank` no aplicaban los filtros
  `_is_blocked_domain()` / `_is_panama_related()` que ya existían y se usaban en `fetch_rss` y
  `fetch_gdelt_historical`. Se agregaron los mismos filtros a ambas funciones para exigir al menos un
  término panameño inequívoco (topónimo, no siglas ambiguas) en título/URL antes de aceptar un
  artículo. Esto debería eliminar esta clase de falso positivo en fetches futuros vía GitHub Actions.

BUG ADICIONAL: `scripts/ingest.py::mark_ingested` (comando `mark-ingested` singular) iteraba
  `processed.items()` sin filtrar la clave interna `_gdelt_windows` (una lista), causando
  `AttributeError: 'list' object has no attribute 'get'` en cada invocación — el comando estaba
  roto. Corregido para usar `article_entries(processed)` como el resto del código.

FALSOS POSITIVOS (resto de la cola): los 4 artículos pendientes restantes también se verificaron y
  son falsos positivos por la misma causa raíz (términos agro genéricos sin relación con Panamá):
  - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) → paper 6G.
  - "New York Farm Bureau" (nyfb.org) → gremio agrícola de Nueva York, EE.UU.
  - "'Reef Saudi', a Successful Program..." (spa.gov.sa) → programa agrícola de Arabia Saudita.
  - "The Persian Qanat" (whc.unesco.org) → sitio Patrimonio de la Humanidad en Irán.
  Marcados como `ingested` (sin contenido agregado al wiki). Con esto, Pendientes de ingesta = 0.
