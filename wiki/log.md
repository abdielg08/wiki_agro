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

## 2026-07-13 08:03
INGEST: 5 artículos pendientes revisados — 5 FALSOS POSITIVOS, 0 ingestados
  Ninguno de los 5 artículos es sobre agro panameño. NO se ingestó ninguno
  (regla CLAUDE.md: 0% falsos positivos es innegociable):
    1. "Box Elder data center opponents..." (sltrib.com, 2026-05-27)
       → sobre un data center en Utah; "MIDA" = Military Installation
         Development Authority (Utah), no el Ministerio de Desarrollo
         Agropecuario de Panamá
    2. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
       → misma confusión de acrónimo "MIDA" (Utah)
    3. "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com, 2026-05-19)
       → misma confusión de acrónimo "MIDA" (Utah)
    4. "Utah wants to process uranium on the Wasatch Front..." (sltrib.com, 2025-06-13)
       → misma confusión de acrónimo "MIDA" (Utah)
    5. "The Persian Qanat" (whc.unesco.org, 2026-07-07)
       → sistema de riego persa antiguo (Irán); "agricultural" coincidió
         como substring de la palabra clave "agricultura"

  DIAGNÓSTICO DE CAUSA RAÍZ: los 5 artículos vinieron de fetch_ddg_search()
  (búsqueda DDG configurada como "prensa_agro", site: prensa.com) en
  scripts/fetch_news.py. Esa función solo llamaba is_agro_relevant() y NO
  aplicaba los guards _is_blocked_domain()/_is_panama_related() que sí usan
  fetch_rss() y fetch_gdelt_batch() desde la auditoría del 2026-06-22. El
  filtro "site:prensa.com" de DDG no se respeta de forma confiable, por lo
  que la búsqueda trajo resultados de sltrib.com y whc.unesco.org
  etiquetados incorrectamente con source="prensa.com" y country="PA"
  hardcodeados.

  FIX APLICADO: scripts/fetch_news.py — fetch_ddg_search() ahora aplica
  _is_blocked_domain() y _is_panama_related() (título/URL/cuerpo), igual
  que fetch_rss() y fetch_gdelt_batch(). Esto debería eliminar esta clase
  de falso positivo en corridas futuras del fetch DDG.

  Los 5 artículos se marcaron como `ingested: true` en sources/processed.json
  vía `mark-all-ingested` para sacarlos de la cola de pendientes (no se creó
  contenido de wiki para ninguno).

## 2026-07-13 08:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-13 08:15
BUG ENCONTRADO Y CORREGIDO: mark_all_ingested() marcaba artículos distintos
a los que `ingest` mostró y Claude revisó.
  Causa: `ingest`/run_prepare() selecciona artículos con prioritize() (orden
  por score, filtrable por año/fuente), mientras que mark_all_ingested()
  llamaba find_pending() directamente (orden alfabético por nombre de
  archivo) — dos selecciones potencialmente distintas para el mismo --limit.
  Efecto observado esta sesión: el primer `mark-all-ingested --limit 5`
  marcó como ingestado un artículo nunca revisado
  ("New York Farm Bureau", https://www.nyfb.org/, source=prensa.com,
  2026-06-17) mientras dejaba pendientes 2 artículos que SÍ había revisado
  y descartado como falsos positivos (Persian Qanat, Reef Saudi). Riesgo:
  en una corrida con artículos reales de Panamá, este bug podría marcar
  como "ingestado" (y por tanto nunca más mostrado) un artículo real sin
  que Claude lo haya procesado — pérdida silenciosa de contenido.
  Fix: scripts/ingest.py — mark_all_ingested() ahora lee las URLs
  directamente de pending_ingest.md (el mismo archivo que Claude ve) en
  vez de recomputar find_pending() con un orden distinto.

  Revisión del artículo recién descubierto "New York Farm Bureau"
  (nyfb.org): organización agrícola del estado de Nueva York, EE.UU. — NO
  es sobre agro panameño. FALSO POSITIVO #6, no ingestado (ya quedó
  `ingested: true` en processed.json por el bug de arriba, pero sin
  contenido creado en wiki/; documentado aquí para que quede registro).

  Artículo 2/2 revisado: "'Reef Saudi', a Successful Program Based on
  Rain-Fed Agriculture" (https://www.spa.gov.sa/en/N2096157, 2026-06-24) —
  programa de agricultura de secano en Arabia Saudita. NO es sobre agro
  panameño. FALSO POSITIVO #7, no ingestado.
  Ambos falsos positivos también vinieron de fetch_ddg_search() sin el
  guard de Panamá (mismo root cause que los 5 documentados arriba;
  cubiertos por el fix ya aplicado en scripts/fetch_news.py).

  Total esta sesión: 7 artículos pendientes revisados, 7 falsos positivos,
  0 ingestados al wiki. Cola de pendientes: 0.

