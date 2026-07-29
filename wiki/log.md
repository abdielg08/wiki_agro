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

## 2026-07-29 00:00
FALSOS POSITIVOS: 5/5 artículos del lote descartados — NO ingestados (0% falsos positivos, regla innegociable)
  Causa: colisión de la sigla "MIDA" con entidades no panameñas — la fuente prensa.com
  entregó artículos ajenos al agro panameño:
    - https://paultan.org/2026/07/07/miti-working-on-simplified-ncm-customised-incentive-mechanism-to-build-real-local-industrial-capabilities/
      → MITI/MARii Malasia (incentivos industriales), sin relación con MIDA Panamá
    - https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/
      → "MIDA" = Military Installation Development Authority (Utah, EE.UU.), data center Kevin O'Leary
    - https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/
      → mismo MIDA de Utah, oposición a data center en Box Elder County
    - https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/
      → mismo MIDA de Utah, orden del gobernador Cox sobre calidad del aire/Great Salt Lake
    - https://www.msn.com/en-us/news/other/cultural-rules-for-staying-with-locals-abroad/ss-AA1QWARj?ocid=BingNewsVerp
      → artículo de viajes/cultura, menciona demanda contra MIDA de Utah de pasada
  Ninguna página de wiki/ creada ni actualizada. Marcados como ingested=true vía
  mark-all-ingested para despejar la cola de pendientes (no vuelven a aparecer en stats).
  RECOMENDACIÓN: revisar el filtro de la fuente "prensa.com" en el fetch —
  probablemente busca por la palabra clave "MIDA" sin desambiguar Panamá vs. otras
  entidades homónimas (Utah MIDA, y posible ruido de dominios no panameños como
  paultan.org, sltrib.com, msn.com).

## 2026-07-29 08:05
BUG DE HERRAMIENTA DETECTADO: `mark-all-ingested --limit 5` no usa la misma
  selección que `ingest --limit N` (que por defecto usa --strategy score).
  `mark-all-ingested` marca los primeros N pendientes en orden de archivo
  (find_pending), no los N mostrados a Claude. Resultado: de los 5 artículos
  marcados ingested=true, solo 2 coincidían con el lote que Claude realmente
  revisó (Kevin O'Leary timeline, Cultural Rules Abroad). Los otros 3 marcados
  sin revisión previa fueron verificados retroactivamente — también son
  falsos positivos, ninguno es agro de Panamá:
    - https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/
      → mismo "MIDA" de Utah (uranio/energía nuclear)
    - https://ieeexplore.ieee.org/document/10945742
      → paper IEEE "Ambient IoT: Communications Enabling Precision Agriculture",
        genérico global, sin mención de Panamá
    - https://archive.org/details/Cataloguedipter2SaoP
      → catálogo zoológico de dípteros de Brasil (1966/67), no Panamá
  No se perdió contenido real: los 3 confirmados por revisión retroactiva son
  igualmente falsos positivos. RECOMENDACIÓN: corregir `mark_all_ingested()` en
  scripts/ingest.py para que reciba y marque explícitamente las URLs procesadas
  por Claude (o replicar la misma estrategia/orden que `ingest`), en vez de
  recalcular su propia lista con find_pending() en orden de archivo.
  FIX APLICADO: `mark_ingested()` (comando singular) en scripts/ingest.py
  iteraba `processed.items()` sin filtrar las claves internas `_meta` (p.ej.
  `_gdelt_windows`, una lista), y crasheaba en `meta.get("path", "")` al
  encontrar una lista en vez de dict. Corregido para usar `article_entries()`
  igual que el resto de funciones del módulo.

## 2026-07-29 08:12
FALSOS POSITIVOS: 6/6 artículos restantes del lote de 11 pendientes descartados
  — NO ingestados. Los primeros 3 ya documentados arriba (MITI/MARii Malasia,
  Box Elder MIDA Utah, Utah gov MIDA). Los 3 nuevos, verificados sin mención
  alguna de Panamá en el texto completo:
    - https://www.nyfb.org/ → "New York Farm Bureau" (agro de Nueva York, EE.UU.)
    - https://www.spa.gov.sa/en/N2096157 → programa "Reef Saudi" de agricultura
      de secano en Arabia Saudita
    - https://whc.unesco.org/en/list/1506 → "The Persian Qanat", sistema de
      riego ancestral de Irán (patrimonio UNESCO)
  Marcados como ingested=true individualmente vía `mark-ingested <url>` (ya
  corregido) para evitar el bug de selección de `mark-all-ingested`.
  RESULTADO DE LA SESIÓN: 11/11 artículos pendientes eran falsos positivos
  (0 ingestados al wiki, 0% falsos positivos ingestados — regla cumplida).
  Pendientes de ingesta: 0.

## 2026-07-29 08:20
DIAGNÓSTICO DE CAUSA RAÍZ + FIX EN scripts/fetch_news.py:
  Los 11 falsos positivos de hoy venían todos de la fuente etiquetada
  "prensa.com" (18/24 artículos descargados totales), generada por la
  búsqueda web `prensa_agro` (config/sources.yaml → web_searches), que arma
  la consulta `site:prensa.com agropecuario OR agricultura OR ganadería OR
  MIDA OR cosecha Panamá` vía DuckDuckGo (ddgs.news).
  Causa raíz identificada en `fetch_ddg_search()`:
    1. El operador `site:` de DDG NO se respeta de forma confiable en el
       backend — la búsqueda devolvió resultados de dominios totalmente
       ajenos (paultan.org, sltrib.com, nyfb.org, spa.gov.sa,
       whc.unesco.org, ieeexplore.ieee.org, archive.org, thestar.com.my,
       msn.com), pero el código los guardaba con `"source": site` (=
       "prensa.com") sin verificar el dominio real — es decir, TODOS
       aparecían falsamente etiquetados como artículos de La Prensa Panamá.
    2. `is_agro_relevant()` solo exige que aparezca CUALQUIER término de
       `search_terms` (p.ej. "MIDA", "riego", "agricultura") en el texto,
       sin exigir mención de "Panamá" — por lo que coincide con MIDA de Utah
       (Military Installation Development Authority), MITI/MARii de
       Malasia, agricultura de secano en Arabia Saudita, qanats de Irán,
       papers IEEE de agricultura de precisión genérica, etc.
  FIX aplicado (scripts/fetch_news.py):
    - `fetch_ddg_search()` ahora valida que el dominio real del resultado
      (urlparse(url).netloc) coincida con el `site` solicitado antes de
      aceptarlo — descarta silenciosamente los que no coincidan.
    - `is_agro_relevant()` acepta un nuevo parámetro `require_panama`; para
      resultados de búsqueda web (DDG) ahora se exige además que el texto
      contenga "panam" (Panamá/Panama), no solo un término agro genérico.
    - Se agregó log de descartados por dominio/relevancia en consola.
  No se tocó `sources/` (regla #1 de CLAUDE.md) ni el resto de fetchers
  (RSS de IICA/La Prensa, World Bank API, GDELT), que no presentaban este
  problema. Pendiente de validación: próxima corrida de GitHub Actions con
  el código corregido.

## 2026-07-29 08:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
