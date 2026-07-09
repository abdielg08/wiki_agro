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

## 2026-07-09 00:00
FALSOS POSITIVOS: 5/5 artículos del lote `ingest --limit 5` rechazados — 0% ingestados
  NINGUNO de los 5 artículos trata sobre agro panameño. Todos vienen mal
  clasificados con `country: PA` pese a no mencionar Panamá ni una vez
  (verificado con grep sobre `summary_raw` de cada JSON fuente).
    - 20260519_prensacom_news-2026-05-19-kevin-oleary-data-center-timeline.json
      → Utah (EE.UU.), centro de datos de Kevin O'Leary. Colisión de palabra
        clave "MIDA" = Military Installation Development Authority (Utah),
        NO Ministerio de Desarrollo Agropecuario de Panamá.
    - 20260527_prensacom_news-2026-05-27-box-elder-data-center-opponents.json
      → Utah, oposición al centro de datos de Box Elder. Misma colisión "MIDA".
    - 20260529_prensacom_news-environment-2026-05-29-utah-governor-issues-order-prote.json
      → Utah, orden del gobernador Cox sobre Great Salt Lake / calidad del aire.
        Misma colisión "MIDA".
    - 20250613_prensacom_news-environment-2025-06-12-utah-nuclear-energy-state.json
      → Utah, procesamiento de uranio para energía nuclear. Misma colisión "MIDA"
        (Utah National Guard + Military Installation Development Authority).
    - 20260624_prensacom_en-n2096157.json
      → Arabia Saudita, programa "Reef Saudi" de agricultura de secano. Es
        agricultura real pero de otro país — colisión por palabra clave
        genérica "agriculture", no por "MIDA".
  Acción: NO se creó contenido en wiki/. Los 5 se marcan `ingested: true` en
  `processed.json` vía `mark-all-ingested` para vaciar la cola sin volver a
  presentarlos.
  Patrón recurrente: este es el mismo problema de colisión de acrónimo "MIDA"
  documentado en PR #20 (fix: calidad GDELT + métricas + reset backfill).
  El filtro de ingesta / clasificación de `country` sigue sin desambiguar
  "MIDA" (Panamá) de "MIDA" (Utah, EE.UU.) — requiere un fix en el pipeline
  de fetch/scoring, no solo en la revisión manual de cada lote.

