---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-23
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

## 2026-07-23 16:00
FALSOS POSITIVOS: 11/11 artículos pendientes rechazados — 0 ingestados al wiki
  Ninguno de los 11 artículos en cola trataba sobre agro panameño. NO se creó
  contenido de wiki para ninguno (regla de 0% falsos positivos). Se marcaron
  como revisados (`ingested: true`, sin páginas de wiki asociadas) para que no
  bloqueen la cola de ingesta:
    - paultan.org — MITI/MIDA Malasia (incentivos industriales, no agro-PA)
    - sltrib.com — Kevin O'Leary / centro de datos Utah (MIDA = Utah Military
      Installation Development Authority)
    - sltrib.com — Box Elder, oposición a centro de datos (mismo MIDA de Utah)
    - sltrib.com — Gov. Cox, protección Great Salt Lake (mismo MIDA de Utah)
    - msn.com — "Cultural Rules For Staying With Locals Abroad" (sin relación)
    - sltrib.com — Utah, uranio para energía nuclear (mismo MIDA de Utah)
    - whc.unesco.org — "The Persian Qanat" (irrigación antigua de Irán)
    - nyfb.org — New York Farm Bureau (agricultura de EE.UU., no Panamá)
    - spa.gov.sa — Programa "Reef Saudi" (agricultura de secano en Arabia Saudita)
    - ieeexplore.ieee.org — paper IEEE sobre IoT/agricultura de precisión (6G,
      genérico, sin mención de Panamá)
    - archive.org — catálogo de dípteros de zoología, Brasil, 1966/1967

  CAUSA RAÍZ identificada y corregida en scripts/fetch_news.py:
    fetch_ddg_search() (búsqueda web DuckDuckGo, usada por `fetch --mode all`
    en el workflow diario) sólo filtraba con is_agro_relevant() — que hace
    match de keywords genéricos como "MIDA" sin exigir contexto de Panamá.
    A diferencia de fetch_rss() y fetch_gdelt, NO aplicaba _is_blocked_domain()
    ni _is_panama_related(). El operador `site:` de DDG tampoco se respeta de
    forma confiable, así que la búsqueda "site:prensa.com ... MIDA ..."
    devolvió resultados de paultan.org, sltrib.com, msn.com, etc., guardados
    con source="prensa.com" (metadata incorrecta) y country="PA" (hardcoded,
    también incorrecto). FIX: se agregaron los mismos filtros _is_blocked_domain()
    y _is_panama_related() usados en fetch_rss() a fetch_ddg_search().

  BUG SECUNDARIO encontrado y corregido en scripts/ingest.py:
    1. mark_ingested() (comando singular `mark-ingested <url>`) iteraba
       processed.items() directamente en vez de article_entries(processed),
       y crasheaba con AttributeError al toparse con la clave interna
       `_gdelt_windows` (una lista, no un dict). Este comando estaba roto
       para cualquier processed.json con ventanas GDELT registradas.
    2. mark_all_ingested() (comando `mark-all-ingested --limit N`) usaba
       find_pending() en orden alfabético de archivo, mientras que `ingest
       --limit N` usa prioritize(strategy="score"). Esto hacía que
       `mark-all-ingested --limit 5` marcara un conjunto de artículos
       DISTINTO al que realmente se mostró en pending_ingest.md y fue
       revisado por Claude — en esta sesión marcó por error 3 artículos
       nunca revisados (incluido uno de zoología de 1966 sin relación a
       Panamá) como ingestados, mientras dejaba 3 de los 5 sí revisados
       todavía pendientes. Se revirtió el estado incorrecto en
       sources/processed.json antes del commit. FIX: mark_all_ingested()
       ahora usa prioritize(strategy="score") para igualar el orden de
       `ingest`, y mark_ingested() usa article_entries() para saltar
       claves internas.

  DIAGNÓSTICO — Paso 4 avanzado (Pendientes = 0 tras el rechazo):
    - GitHub Actions SÍ corrió hoy (commit 51e7fed, 2026-07-23 12:25 UTC),
      pero 0 artículos nuevos (igual que 2026-07-21; sin corrida el 07-22).
      → 3 días consecutivos sin artículos nuevos reales en sources/articles/
      (última vez con contenido nuevo: 2026-07-20, 2 artículos). Condición de
      falla de CLAUDE.md activada — documentada aquí y en metrics.md.
    - Ventanas GDELT completadas: 53 (`_gdelt_windows` en processed.json).
      Supera el umbral de 45 → el rango histórico configurado está agotado
      y necesita expansión (nuevo --years para fetch-historical, o ajustar
      el rango por defecto para cubrir 2026+ de forma continua).
    - RSS activos (IICA, La Prensa) no aportaron artículos nuevos en los
      últimos 3 días — consistente con baja frecuencia de publicación de
      esas fuentes, no necesariamente una falla de fetch.
  Artículos ingestados con contenido real esta sesión: 0 (los 11 pendientes
  eran 100% falsos positivos). Total de páginas de wiki sin cambios: 20.

## 2026-07-23 16:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
