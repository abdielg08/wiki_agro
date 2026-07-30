---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-30
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

## 2026-07-30 08:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-30 08:09
ROUTINE: 13 pendientes revisados — **13/13 falsos positivos, 0 ingestados al wiki**

  Todos los pendientes de esta sesión resultaron ser ruido del pipeline de fetch,
  no noticias de agro panameño. Ninguno generó página nueva en wiki/. Detalle:

  1. `paultan.org` — "MITI working on simplified NCM..." → MIDA = Malaysian
     Investment Development Authority (Malasia), no Panamá.
  2. `sltrib.com` — "Kevin O'Leary data center timeline" → MIDA = Military
     Installation Development Authority (Utah, EE.UU.), no Panamá.
  3. `sltrib.com` — "Box Elder data center opponents..." → mismo MIDA de Utah.
  4. `sltrib.com` — "Utah Gov. Cox issues order..." → mismo MIDA de Utah.
  5. `msn.com` — "Cultural Rules For Staying With Locals Abroad" → menciona de
     pasada el MIDA de Utah; sin relación con Panamá.
  6. `nyfb.org` — "New York Farm Bureau" → gremio agrícola de Nueva York, EE.UU.
  7. `sltrib.com` — "Utah wants to process uranium..." → mismo MIDA de Utah.
  8. `ieeexplore.ieee.org` — "Ambient IoT: Communications Enabling Precision
     Agriculture" → paper técnico 6G genérico, sin mención de Panamá.
  9. `archive.org` — "Catalogue of the diptera of the Americas South of United
     States" → catálogo de zoología (Brasil, 1966), sin relación con Panamá.
  10. `heraldo.es` — "Aragón celebra la sentencia del Supremo..." (bienestar
      porcino) → Aragón, España.
  11. `spa.gov.sa` — "'Reef Saudi', a Successful Program..." → Arabia Saudita.
  12. `whc.unesco.org` — "The Persian Qanat" → Irán, patrimonio UNESCO.
  13. `heraldo.es` — "Luis Biendicho asume la consejería de Medio Ambiente..."
      → Aragón, España (política regional).

  **Causa raíz identificada**: `scripts/fetch_news.py::fetch_ddg_search()`
  (usado por las búsquedas web DDG en `config/sources.yaml: web_searches`,
  p.ej. `prensa_agro` con `site: "prensa.com"`) no aplicaba los dos filtros
  anti-falsos-positivos que sí tienen `fetch_rss()` y el crawl histórico de
  GDELT: `_is_blocked_domain()` (rechazar dominios no-panameños) e
  `_is_panama_related()` (exigir un término geográfico panameño en título/URL).
  El operador `site:` de DuckDuckGo no se respeta de forma confiable — la
  búsqueda `site:prensa.com MIDA ...` devolvió resultados de thestar.com.my,
  sltrib.com, ieeexplore.org, heraldo.es, etc., todos re-etiquetados a ciegas
  como `source: "prensa.com"`, `country: "PA"`, `language: "es"`.
  Además, el acrónimo "MIDA" (término de búsqueda) colisiona con el "Malaysian
  Investment Development Authority" y el "Military Installation Development
  Authority" de Utah — mismo patrón ya documentado en el log del 2026-06-22.

  **Fix aplicado** (`scripts/fetch_news.py`): se agregaron `_is_blocked_domain()`
  e `_is_panama_related()` a `fetch_ddg_search()`, igual que en `fetch_rss()`.
  `_is_panama_related()` ahora exime dominios `.gob.pa` (MIDA/IDIAP/BDA
  oficiales) del requisito de mención explícita de Panamá, ya que el dominio
  gubernamental ya prueba la relevancia.

  **Bug adicional encontrado y corregido** (`scripts/ingest.py`):
  - `mark_all_ingested()` seleccionaba los "primeros N pendientes" ordenando
    por nombre de archivo, mientras que `ingest`/`run_prepare()` los muestra
    ordenados por `prioritize()` (score). Esto causó que la sesión previa
    marcara como ingestados 5 artículos **nunca mostrados ni revisados**
    (Utah uranium, Ambient IoT, Catalogue diptera, Aragón/heraldo, Cultural
    Rules) en vez de los que sí se habían leído. Se corrigió para usar el
    mismo orden de `prioritize()` en ambas funciones.
  - `mark_ingested(url)` fallaba con `AttributeError` en cualquier repo que
    tenga la clave interna `_gdelt_windows` en `processed.json` (una lista,
    no un dict) porque iteraba `processed.items()` directamente en vez de
    `article_entries(processed)`. Esto rompía por completo el comando
    `mark-ingested <url>` que la propia routine genera al final de
    `pending_ingest.md`. Corregido.

  Verificado: ninguna página de `wiki/` menciona contenido de estos falsos
  positivos (thestar.com.my, fox13now, worldbank.org/ext, ieeexplore,
  sltrib.com) — la contaminación quedó contenida en `sources/`/`processed.json`
  y nunca llegó al wiki.

  Los 13 artículos se marcaron `ingested: true` (sin crear páginas) para
  vaciar la cola. `Pendientes de ingesta` = 0 al cierre de esta sesión.
