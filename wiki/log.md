---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-20
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

## 2026-07-20 16:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-20 16:20
ROUTINE: 8 artículos pendientes revisados — 0 sobre agro panameño, 8 falsos positivos
  Falsos positivos detectados (NO ingestados al wiki):
    - paultan.org "MITI working on simplified NCM..." → MITI Malasia, no MIDA Panamá
    - sltrib.com "Box Elder data center opponents..." → MIDA = Utah Military Installation Development Authority
    - sltrib.com "Utah Gov. Cox issues order to protect Great Salt Lake..." → mismo MIDA Utah
    - sltrib.com "Timeline: How the Kevin O'Leary data center plan..." → mismo MIDA Utah
    - sltrib.com "Utah wants to process uranium..." → mismo MIDA Utah
    - msn.com "Cultural Rules For Staying With Locals Abroad" → MIDA Utah mencionado de paso
    - ieeexplore.ieee.org "Ambient IoT: ... Precision Agriculture" → paper técnico genérico, no Panamá
    - archive.org "Catalogue of the diptera of the Americas..." → catálogo taxonómico, no relevante
    - spa.gov.sa "'Reef Saudi', ... Rain-Fed Agriculture" → Arabia Saudita
    - nyfb.org "New York Farm Bureau" → EE.UU.
    - whc.unesco.org "The Persian Qanat" → Irán, patrimonio UNESCO
  Todos marcados `ingested: true` en processed.json (revisados, descartados) sin crear
  contenido en wiki/. Pendientes de ingesta: 11 → 0.

CAUSA RAÍZ identificada: `scripts/fetch_news.py::fetch_ddg_search()` (usado por la fuente
web "prensa_agro" y análogas en `config/sources.yaml`) solo aplicaba `is_agro_relevant()`
(match de keywords genéricos como "MIDA", "agricultura") SIN los guards
`_is_blocked_domain()` / `_is_panama_related()` que sí protegen a `fetch_rss()` y
`fetch_gdelt_batch()`. Además, el operador `site:` de DDGS no se respeta de forma
confiable — la búsqueda "site:prensa.com ..." devolvió resultados de sltrib.com,
thestar.com.my, ieeexplore.ieee.org, archive.org, etc., todos etiquetados como fuente
"prensa.com" en processed.json. Esto explica que las 18 entradas de la fuente
"prensa.com" en `stats` sean en su mayoría (posiblemente todas) ruido global que
coincide con "MIDA" (Malaysia Investment Development Authority / Utah Military
Installation Development Authority) en vez de Panamá.

FIX aplicado: `fetch_ddg_search()` ahora también aplica `_is_blocked_domain()` y
`_is_panama_related()` antes de aceptar un resultado — mismo criterio ya usado en
RSS/GDELT. Bug adicional corregido: `scripts/ingest.py::mark_ingested()` lanzaba
`AttributeError` al iterar `processed.json` porque no saltaba la clave `_gdelt_windows`
(una lista, no un dict) — impedía marcar artículos individuales por URL. Ambos fixes
en este commit.

DIAGNÓSTICO GDELT: 51 ventanas trimestrales completadas (≥45) → backfill 2015-hoy
efectivamente agotado bajo la query actual. 0 artículos de wiki/ provienen de GDELT
hasta ahora (los 6 summaries existentes son semilla manual). Con sourcecountry:PA
+ términos actuales, GDELT no ha devuelto resultados reales aprovechables; requiere
revisión de query/filtro en una sesión futura (posible expansión de términos o
revisión del filtro sourcecountry:PA).
  Fetch GitHub Actions: corrió hoy (commit a41daf4, 13:08 UTC) — mecanismo activo,
  pero sus 2 artículos nuevos fueron ambos falsos positivos (ver arriba).
  Avance medible real (contenido nuevo en wiki/): 0 artículos esta sesión —
  ningún pendiente resultó ser sobre agro panameño.
