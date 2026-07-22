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

## 2026-07-22 00:00
INGEST: 0 artículos reales — 11/11 pendientes eran falsos positivos (NO ingestados al wiki)
  Ningún artículo trataba sobre agro panameño. Todos etiquetados `source: prensa.com`
  pero ninguna URL pertenece a ese dominio:
    - https://www.spa.gov.sa/en/N2096157 — "Reef Saudi" (programa agrícola de Arabia Saudita)
    - https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/ — MIDA = Military
      Installation Development Authority (Utah), no Ministerio de Desarrollo Agropecuario
    - https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/ — idem (MIDA Utah)
    - https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/ — idem (MIDA Utah)
    - https://www.nyfb.org/ — New York Farm Bureau (agricultura de EE.UU., no Panamá)
    - https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/ — energía nuclear en Utah
    - https://whc.unesco.org/en/list/1506 — Qanats persas (patrimonio UNESCO, riego histórico de Irán)
    - https://paultan.org/2026/07/07/miti-working-on-simplified-ncm-... — MIDA = Malaysian Investment
      Development Authority, artículo sobre incentivos industriales de Malasia
    - https://ieeexplore.ieee.org/document/10945742 — paper IEEE sobre IoT y agricultura de precisión (genérico, sin Panamá)
    - https://www.msn.com/en-us/news/other/cultural-rules-for-staying-with-locals-abroad/... — artículo de viajes, sin relación agro
    - https://archive.org/details/Cataloguedipter2SaoP — catálogo de dípteros de América (entomología, sin relación con Panamá agro)
  Los 11 se marcaron `ingested: true` en processed.json para despejar la cola de pendientes
  (nunca serán válidos; mantenerlos en pendientes bloquearía permanentemente el conteo
  "Pendientes > 0" sin ninguna acción posible del LLM). No se creó ninguna página en wiki/.

CAUSA RAÍZ IDENTIFICADA Y CORREGIDA (scripts/fetch_news.py, fetch_ddg_search):
  1. La búsqueda web `web_searches.prensa_agro` usa `site:prensa.com` + query con
     términos OR (incluye "MIDA"), pero `ddgs.news()` no respeta de forma confiable
     el operador `site:` — devolvía resultados de dominios completamente ajenos
     (sltrib.com, paultan.org, msn.com, archive.org, ieeexplore.ieee.org, etc.)
     y los etiquetaba con `source: "prensa.com"` sin verificar el dominio real.
  2. `is_agro_relevant()` solo exige una coincidencia de substring con la lista
     `search_terms` (p.ej. "MIDA", "agricultura", "riego") sin exigir ningún
     término de contexto Panamá — acrónimos ambiguos como "MIDA" (existe también
     en Malasia y Utah) pasan el filtro con cualquier fuente global.
  FIX aplicado: `fetch_ddg_search()` ahora descarta cualquier resultado cuyo
  dominio real (`urlparse(url).netloc`) no contenga el `site` configurado,
  antes de aplicar el filtro de keywords. Esto elimina el 100% de los falsos
  positivos de esta sesión (ninguno pertenecía a prensa.com).
  Pendiente de monitorear en próximas corridas de GitHub Actions.

DIAGNÓSTICO GDELT: 52 ventanas en total en `_gdelt_windows` (processed.json), pero
  solo 37 son ventanas trimestrales reales del backfill (2017-03-30 → 2026-06-17);
  las otras 15 son ventanas incrementales diarias recientes (2026-06-18 en adelante).
  GAP REAL: 2015-01-01 → 2017-03-29 (~9 ventanas trimestrales) nunca se completaron.
  El backfill histórico NO cubre aún el rango objetivo completo (2015-02-19 → hoy) —
  contradice la entrada de metrics.md del 2026-06-22 que asumía "backfill agotado".
  No se pudo probar la causa en este entorno (proxy bloquea salida a
  api.gdeltproject.org con 403); queda para validar en la próxima corrida real de
  GitHub Actions (fetch_gdelt_historical() en scripts/fetch_news.py, que itera
  desde 2015-01-01 según config/sources.yaml).

## 2026-07-22 08:05
INGEST: 11 artículos marcados como ingestados por sesión Claude Code
