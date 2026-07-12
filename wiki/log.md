---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-12
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
AUDIT: 7 pendientes revisados — los 7 son FALSOS POSITIVOS, 0 ingestados al wiki

  **Artículos rechazados** (ninguno trata del sector agropecuario panameño):
    1. "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com) — Utah,
       "MIDA" = Military Installation Development Authority (no relacionado a Panamá)
    2. "Box Elder data center opponents..." (sltrib.com) — mismo caso, Utah/MIDA
    3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) — Utah/MIDA
    4. "Utah wants to process uranium... nuclear energy" (sltrib.com) — Utah/MIDA
    5. "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa)
       — agricultura, pero de Arabia Saudita, no Panamá
    6. "New York Farm Bureau" (nyfb.org) — agricultura de EE.UU., no Panamá
    7. "The Persian Qanat" (whc.unesco.org) — sistema de riego de Irán, no Panamá

  Los 7 fueron descargados por `fetch_ddg_search` (búsqueda `prensa_agro`,
  `site:prensa.com ... MIDA ...`) pero NINGUNO proviene realmente de prensa.com.
  Los 7 quedaron marcados con `"source": "prensa.com"` y `"country": "PA"` en
  `processed.json` — metadata incorrecta generada por el fetcher, no por el LLM.

  **Causa raíz identificada** (`scripts/fetch_news.py::fetch_ddg_search`):
  A diferencia de `fetch_rss()` y `fetch_gdelt_batch()` (que sí verifican
  `_is_blocked_domain()` y `_is_panama_related()`), la búsqueda DDG nunca
  validaba que la URL devuelta perteneciera realmente al dominio pedido en
  `site:`. El backend de noticias de DDG no respeta el operador `site:` de
  forma confiable, así que "site:prensa.com" devolvía resultados de dominios
  totalmente ajenos (sltrib.com, spa.gov.sa, nyfb.org, whc.unesco.org) y el
  código los aceptaba etiquetándolos ciegamente como `country: "PA"`.

  **Fix aplicado**: se añadió verificación de dominio (`site.lower() in
  _url_domain(url)`) + `_is_blocked_domain()` en `fetch_ddg_search()`, para que
  solo se acepten resultados que realmente vengan del dominio solicitado.
  Commit incluido en esta sesión.

  **Bug adicional encontrado y corregido**: `mark_ingested()` en
  `scripts/ingest.py` iteraba `processed.items()` sin filtrar la clave interna
  `_gdelt_windows` (una lista, no un dict), causando un `AttributeError` al
  intentar marcar cualquier artículo. Se corrigió para usar
  `article_entries(processed)` como el resto del código base.

  **Acción sobre processed.json**: los 7 se marcaron `ingested: true` (única
  vía disponible para sacarlos de la cola de pendientes) — esto NO significa
  que se haya creado contenido en el wiki para ellos. No existe página,
  summary ni referencia en index.md para ninguno de los 7. Ver tabla de
  falsos positivos acumulados en `wiki/metrics.md`.

  **Hallazgo importante para el usuario**: desde la carga semilla del
  2026-05-24 (6 artículos reales) hasta hoy (7 semanas de fetch diario 3x/día
  vía GitHub Actions), NINGÚN artículo nuevo genuino sobre agro panameño ha
  sido descargado. Los 14 artículos "nuevos" acumulados en ese período
  (7 el 2026-06-22, 7 hoy) fueron el 100% falsos positivos. El wiki sigue
  teniendo exactamente 6 artículos de contenido real.

DIAGNÓSTICO AVANZADO (pendientes = 0 tras el rechazo):
  - Artículos nuevos en sources/articles/ HOY (2026-07-12): 0
    (el workflow de GitHub Actions aún no corre hoy; última corrida fue
    2026-07-11 11:45 UTC, exitosa pero con 0 artículos guardados)
  - Ventanas GDELT completadas: 48 (`_gdelt_windows` en processed.json)
  - GDELT **SÍ está siendo bloqueado activamente**: en la corrida de Actions
    del 2026-07-11 (run 29151485830), CADA ventana intentada (las 8 más
    antiguas sin completar: 2015-01-01 → 2017-03-29, y la ventana más
    reciente 2026-06-18 → 2026-07-10) devolvió timeout o 403/429. Solo las
    ~39 ventanas intermedias (2017-03-30 → 2026-06-17) están completas,
    aparentemente logradas en corridas anteriores antes de toparse con el
    bloqueo persistente.
  - Efecto: el backfill histórico está atascado en sus dos extremos —
    (a) 2015 Q1 a 2017 Q1 nunca logran completarse porque el loop las
    reintenta PRIMERO en cada corrida y GDELT bloquea casi de inmediato;
    (b) la ventana más reciente (contenido más valioso, noticias actuales)
    se intenta AL FINAL de cada corrida, cuando el bloqueo ya está activo,
    así que tampoco progresa.
  - RSS: IICA y La Prensa devolvieron 0 entradas el 2026-07-11 (normal,
    no indica fallo — las fuentes simplemente no publicaron ese día).
  - DDG: las búsquedas a mida.gob.pa, idiap.gob.pa, oirsa.org, fao.org,
    bancomundial.org, iica.int devolvieron "No results found" el 2026-07-11
    (el backend de noticias de ddgs parece no soportar bien `site:` para
    estos dominios — ninguna de estas búsquedas ha producido un artículo
    real ingestado hasta ahora).

  **Próximos pasos recomendados** (no aplicados en esta sesión, requieren
  más diseño/pruebas):
  1. Cambiar el orden de iteración de `fetch_gdelt_historical()` para
     procesar la ventana más reciente primero (o alternar extremos), para
     que el contenido actual no quede sistemáticamente huérfano del bloqueo.
  2. Evaluar si GDELT requiere ahora una clave de API o límites de tasa más
     estrictos que antes — los timeouts/403 son consistentes y persistentes,
     no esporádicos.
  3. Revisar si las búsquedas DDG por dominio (mida.gob.pa, idiap.gob.pa,
     etc.) alguna vez han funcionado — llevan semanas en "No results found".
