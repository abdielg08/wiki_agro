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

## 2026-07-30 00:00
FALSOS POSITIVOS: 5/5 artículos del lote `ingest --limit 5` rechazados — 0% ingestados
  Ninguno trata sobre agro panameño. Todos vienen de la fuente `prensa_agro` (búsqueda
  DDG configurada con `site:prensa.com`), pero ninguno es de prensa.com:
    - paultan.org — MITI/MIDA de Malasia (incentivos industriales)
    - sltrib.com (x2) — MIDA = "Military Installation Development Authority" de Utah,
      centro de datos de Kevin O'Leary
    - sltrib.com — orden del gobernador de Utah sobre Great Salt Lake (menciona MIDA de Utah)
    - msn.com — artículo de viajes ("Cultural Rules For Staying With Locals Abroad")
  Causa raíz encontrada y corregida en `scripts/fetch_news.py::fetch_ddg_search`:
  el backend de noticias de DDG (ddgs.news) NO respeta el operador `site:`, así que la
  query `site:prensa.com agropecuario OR ... OR MIDA OR cosecha Panamá` devuelve
  resultados globales que solo calzan por la palabra suelta "MIDA" (que en Malasia,
  Utah, etc. es una sigla no relacionada). Auditoría de los 23 artículos ya guardados
  bajo `source: prensa.com`: **0/23 son realmente de prensa.com** (heraldo.es, sltrib.com,
  thestar.com.my, ieeexplore.org, msn.com, worldbank.org, etc.) — el filtro de dominio/
  Panamá que ya existe para RSS y GDELT (`_is_blocked_domain`, `_is_panama_related`)
  nunca se aplicaba a `fetch_ddg_search`. Se agregó ahí para prevenir recurrencia.
  Los 5 artículos se marcan como ingestados (sin páginas wiki) vía `mark-all-ingested`
  para vaciar la cola; no se creó contenido en wiki/ para ninguno.
  Pendiente para el usuario: revisar si los 23 artículos históricos de `prensa.com`
  (source label) deben limpiarse/re-etiquetarse — no se tocó `sources/` en esta sesión.

## 2026-07-30 16:05
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-30 16:10
FIX: bug en `mark-all-ingested`/`mark-ingested` (scripts/ingest.py)
  `mark_ingested()` iteraba `processed.items()` directo, incluyendo la clave
  interna `_gdelt_windows` (una lista, no un dict) → `AttributeError` en cada
  llamada, y ademas `mark-all-ingested --limit N` usa el orden de
  `find_pending()` (alfabético por archivo), que NO coincide con el orden por
  score que usa `ingest --limit N` para armar `pending_ingest.md`. Resultado:
  la primera corrida de esta sesión marcó 5 artículos DISTINTOS a los 5 que
  realmente se revisaron (solo 1/5 coincidía). Se revirtió ese cambio
  (`git checkout -- sources/processed.json`) y se marcaron los 5 artículos
  correctos uno por uno con `mark-ingested <url>`. Se corrigió `mark_ingested()`
  para usar `article_entries(processed)` (ya usado en `find_pending`/
  `mark_all_ingested`), que excluye las claves internas `_meta`.
  Recomendación: mientras no se sincronice el orden de ambos comandos, usar
  `mark-ingested <url>` individual en vez de `mark-all-ingested --limit N`
  después de un `ingest --limit N`.

## 2026-07-30 16:20
DIAGNÓSTICO AVANZADO: cobertura GDELT 2015-2016 nunca completada
  `_gdelt_windows` tiene 59 entradas: 2017-2025 con 4/4 ventanas cada año
  (36 total, todas exitosas), pero **2015 y 2016 con 0/8** — nunca se
  completó ni una sola ventana para esos dos años, que son justamente el
  inicio del objetivo de cobertura (2015-02-19). Causa: en
  `fetch_gdelt_historical()` (scripts/fetch_news.py), si `fetch_gdelt_batch`
  devuelve `None` (error de red) la ventana NO se marca completa y el error
  solo se imprime en consola (no queda registrado en ningún log persistente),
  así que si GDELT falla consistentemente para 2015-2016 (posible límite de
  antigüedad de la API), esas ventanas se reintentan en silencio cada día sin
  jamás avanzar ni alertar. Además, las 23 entradas restantes son ventanas
  del "tramo final" de 2026 casi duplicadas día a día (mismo inicio ~2026-06-18,
  fin creciente) — no pierden cobertura pero inflan la lista sin necesidad,
  porque el límite `end = hoy-1` cambia cada día y esa última ventana (aún no
  cerrada por 90 días) genera una clave nueva cada vez en vez de extender la
  anterior.
  Ninguna ventana GDELT (2017-2026) produjo artículos nuevos en `sources/`
  (0 artículos con fuente tipo GDELT en `processed.json`) — el filtro Panamá
  ya se aplica ahí (`_is_blocked_domain`/`_is_panama_related`), así que no es
  un problema de falsos positivos, sino de cobertura real casi nula.
  Acción recomendada para el usuario: correr `python wiki_agro.py fetch --mode
  gdelt` manualmente y observar el error real para 2015-2016 (posible rate
  limit distinto o el endpoint no indexa noticias tan antiguas).

## 2026-07-30 16:11
LINT: 20 páginas revisadas, 55 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:12, no_index:1
