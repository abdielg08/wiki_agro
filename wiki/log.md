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

## 2026-07-15 16:02
INGEST: 5 artículos evaluados — 0 ingestados, 5 falsos positivos (colisión de sigla "MIDA")
  Falsos positivos detectados:
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, 2026-07-08)
      → Sobre MITI/MIDA/MARii de MALASIA (Malaysian Investment Development Authority), no Panamá
    - "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27)
      → Sobre Military Installation Development Authority (MIDA) de UTAH, EE.UU., data centers
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
      → Sobre MIDA (Utah) y calidad del aire/agua, sin relación con Panamá
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19)
      → Sobre MIDA (Utah) y proyecto de centro de datos de Kevin O'Leary
    - "Utah wants to process uranium on the Wasatch Front..." (sltrib.com, 2025-06-13)
      → Sobre MIDA (Utah) y procesamiento de uranio para energía nuclear
  Causa raíz: el fetch/búsqueda hace matching por la palabra "MIDA", que colisiona con
    Malaysian Investment Development Authority y Military Installation Development
    Authority (Utah), ninguna relacionada con el Ministerio de Desarrollo Agropecuario
    de Panamá. No se creó contenido de wiki para estos 5 artículos.
  Acción: marcados como procesados vía `mark-all-ingested --limit 5` para vaciar la cola
    de pendientes sin contaminar el wiki. Total falsos positivos acumulados: 12 (7 previos + 5).
  Recomendación: si persiste este patrón, ajustar el filtro de fetch para exigir contexto
    panameño explícito (.pa, "Panamá", "Ministerio de Desarrollo Agropecuario") junto a "MIDA".

## 2026-07-15 16:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-15 16:10
BUGFIX: detectado y corregido bug en `mark_all_ingested` (scripts/ingest.py)
  Síntoma: `ingest --limit N` selecciona artículos por score (prioritize.py,
    estrategia "score" por defecto), pero `mark_all_ingested` marcaba los
    primeros N pendientes en orden de archivo (find_pending sin scoring) —
    dos selecciones distintas del mismo lote nominal.
  Impacto real detectado en esta sesión: el artículo revisado y documentado
    como falso positivo (paultan.org, MITI/MIDA Malasia) NO quedó marcado,
    mientras que https://ieeexplore.ieee.org/document/10945742
    ("Ambient IoT: Communications Enabling Precision Agriculture", sin
    ninguna mención de Panamá) fue marcado como ingestado SIN haber sido
    mostrado a Claude Code para revisión — riesgo directo a la meta de
    0% falsos positivos, ya que un artículo podría descartarse sin
    documentación ni revisión humana/LLM.
  Corrección aplicada:
    1. scripts/ingest.py: `mark_all_ingested` ahora lee las URLs exactas
       del bloque `mark-ingested` al final de `pending_ingest.md` (el lote
       real mostrado a Claude), en vez de recalcular con find_pending().
       Fallback a find_pending() solo si pending_ingest.md no existe.
    2. sources/processed.json: revertido ingested=False en
       ieeexplore.org/document/10945742 (nunca revisado) y corregido
       ingested=True en la URL de paultan.org (sí revisado, documentado
       arriba como falso positivo).
  Verificado: `python wiki_agro.py stats` vuelve a mostrar 4 pendientes
    consistentes con el lote real no revisado.

## 2026-07-15 16:12
INGEST: 4 artículos evaluados — 0 ingestados, 4 falsos positivos (agro genérico/internacional, 0 menciones de Panamá)
  Falsos positivos detectados:
    - "The Persian Qanat" (whc.unesco.org, 2026-07-07) → sitio UNESCO sobre
      sistema de riego qanat en Irán, sin relación con Panamá
    - "New York Farm Bureau" (nyfb.org, 2026-06-17) → organización gremial
      agrícola del estado de Nueva York, EE.UU.
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture"
      (spa.gov.sa, 2026-06-24) → programa agrícola de secano de Arabia Saudita
    - "Ambient IoT: Communications Enabling Precision Agriculture"
      (ieeexplore.ieee.org, 2025-03-31) → paper académico genérico sobre 6G/IoT
      en agricultura de precisión, sin mención de Panamá
  Causa raíz: el fetch/búsqueda de prensa.com está trayendo artículos por
    coincidencia genérica del término "agriculture"/"agricultural", sin
    filtro de país. Ninguno de los 4 menciona Panamá ni una sola vez
    (verificado por conteo de ocurrencias en el texto completo).
  No se creó contenido de wiki. Marcados como procesados vía
    `mark-ingested` individual (URLs exactas de pending_ingest.md) para
    vaciar la cola sin contaminar el wiki. Total falsos positivos
    acumulados: 16 (12 previos + 4).
  Recomendación: revisar la config de fuentes (config/sources.yaml) para la
    fuente "prensa.com" — parece estar indexando contenido internacional
    genérico en vez de La Prensa de Panamá (prensa.com es dominio real de
    La Prensa panameña, pero el contenido fetched no corresponde).

