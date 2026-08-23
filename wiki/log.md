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

## 2026-08-23 00:12
INGEST: 5/5 artículos revisados — TODOS falsos positivos, 0 ingestados al wiki
  Artículos rechazados (documentados, NO agregados a wiki/):
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org)
      → Coincide solo por "MIDA" = Malaysian Investment Development Authority (agencia
        de MITI, Malasia), no tiene relación con el MIDA panameño (Ministerio de
        Desarrollo Agropecuario).
    - "Box Elder data center opponents hope for a vote..." (sltrib.com)
      → Coincide solo por "MIDA" = Military Installation Development Authority (Utah,
        disputa sobre centro de datos de Kevin O'Leary). No es Panamá.
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com)
      → Mismo MIDA de Utah (Military Installation Development Authority). No es Panamá.
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com)
      → Mismo MIDA de Utah. No es Panamá.
    - "Cultural Rules For Staying With Locals Abroad" (msn.com)
      → Artículo de viajes sin relación agropecuaria; menciona MIDA de Utah de pasada.
  Acción: `mark-all-ingested --limit 5` ejecutado para limpiar la cola de pendientes
  (los 5 quedan marcados `ingested: true` en processed.json, pero SIN página en wiki/).

DIAGNÓSTICO — causa raíz identificada:
  Los 5 (y probablemente los 12 pendientes restantes) provienen de la fuente DDG
  "prensa_agro" (config/sources.yaml, web_searches), que ejecuta una búsqueda
  DuckDuckGo con `site:prensa.com` + keywords ("MIDA" entre ellas). El operador
  `site:` de DDG no se está respetando de forma confiable en `ddgs.news()`, así que
  llegan resultados de dominios totalmente ajenos (sltrib.com, paultan.org, msn.com)
  pero `fetch_ddg_search()` en scripts/fetch_news.py etiquetaba `source` con el valor
  de `site` configurado ("prensa.com") sin validar el dominio real del resultado.
  Además, a diferencia del fetcher RSS (que sí llama `_is_panama_related()`),
  `fetch_ddg_search()` no aplicaba ningún filtro de relevancia geográfica — solo
  keywords genéricas ("MIDA", "agricultura"), que colisionan con entidades
  homónimas fuera de Panamá (Malasia, Utah).

  Revisando processed.json completo: los 17 pendientes actuales son TODOS de fuentes
  no panameñas (Arabia Saudita, Utah, Malasia, Nueva York, UNESCO, IEEE, Aragón/España,
  Brasil, Maine) — mismo patrón. No se ingirió ninguno.

FIX APLICADO (scripts/fetch_news.py, fetch_ddg_search):
  1. Se valida que el dominio real del resultado (`_url_domain(url)`) termine en el
     `site` configurado antes de aceptarlo — descarta resultados fuera de dominio
     aunque DDG los devuelva.
  2. Para búsquedas sin `site` configurado, se añade el filtro `_is_panama_related()`
     ya usado por el fetcher RSS.
  Esto debería eliminar la recurrencia de este patrón de falsos positivos en las
  próximas corridas de GitHub Actions.

## 2026-08-23 00:12
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-23 00:25
BUG DETECTADO Y CORREGIDO — desincronización `ingest` / `mark-all-ingested`:
  Al ejecutar `mark-all-ingested --limit 5` arriba, se marcaron 5 artículos
  DISTINTOS a los 5 que aparecían en `pending_ingest.md` y que ya habían sido
  revisados/documentados como falsos positivos. Causa: `ingest` (comando
  `run_prepare`) selecciona el lote por `strategy="score"` (prioriza fuentes y
  términos como "MIDA"), mientras que `mark-all-ingested` (función
  `mark_all_ingested`) usaba `find_pending()`, que ordena por nombre de archivo
  (fecha). Ambos comandos operan sobre "los primeros N pendientes" pero con
  criterios de orden distintos, así que casi nunca coinciden.
  Además, `mark-ingested <url>` individual fallaba con `AttributeError` porque
  iteraba `processed.items()` sin excluir la clave interna `_gdelt_windows`
  (una lista, no un dict de metadata de artículo).

  Artículos marcados por error (NO revisados originalmente, pero verificados
  ahora — también son falsos positivos, mismo patrón de colisión "MIDA"/keyword
  genérico sin relación con Panamá):
    - "Utah wants to process uranium on the Wasatch Front..." (sltrib.com)
      → Utah, energía nuclear. Sin relación agropecuaria ni con Panamá.
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org)
      → Paper académico genérico sobre IoT/agricultura de precisión, sin
        mención ni relación específica con Panamá.
    - "Catalogue of the diptera of the Americas South of United States" (archive.org)
      → Catálogo taxonómico de dípteros (entomología), no es noticia agropecuaria
        de Panamá.
    - "Aragón celebra la sentencia del Supremo... espacio por cerdo en las granjas" (heraldo.es)
      → Regulación ganadera de Aragón, España. No es Panamá.
  (La quinta reasignada, "Cultural Rules For Staying With Locals Abroad", ya
  estaba documentada arriba como falso positivo revisado.)

  Corrección aplicada en esta sesión:
    1. Se marcaron individualmente (vía `mark-ingested <url>`) los 4 artículos
       que sí habían sido revisados y documentados arriba (MITI, Box Elder,
       Utah Cox, Kevin O'Leary) — ahora también fuera de la cola de pendientes.
    2. Fix en scripts/ingest.py:
       - `mark_all_ingested()` ahora usa `prioritize(strategy="score")`, el
         mismo criterio que `run_prepare`, para que ambos comandos operen
         sobre el mismo lote.
       - `mark_ingested()` ahora itera `article_entries(processed)` (excluye
         claves internas `_*`) en vez de `processed.items()` crudo, evitando
         el `AttributeError` sobre `_gdelt_windows`.
  Resultado: 0 artículos ingestados incorrectamente al wiki — los 9 falsos
  positivos de esta sesión quedan marcados `ingested: true` en processed.json
  (fuera de la cola) pero SIN página creada en wiki/. Pendientes: 17 → 8.
