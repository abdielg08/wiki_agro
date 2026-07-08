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

## 2026-07-08 00:00
INGEST: 6 artículos pendientes revisados — los 6 son FALSOS POSITIVOS, ninguno ingestado al wiki
  Artículos rechazados (no tratan sobre agro panameño):
    - "Timeline: Kevin O'Leary data center" (sltrib.com, Utah, EE.UU.) — "MIDA" = Military
      Installation Development Authority de Utah, NO Ministerio de Desarrollo Agropecuario
    - "Box Elder data center opponents" (sltrib.com, Utah, EE.UU.) — mismo MIDA de Utah
    - "Utah Gov. Cox issues order... data centers" (sltrib.com, Utah, EE.UU.) — mismo MIDA de Utah
    - "Utah wants to process uranium... nuclear energy" (sltrib.com, Utah, EE.UU.) — mismo MIDA de Utah
    - "'Reef Saudi'... Rain-Fed Agriculture" (spa.gov.sa, Arabia Saudita) — agricultura, pero de
      Arabia Saudita, no Panamá
    - "New York Farm Bureau" (nyfb.org, EE.UU.) — organización agrícola de Nueva York, no Panamá
  Los 6 fueron marcados `ingested=true` en processed.json (mark-ingested) para sacarlos de la
  cola de pendientes, sin crear ninguna página en wiki/.

DIAGNÓSTICO — causa raíz de los falsos positivos:
  Los 6 (y de hecho los 13 artículos etiquetados fuente "prensa.com" en sources/, un 100%)
  vinieron de la búsqueda web `prensa_agro` (DuckDuckGo, config/sources.yaml web_searches),
  cuya query usa el término "MIDA" sin exigir mención de Panamá. La función
  `fetch_ddg_search()` en scripts/fetch_news.py NO aplicaba los filtros
  `_is_panama_related()` / `_is_blocked_domain()` que sí usan `fetch_rss()` y
  `fetch_gdelt_batch()`, y además el operador `site:` de DDG no se respeta estrictamente
  (resultados de sltrib.com, spa.gov.sa, nyfb.org, thestar.com.my, fox13now.com,
  worldbank.org, ieeexplore.ieee.org se colaron bajo `site:prensa.com`). Cada resultado se
  guardaba con `source: "prensa.com"` y `country: "PA"` fijos, sin verificar el dominio real.

FIX APLICADO (scripts/fetch_news.py, fetch_ddg_search):
  1. Rechaza resultados cuyo dominio no contiene el `site` configurado (el filtro site: de
     DDG no es confiable).
  2. Rechaza dominios bloqueados vía `_is_blocked_domain()`.
  3. Exige mención de Panamá (`_is_panama_related()`) en título/URL para fuentes
     internacionales (oirsa.org, fao.org, iica.int, bancomundial.org) — no para dominios
     inherentemente panameños (prensa.com, mida.gob.pa, idiap.gob.pa, bda.gob.pa), que ya
     quedan acotados por el chequeo de dominio.

BUG SECUNDARIO CORREGIDO (scripts/ingest.py, mark_ingested):
  `mark_ingested()` iteraba sobre `processed.items()` crudo (incluye la clave interna
  `_gdelt_windows`, una lista) en vez de `article_entries(processed)`, causando
  `AttributeError: 'list' object has no attribute 'get'` cada vez que se ejecutaba
  `mark-ingested <url>` individual (el comando que pending_ingest.md sugiere ejecutar
  artículo por artículo). `mark-all-ingested` no tenía este bug porque ya filtraba
  correctamente. Corregido para usar `article_entries()`.

DIAGNÓSTICO — Estado del fetch (GitHub Actions):
  Verificado vía GitHub API: el workflow wiki_daily.yml SÍ corrió exitosamente todos los
  días 2026-07-05, 07-06 y 07-07 (status=success), pero no generó commits porque no
  encontró artículos nuevos en ninguna fuente esos 3 días — 5 días consecutivos sin
  artículos nuevos reales contando desde 07-03 (supera el umbral de 3 días de CLAUDE.md).
  Causa: ventanas GDELT completadas = 45 (backfill histórico alcanzó el presente, no hay
  más ventanas trimestrales disponibles hasta que pase más tiempo real) + RSS de IICA y
  La Prensa devolvieron 0 entradas relevantes esos días. La búsqueda DDG era, de hecho, la
  única fuente que seguía produciendo "artículos nuevos" recientes — pero 100% falsos
  positivos, ahora corregidos. Se espera que tras el fix, DDG aporte 0 o pocos artículos
  reales por día hasta que se amplíen las queries o se agreguen fuentes RSS activas.
  Total páginas wiki: 20 (8 topics, 3 entities, 6 summaries)