## 2026-07-13 08:05
INGEST: 2 artículos marcados como ingestados por sesión Claude Code

## 2026-07-13 08:30
DIAGNÓSTICO AVANZADO: 3 días sin artículos nuevos en sources/articles/
  (última descarga real: 2026-07-10, hoy: 2026-07-13) → señal de alarma
  del CLAUDE.md activada. Revisado en orden:

  1. ¿Corrió GitHub Actions? SÍ, corre diario y en verde (revisado con la
     API de GitHub Actions): runs del 2026-07-10, 07-11 y 07-12 todos
     "completed / success". El workflow SÍ se está ejecutando — el
     problema NO es que Actions dejó de correr.
  2. Ventanas GDELT: 37/~46 ventanas trimestrales históricas completadas
     (2017-Q1 → 2026-Q1), MÁS una ventana móvil "hoy" que avanzó día a
     día hasta el 2026-07-09 (dio el artículo del 07-10) y luego se
     detuvo. Confirmado con los logs del job del 2026-07-12
     (run 29191567085): las 8 ventanas trimestrales de 2015-01-01 a
     2016-12-28 (justo el inicio del rango objetivo 2015-02-19) y la
     ventana móvil actual (2026-06-18→hoy) fallan TODOS los días con
     `GET blocked (403/429)` o timeout de conexión contra
     api.gdeltproject.org — nunca se marcan como completadas y se
     reintentan sin éxito en cada corrida. Los RSS (IICA, La Prensa)
     devolvieron 0 entradas ese día y las búsquedas DDG de sitios
     oficiales (mida.gob.pa, idiap.gob.pa, bda.gob.pa, fao.org,
     bancomundial.org, iica.int) devolvieron "No results found".
  3. Conclusión: no es un bug de nuestro código ni de la config — es
     bloqueo/rate-limit intermitente de la API pública de GDELT contra
     las IPs de GitHub Actions, específicamente en las primeras
     ventanas que se solicitan en cada corrida (las 8 más antiguas,
     2015-2016, siempre al inicio del loop) y en la ventana móvil más
     reciente. Esto significa que el backfill de 2015-2016 — el inicio
     mismo del rango objetivo del wiki — lleva semanas sin poder
     avanzar, no por falta de datos sino por bloqueo de red persistente.
  Recomendación para una futura sesión: agregar backoff/jitter entre
  reintentos de GDELT dentro de fetch_gdelt_historical(), o priorizar
  esas 8 ventanas antiguas en una corrida manual con más tiempo entre
  llamadas, ya que actualmente compiten por el mismo rate-limit que la
  ventana móvil reciente y ninguna de las dos progresa.

  Además, esta sesión corrigió dos bugs de código (ver 2026-07-13 08:15):
    - fetch_ddg_search() sin guard de Panamá → causaba los 7 falsos
      positivos de hoy.
    - mark_all_ingested() marcaba artículos distintos a los revisados.
  Ningún bug nuevo en el pipeline de GDELT/RSS — el 0-artículos de estos
  3 días es enteramente atribuible al bloqueo de red de GDELT descrito
  arriba.