## 2026-07-15 16:20
BUGFIX: causa raíz de los falsos positivos encontrada y corregida en
  scripts/fetch_news.py (`fetch_ddg_search`, fuente de búsqueda "prensa.com"
  en config/sources.yaml, líneas ~159-161).
  Causa raíz: la búsqueda vía DuckDuckGo (`ddgs.news()`) arma la query como
    `site:{site} {query}` pero la API de noticias de ddgs NO respeta de
    forma confiable el operador `site:` — devuelve resultados de dominios
    completamente ajenos (sltrib.com, paultan.org, whc.unesco.org, nyfb.org,
    spa.gov.sa, ieeexplore.ieee.org). Además, a diferencia del path RSS
    (que sí aplica `_is_panama_related()` y `_is_blocked_domain()`), el path
    de búsqueda DDG solo filtraba por `is_agro_relevant()` (términos de
    agro genéricos), sin exigir mención de Panamá ni validar el dominio.
    Esto explica los 9 falsos positivos de esta sesión y probablemente la
    mayoría de los 12 falsos positivos previos acumulados.
  Corrección aplicada en `fetch_ddg_search()`:
    1. Rechaza resultados cuyo dominio no contenga el `site` solicitado.
    2. Aplica `_is_blocked_domain()` (TLDs no-Panamá conocidos).
    3. Aplica `_is_panama_related()` (exige término panameño en título/URL),
       igual que el path RSS.
  Segundo bug encontrado y corregido: `mark_ingested()` (scripts/ingest.py)
    iteraba `processed.items()` sin filtrar las claves internas `_meta`
    (p.ej. `_gdelt_windows`, que es una `list`, no `dict`), causando
    `AttributeError: 'list' object has no attribute 'get'` en TODA
    invocación de `python wiki_agro.py mark-ingested <url>` — el comando
    documentado en CLAUDE.md estaba roto. Corregido para usar
    `article_entries(processed)` como ya hacían `find_pending` y
    `mark_all_ingested`. Verificado: las 4 URLs de la sección anterior se
    marcaron correctamente después del fix.
  Estado post-fix: `python wiki_agro.py stats` → 0 pendientes.

## 2026-07-15 16:35
DIAGNÓSTICO: pendientes = 0 tras ingesta de esta sesión. Diagnóstico avanzado (Paso 4):
  1. ¿Corrió GitHub Actions hoy? Sí — commit `5f4d667` "chore(sources): 1
     artículos nuevos descargados [skip ci]" fechado 2026-07-15 12:17 UTC.
     El fetch diario (RSS + búsqueda DDG, modo "daily") está funcionando.
  2. Ventanas GDELT completadas: 49 en `sources/processed.json["_gdelt_windows"]`,
     cubriendo de forma continua 2017-03-30 → 2026-07-14 (más varias ventanas
     diarias de "catch-up" de julio 2026). **Faltan las ~9 ventanas de
     2015-01-01 a 2017-03-29** — nunca se completaron (ni en esta sesión ni
     en sesiones previas), por lo que la cobertura real NO llega hasta la
     meta de 2015-02-19 declarada en CLAUDE.md.
  3. Intento de avanzar el backfill en esta sesión (`python wiki_agro.py
     fetch --mode gdelt --limit 20 --no-text`): las 9 ventanas de 2015-2016
     fallaron con `ProxyError: Tunnel connection failed: 403 Forbidden`.
     Verificado con `$HTTPS_PROXY/__agentproxy/status`: el gateway del
     entorno sandbox de ESTA sesión rechaza explícitamente las conexiones a
     `api.gdeltproject.org` ("gateway answered 403 to CONNECT — policy
     denial"). **Esto es una restricción del entorno de esta sesión de
     Claude Code, no necesariamente una falla real de GDELT** — no se marcó
     ninguna ventana como completa (el código solo marca completo en
     respuesta HTTP exitosa), así que no hay pérdida de datos ni falso
     "completado".
  4. Hallazgo adicional importante: el modo `daily` de `fetch_news.run_fetch()`
     (el que corre GitHub Actions automáticamente 3x/día) NO incluye GDELT
     — solo RSS + búsqueda DDG (ver `scripts/fetch_news.py` líneas ~560-581
     vs ~594-602, `mode in ("gdelt", "all")`). El backfill GDELT solo avanza
     si alguien dispara manualmente `python wiki_agro.py fetch --mode gdelt`
     (o `all`) desde un entorno con salida de red completa (p.ej. un
     workflow dedicado de GitHub Actions o una sesión local), no desde este
     tipo de sesión sandboxed ni desde el cron diario actual.
  Recomendación para próxima sesión con acceso de red completo a GDELT:
    `python wiki_agro.py fetch --mode gdelt --limit 200` (repetir hasta que
    las 9 ventanas de 2015-2016 completen o confirmen 0 resultados reales).
    Si siguen fallando con error HTTP real (no proxy) en un entorno sin
    restricciones, entonces sí seria evidencia de que GDELT no indexa esas
    fechas para `sourcecountry:PA` — sería la primera evidencia genuina, ya
    que el intento de hoy fue bloqueado por el proxy del sandbox, no por GDELT.