## 2026-07-09 00:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-09 00:10
BUG DETECTADO Y CORREGIDO: `mark-all-ingested --limit N` marcaba artículos
distintos a los que `ingest --limit N` había mostrado para revisión.
  Causa raíz: `ingest` selecciona el lote por `strategy=score` (prioritize.py),
  pero `mark_all_ingested` recalculaba los pendientes con `find_pending()`
  (orden por nombre de archivo). Ambos órdenes pueden diferir, así que
  `mark-all-ingested` podía marcar como `ingested: true` un artículo que
  Claude Code NUNCA leyó ni revisó.
  Evidencia: al correr `mark-all-ingested --limit 5` tras revisar los 5
  artículos del lote de las 00:00 (4 de Utah + 1 de Arabia Saudita), se marcó
  en su lugar `https://www.nyfb.org/` ("New York Farm Bureau", agro de EE.UU.,
  también mal clasificado como `country: PA`) — un artículo NO revisado —
  y dejó sin marcar el de Arabia Saudita que sí habíamos revisado y
  rechazado. Esto viola la regla de "0% falsos positivos — innegociable"
  porque un artículo puede quedar `ingested: true` sin pasar por la
  verificación humana/LLM del Paso 3.
  FALSO POSITIVO adicional confirmado por revisión retroactiva:
    - 20260617_prensacom_.json (https://www.nyfb.org/) → "New York Farm
      Bureau". 0 menciones de Panamá en el texto. Mismo patrón de
      mal-clasificación `country: PA`. NO se creó contenido en wiki/.
  Fix aplicado en `scripts/ingest.py`: `run_prepare()` ahora persiste el
  lote exacto de URLs mostradas en `sources/.last_ingest_batch.json`;
  `mark_all_ingested()` marca ese lote (no un recálculo independiente) y
  borra el archivo temporal al terminar. Se agregó `sources/.last_ingest_batch.json`
  a `.gitignore`.
  Recomendación pendiente: además del fix de ordering, sigue sin resolverse
  la causa raíz del `country: PA` mal asignado en el fetch/scoring — ver
  entrada anterior sobre colisión de acrónimo "MIDA" (PR #20).
  Bug adicional (menor) descubierto y corregido en la misma sesión:
  `mark_ingested()` (singular, por URL) iteraba `processed.items()` sin
  filtrar `_gdelt_windows` (una lista, no un dict), causando
  `AttributeError: 'list' object has no attribute 'get'` en cualquier
  llamada. Se cambió a `article_entries(processed)`, igual que ya hacía
  `mark_all_ingested()`.

## 2026-07-09 00:15
DIAGNÓSTICO AVANZADO: Pendientes = 0 tras la revisión — 0 días sin
  artículos DESCARGADOS hoy porque el cron aún no corre hoy (cron
  "0 11 * * *" = 11:00 UTC; sesión actual: 00:06 UTC). Revisando runs
  reales de "Wiki Agropecuario — Fetch Diario" vía GitHub Actions API:
    - El workflow SÍ corre todos los días (schedule, completed/success) —
      no hay fallas de cron ni gaps de ejecución.
    - Sin embargo, el último artículo NUEVO real fue el 2026-07-02 (hace 7
      días). Runs de 07-03, 07-04, 07-06, 07-07, 07-08: 0 artículos nuevos.
  Causa raíz confirmada leyendo el log completo del run 2026-07-06
  (id 28798415569, job "Fetch artículos → Commit a sources/"):
    1. RSS (IICA, La Prensa): 0 entradas en ambos feeds.
    2. DDG (ddgs): las 8 búsquedas configuradas devuelven "No results
       found" — sospechoso que TODAS fallen igual, sugiere que las IPs de
       GitHub Actions están bloqueadas/limitadas por DuckDuckGo, no que
       genuinamente no haya resultados.
    3. GDELT: las 9 ventanas más antiguas (2015-01-01 → 2017-03-29, las
       únicas que faltan de las 46 totales) fallan TODAS con
       timeouts/403/429/"Max retries exceeded" — el mismo patrón se repite
       en cada corrida diaria, así que nunca se marcan completas y se
       reintentan indefinidamente sin avanzar. La ventana más reciente aún
       no descargada (2026-06-18 → 2026-07-05) también fue bloqueada con
       "GET blocked (403/429)" en el mismo run.
  Conclusión: no es un problema de configuración de cron ni de código de
  ingesta — es que GDELT (y posiblemente DuckDuckGo) están limitando o
  bloqueando las IPs de datacenter de GitHub Actions casi todos los días,
  dejando el fetch diario funcionalmente vacío salvo corridas ocasionales
  con suerte (ej. 07-02, 1 artículo). El comentario en `wiki_daily.yml`
  ("IPs de GitHub Actions no bloqueadas") ya no refleja la realidad
  observada.
  Recomendaciones (no aplicadas en esta sesión — requieren más
  investigación/pruebas contra la API real):
    a. Agregar backoff/circuit-breaker en `fetch_gdelt_historical()` para
       no gastar ~5 min del budget diario reintentando las mismas 9
       ventanas de 2015-2017 que fallan siempre — dejaría más tiempo para
       la ventana reciente y RSS/DDG.
    b. Evaluar si el crawl histórico 2015-2017 debe moverse por completo al
       workflow manual `wiki_historical.yml` (timeout de 6h) en vez de
       repetirse en el job diario de 30 min.
    c. Revisar por qué las 8 búsquedas DDG fallan uniformemente — podría
       ser un bloqueo de IP o un cambio en la librería `ddgs`.
  Ventanas GDELT completadas: 46/46 posibles con el rango de 90 días desde
  2017-03-30, pero 9 ventanas de 2015-01-01 a 2017-03-29 siguen sin
  completarse — la cobertura NO llega a 2015 como indica el objetivo del
  proyecto, se detiene en 2017-03-30 por el bloqueo persistente descrito
  arriba.

## 2026-07-09 00:09
INGEST: 0 artículos marcados como ingestados por sesión Claude Code
