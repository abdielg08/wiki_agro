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

## 2026-07-12 00:00
FALSOS POSITIVOS: 7/7 artículos pendientes rechazados — 0 ingestados al wiki (tasa falsos positivos 0% respetada)
  Todos venían de la fuente `prensa.com` (búsqueda DDG configurada como `web_searches: prensa_agro`,
  ver `config/sources.yaml`), no de RSS ni GDELT.
  Artículos rechazados:
    - sltrib.com/.../kevin-oleary-data-center-timeline — MIDA = Military Installation Development
      Authority (Utah), no Ministerio de Desarrollo Agropecuario de Panamá
    - sltrib.com/.../box-elder-data-center-opponents — ídem (MIDA de Utah)
    - sltrib.com/.../utah-governor-issues-order-protect — ídem (MIDA de Utah)
    - sltrib.com/.../utah-nuclear-energy-state — ídem (MIDA de Utah)
    - spa.gov.sa/en/N2096157 "Reef Saudi" — agricultura de secano, pero de Arabia Saudita, no Panamá
    - nyfb.org — New York Farm Bureau, agro de EE.UU., no Panamá
    - whc.unesco.org/en/list/1506 — sistema de qanats en Irán, no Panamá
  Causa raíz identificada: `fetch_ddg_search()` en `scripts/fetch_news.py` nunca recibió los filtros
  `_is_blocked_domain()` / `_is_panama_related()` que el fix del 2026-06-22 (#20) sí aplicó a los
  fetchers de RSS y GDELT. Además, `site:` en DDGS no es un filtro estricto — DDG devuelve resultados
  de dominios no relacionados que solo coinciden por palabra clave ("MIDA", "agricultura").
  Fix aplicado esta sesión: `fetch_ddg_search()` ahora exige que el dominio del resultado contenga el
  `site` configurado, aplica `_is_blocked_domain()`, y exige `_is_panama_related()` en título/URL/cuerpo
  antes de aceptar un resultado — igual que RSS y GDELT.
  Bug adicional corregido: `mark_ingested()` en `scripts/ingest.py` fallaba con
  `AttributeError: 'list' object has no attribute 'get'` al iterar `processed.json` porque no excluía
  la clave interna `_gdelt_windows` (una lista). Ahora usa `article_entries()` como el resto del código.
  Los 7 artículos se marcaron `ingested: true` + `false_positive: true` en `sources/processed.json`
  para no volver a aparecer en la cola de pendientes, sin agregar contenido al wiki.
  Pendientes de ingesta tras esta sesión: 0

DIAGNÓSTICO AVANZADO (Paso 4):
  Último commit de fetch automático (GitHub Actions, wiki_daily.yml, cron diario 11:00 UTC):
  2026-07-10 (88389fe, "1 artículos nuevos descargados" — resultó ser whc.unesco.org/en/list/1506,
  uno de los 7 falsos positivos de esta sesión). Sin commits de fetch en 07-11 ni 07-12 (hoy) — el
  workflow diario normalmente commitea todos los días aunque encuentre 0 artículos nuevos ("chore
  (sources): 0 artículos nuevos"), así que la ausencia total de commit en dos días sugiere que la
  Action no corrió o falló antes de llegar al commit, no que corrió y no encontró nada. Requiere
  revisar el historial de runs de Actions para confirmar. Aún por debajo del umbral de alarma de 3
  días consecutivos sin artículos nuevos en `sources/articles/`.
  Ventanas GDELT completadas: 48 (`_gdelt_windows` en processed.json) — por encima del umbral de 45
  que CLAUDE.md marca como "rango de fechas agotado, necesita expansión". El backfill histórico
  2015→hoy probablemente ya cubrió las ventanas configuradas; siguiente paso sería ampliar el rango
  o los términos de búsqueda en `wiki_historical.yml` / `fetch_historical.py` si se busca más
  cobertura, o confirmar que 48 ventanas ya cubren 2015-02-19→hoy y el backfill está esencialmente
  completo.
