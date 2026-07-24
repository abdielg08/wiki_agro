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

## 2026-07-24 00:00
FALSOS POSITIVOS: 5/5 artículos del lote pendiente NO ingestados — 0% falsos positivos mantenido
  Causa raíz: colisión de siglas "MIDA" — el fetch capturó artículos que mencionan MIDA en
  sentidos ajenos al Ministerio de Desarrollo Agropecuario de Panamá:
    - MITI/Malaysia's "New Customised Incentive Mechanism" → MIDA = Malaysian Investment
      Development Authority (paultan.org, 2026-07-07)
    - Kevin O'Leary data center timeline (Utah) → MIDA = Military Installation Development
      Authority, Utah (sltrib.com, 2026-05-19)
    - Box Elder data center opponents (Utah) → MIDA = Military Installation Development
      Authority, Utah (sltrib.com, 2026-05-27)
    - Utah Gov. Cox order on data centers → MIDA = Military Installation Development
      Authority, Utah (sltrib.com, 2026-05-29)
    - "Cultural Rules For Staying With Locals Abroad" → menciona la demanda contra MIDA de
      Utah, sin relación con agro (msn.com, 2026-03-07)
  Verificación: 0 menciones de "Panama"/"Panamá" en el texto de los 5 artículos.
  Acción: ninguno ingestado al wiki; los 5 se marcarán como ingestados en processed.json para
  no reprocesarlos, pero no generaron páginas ni entradas en index.md.
  Recomendación: el fetcher (GDELT/keyword search) debería filtrar por término compuesto
  "MIDA Panamá" o similar, o exigir co-ocurrencia con "Panama"/"Panamá" en el texto, para
  evitar que la sigla MIDA capture entidades homónimas de Malasia y Utah.

