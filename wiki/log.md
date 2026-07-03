---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-03
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

## 2026-07-03 00:02
INGEST: 5 artículos revisados, 0 ingestados, 5 FALSOS POSITIVOS detectados (0 ingestados al wiki)
  Ninguno trata sobre agro panameño. NO se creó ni modificó ninguna página de wiki/.
  Causa raíz: colisión de palabra clave "MIDA" — el fetch capturó noticias sobre la
  "Military Installation Development Authority" de Utah (EE.UU.), homónimo del
  Ministerio de Desarrollo Agropecuario de Panamá, más un artículo genérico de
  "New York Farm Bureau" (agricultura de EE.UU., no de Panamá).
  Artículos rechazados:
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19)
      → MIDA = Military Installation Development Authority (Utah), no MIDA-Panamá
    - "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27)
      → mismo caso, MIDA-Utah / data center, no agro
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
      → MIDA-Utah, calidad del aire/agua en Utah, no Panamá
    - "Utah wants to process uranium on the Wasatch Front..." (sltrib.com, 2025-06-13)
      → MIDA-Utah (Military Installation Development Authority), energía nuclear, no agro
    - "New York Farm Bureau" (nyfb.org, 2026-06-17)
      → agricultura de Nueva York, EE.UU., no de Panamá
  Acción: marcados como ingested=true en sources/processed.json (vía mark-all-ingested)
  para sacarlos de la cola de pendientes; NO se generó contenido de wiki para ninguno.
  Recomendación: agregar filtro de dominio (excluir sltrib.com, nyfb.org y otros no-.pa
  sin relación con Panamá) o desambiguación de "MIDA" en scripts/fetch_news.py para
  reducir la tasa de falsos positivos en fetches futuros.

## 2026-07-03 00:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-03 00:10
INGEST: 1 artículo revisado, 0 ingestados, 1 FALSO POSITIVO detectado (0 ingestados al wiki)
  - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa, 2026-06-24)
    → Programa agrícola de Arabia Saudita (Reef Saudi / SPA), sin relación con Panamá. No se
    creó ni modificó ninguna página de wiki/.
  Causa raíz: el fetch capturó noticia agrícola genérica sin filtro geográfico Panamá.
  Acción: marcado como ingested=true en sources/processed.json (vía mark-all-ingested;
  `mark-ingested <url>` falla con AttributeError por la clave especial `_gdelt_windows`
  —lista, no dict— en processed.json, ver scripts/ingest.py:145) para sacarlo de la cola
  de pendientes.
  BUG DETECTADO: `python wiki_agro.py mark-ingested <url>` rompe con
  "AttributeError: 'list' object has no attribute 'get'" porque itera
  processed.items() sin excluir la clave `_gdelt_windows`. `mark-all-ingested` no
  tiene este problema (usa article_entries() que sí filtra). Reportado para fix futuro.

## 2026-07-03 00:02
INGEST: 1 artículos marcados como ingestados por sesión Claude Code

## 2026-07-03 00:20
DIAGNÓSTICO + FIX: causa raíz de falsos positivos identificada y corregida
  Pendientes = 0 tras la ingesta de esta sesión (0 artículos reales agregados
  al wiki — los 6 pendientes eran 100% falsos positivos, ver entradas arriba).
  Hallazgo: GitHub Actions SÍ corre a diario (última corrida 2026-07-02) y SÍ
  trae artículos, pero 13/19 artículos descargados en total (13/13 de los no-
  semilla) son falsos positivos — 0% de utilidad real desde la carga semilla
  del 2026-05-24.
  Causa raíz: `fetch_ddg_search()` en `scripts/fetch_news.py` NO aplicaba los
  filtros `_is_blocked_domain()` / `_is_panama_related()` que sí tienen
  `fetch_rss()` y `fetch_gdelt_batch()` desde el fix del 2026-06-22 (commit
  c032e62). Además etiquetaba el campo "source" con el nombre de la fuente de
  config (p.ej. "prensa.com") en vez del dominio real del resultado devuelto
  por DuckDuckGo — esto ocultaba que la búsqueda `site:prensa.com` estaba
  devolviendo resultados de sltrib.com, thestar.com.my, fox13now.com, nyfb.org
  y spa.gov.sa (DDG no impone estrictamente el calificador site: en su API de
  noticias). La keyword "MIDA" en la query `web_searches.prensa_agro` colisiona
  con "Military Installation Development Authority" (Utah, EE.UU.) y
  "Malaysian Investment Development Authority" (Malasia).
  Fix aplicado: `fetch_ddg_search()` ahora aplica `_is_blocked_domain(url)` y
  `_is_panama_related(title, url)` antes de aceptar un resultado, igual que
  `fetch_rss()`/`fetch_gdelt_batch()`, y usa `_url_domain(url)` real para el
  campo "source" en vez del nombre de config. Ver scripts/fetch_news.py.
  Backfill GDELT: 43/~46 ventanas completadas, cobertura continua desde
  2017-03-30 hasta 2026-07-01. Gap real pendiente: 2015-02-19 → 2017-03-29
  (~8 ventanas al inicio del rango, nunca fetchadas) — es la prioridad #1 del
  backfill histórico.
  wiki/metrics.md actualizado con estas cifras.