## 2026-07-24 08:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-24 08:10
BUGFIX: `mark-all-ingested --limit N` no coincidía con el lote mostrado por `ingest --limit N`
  Causa: `ingest` selecciona por score de prioridad (prioritize.py), mientras que
  `mark_all_ingested` usa `find_pending()` ordenado por nombre de archivo — listas distintas.
  Efecto observado: de los 5 falsos positivos del batch anterior, `mark-all-ingested --limit 5`
  solo marcó 2 (Kevin O'Leary, Cultural Rules); los otros 3 (MITI, Box Elder, Utah Gov. Cox)
  reaparecieron como pendientes en la siguiente llamada a `ingest`.
  Fix aplicado: usar `mark-ingested <url>` por artículo individual (coincidencia exacta),
  en vez de `mark-all-ingested --limit N`, al documentar falsos positivos.
  Bug adicional corregido en scripts/ingest.py: `mark_ingested()` iteraba sobre
  `processed.items()` crudo, incluyendo la clave interna `_gdelt_windows` (una lista, no un
  dict), causando `AttributeError: 'list' object has no attribute 'get'`. Se cambió a iterar
  sobre `article_entries(processed)` (ya usado en el resto del módulo para excluir claves `_meta`).

## 2026-07-24 08:12
FALSOS POSITIVOS (continuación): 3 artículos adicionales NO ingestados — 0% falsos positivos mantenido
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" → Arabia Saudita,
      sin relación con Panamá (spa.gov.sa, 2026-06-24)
    - "The Persian Qanat" → sistema de riego ancestral de Irán, ficha UNESCO, sin relación
      con Panamá (whc.unesco.org, 2026-07-07)
    - "New York Farm Bureau" → gremio agrícola de Nueva York, EE.UU., sin relación con Panamá
      (nyfb.org, 2026-06-17)
  Verificación: 0 menciones de "Panama"/"Panamá" en el texto de los 3 artículos.
  Nota: los 3 artículos tienen `country: "PA"` en sources/articles/*.json a pesar de no ser
  sobre Panamá — el campo `country` del fetcher no es confiable como filtro por sí solo.
  Total falsos positivos detectados hoy: 8/8 artículos pendientes. Ninguno generó páginas de
  wiki. Cola de pendientes: 0.
  Recomendación adicional: además del fix de "MIDA Panamá", considerar que el `country: PA`
  del fetch (posiblemente heurística de dominio o de query GDELT) está produciendo falsos
  positivos sistemáticos y debería revisarse en el pipeline de sources/.

## 2026-07-24 08:20
FIX (root cause): parcheado el leak real que produjo los 8 falsos positivos de hoy.
  Diagnóstico: los 8 artículos venían de `fetch_ddg_search()` en scripts/fetch_news.py,
  entrada de config `web_searches: prensa_agro` (site: "prensa.com", query: "agropecuario
  OR agricultura OR ganadería OR MIDA OR cosecha Panamá"). Dos causas combinadas:
    1. El operador OR de DDG no distribuye "Panamá" sobre todos los términos — solo el
       último término ("cosecha Panamá") lo exige; "MIDA", "agricultura", etc. quedan sin
       filtro geográfico.
    2. El prefijo `site:prensa.com` no es respetado de forma confiable por `ddgs.news()`,
       por lo que llegaron resultados de dominios totalmente ajenos (paultan.org, sltrib.com,
       spa.gov.sa, whc.unesco.org, nyfb.org, msn.com) — todos etiquetados incorrectamente
       con `source: "prensa.com"` (bug de metadata: `source: site or name` en fetch_ddg_search).
  Comparación: `fetch_rss()` y `fetch_gdelt_batch()` en el mismo archivo YA tenían las
  guardas `_is_blocked_domain()` + `_is_panama_related()` (con comentario explícito:
  "Only unambiguous geographic/national terms — no acronyms (MIDA matches Malaysia too)").
  Solo `fetch_ddg_search()` carecía de ellas — inconsistencia entre fetchers del mismo módulo.
  Fix aplicado en scripts/fetch_news.py:
    - `fetch_ddg_search()`: se agregaron las mismas guardas `_is_blocked_domain(url)` y
      `_is_panama_related(title, url)` que ya usan `fetch_rss` y `fetch_gdelt_batch`.
    - `_is_panama_related()`: se amplió para aceptar también dominios con ccTLD de Panamá
      (`.pa`, p.ej. mida.gob.pa, bda.gob.pa, idiap.gob.pa) aunque el título no diga
      "Panamá" explícitamente — evita falsos negativos en fuentes oficiales panameñas.
  Validación (backtest, sin acceso a Actions en esta sesión):
    - Los 8 falsos positivos de hoy: BLOQUEADOS por el fix (MITI/Malaysia, Kevin O'Leary/
      Box Elder/Utah Gov Cox — Utah MIDA, Cultural Rules Abroad, Reef Saudi, Persian Qanat,
      NY Farm Bureau).
    - 3 artículos reales del wiki (MIDA arroz, BDA crédito, IDIAP semilla): siguen PASANDO.
  Alcance del fix: solo `fetch_ddg_search()` y el helper compartido `_is_panama_related()`.
  No se tocó `is_agro_relevant()` genérico (usado también por RSS) para no arriesgar
  falsos negativos no probados en esa vía — sin datos suficientes en esta sesión para
  validar ese cambio más amplio.
  Bug de metadata (`source` mal etiquetado en fetch_ddg_search) documentado pero NO corregido
  en esta sesión — no afecta la tasa de falsos positivos, queda como mejora futura de trazabilidad.

## 2026-07-24 08:25
FALSOS POSITIVOS (corrección de conteo): 3 artículos adicionales marcados como ingestados sin
  haber sido revisados individualmente al momento — se detectó y corrige aquí.
  Causa: la primera llamada de esta sesión a `mark-all-ingested --limit 5` (antes de descubrir
  el bug de desalineación documentado a las 08:10) marcó los primeros 5 pendientes por orden
  de archivo (find_pending), que NO coincidían exactamente con los 5 mostrados en
  pending_ingest.md (ordenados por score de prioridad). De esos 5, 2 coincidían con los ya
  revisados (Kevin O'Leary, Cultural Rules) y 3 eran artículos distintos, no inspeccionados:
    - "Utah wants to process uranium on the Wasatch Front for nuclear energy" → de nuevo
      MIDA = Military Installation Development Authority, Utah — sin relación con Panamá
      (sltrib.com, 2025-06-12)
    - "Ambient IoT: Communications Enabling Precision Agriculture" → paper académico IEEE
      sobre 6G y agricultura de precisión, genérico, sin mención de Panamá (ieeexplore.ieee.org,
      documento 10945742)
    - "Catalogue of the diptera of the Americas South of United States" → catálogo de
      entomología (Secretaria da Agricultura, aparente origen brasileño), sin relación con
      Panamá (archive.org, 2016-05-13)
  Verificación posterior (esta entrada): 0 menciones de "Panama"/"Panamá" en los 3 artículos.
  Ninguno generó páginas de wiki — la marca como `ingested: true` fue correcta en el resultado
  (no deben reprocesarse), pero no se documentó en su momento. Se corrige aquí.
  **Total falsos positivos reales de la sesión de hoy: 11/11 artículos pendientes procesados.
  0 ingestados al wiki. 0% falsos positivos mantenido.**
  Lección para la routine: al usar `mark-all-ingested --limit N`, verificar SIEMPRE la lista
  completa de URLs efectivamente marcadas (leer sources/processed.json después) en vez de
  asumir que coincide con el lote mostrado en pending_ingest.md — confirmado root cause a
  las 08:10 de hoy.
