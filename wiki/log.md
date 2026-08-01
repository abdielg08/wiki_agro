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

## 2026-08-01 08:02
INGEST: 5 artículos evaluados de pending_ingest.md — 0 ingestados, 5 FALSOS POSITIVOS
  Ninguno de los 5 artículos trata sobre agro panameño; los 5 solo coincidieron
  por la palabra "MIDA", que en estos artículos no se refiere al Ministerio de
  Desarrollo Agropecuario de Panamá:
    - "MITI working on simplified NCM..." (paultan.org) → MIDA = Malaysian
      Investment Development Authority (Malasia), tema industrial/automotriz
    - "Timeline: Kevin O'Leary data center plan..." (sltrib.com) → MIDA =
      Military Installation Development Authority de Utah, EE.UU.
    - "Box Elder data center opponents..." (sltrib.com) → mismo MIDA de Utah
    - "Utah Gov. Cox issues order... data centers" (sltrib.com) → mismo MIDA
      de Utah, calidad del aire/lago Great Salt Lake
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) → artículo de
      viajes, sin relación agropecuaria; menciona MIDA de Utah de pasada
  Ningún artículo generado en wiki/summaries/, wiki/topics/ ni wiki/entities/.
  Los 5 se marcarán como `ingested: true` en processed.json (revisados y
  descartados) para que no permanezcan pendientes indefinidamente.
  Causa raíz probable: el fetch RSS/GDELT está capturando artículos
  internacionales que mencionan "MIDA" sin filtrar por relevancia geográfica
  a Panamá — revisar keywords/filtros de sources/ en la siguiente sesión.

## 2026-08-01 08:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-01 08:15
BUG ENCONTRADO Y CORREGIDO: `mark-all-ingested` marcaba artículos incorrectos
  Al llamar `mark-all-ingested --limit 5` después de revisar los 5 artículos de
  arriba, `stats` mostró 5 marcados — pero `processed.json` reveló que 4 de
  los 5 realmente marcados NO eran los revisados. Causa: `ingest` selecciona
  por relevancia (`strategy=score`, ve TODOS los pendientes), mientras
  `mark-all-ingested` tomaba los primeros N en orden de archivo (`find_pending`
  sin scoring) — dos criterios de orden distintos sobre la misma cola.
  Artículos marcados por error sin revisión explícita (verificados después,
  manualmente, ninguno era agro-Panamá — coincidencia, no garantía):
    - heraldo.es "Aragón celebra sentencia... espacio por cerdo en granjas"
      (España, no Panamá)
    - sltrib.com "Utah wants to process uranium... nuclear energy" (menciona
      MIDA = Military Installation Development Authority de Utah)
    - ieeexplore.ieee.org/document/10945742 "Ambient IoT: Communications
      Enabling Precision Agriculture" (paper académico global, no Panamá)
    - archive.org "Catalogue of the diptera of the Americas South of United
      States" (catálogo taxonómico de Brasil/1966, no noticia de Panamá)
  Fix aplicado en `scripts/ingest.py`:
    - `mark_ingested()`: ahora filtra claves internas (`_gdelt_windows`) con
      `article_entries()` antes de iterar — el comando estaba roto en TODAS
      sus invocaciones (crash `AttributeError: 'list' object has no attribute
      'get'` porque `_gdelt_windows` es la primera clave del dict y es una
      lista, no un diccionario de metadata).
    - `mark_all_ingested()`: ahora usa `prioritize(strategy="score")`, el
      mismo criterio que `run_prepare()`/`ingest`, para marcar exactamente
      los artículos mostrados en `pending_ingest.md`.
  Recomendación: preferir `mark-ingested <url>` por artículo (ahora funcional)
  sobre `mark-all-ingested` hasta confirmar el fix en una corrida real.

## 2026-08-01 08:20
INGEST: 5 artículos más evaluados (2ª tanda, re-mostrados tras el bug) — 0
  ingestados, 5 FALSOS POSITIVOS (4 ya vistos en la tanda anterior + 1 nuevo):
    - paultan.org "MITI working on simplified NCM..." → MIDA = Malaysian
      Investment Development Authority (Malasia)
    - sltrib.com Kevin O'Leary data center timeline → MIDA de Utah
    - sltrib.com Box Elder data center opponents → MIDA de Utah
    - sltrib.com Utah Gov. Cox order (calidad de aire) → MIDA de Utah
    - heraldo.es "AEGA pide elecciones al campo en Aragón..." → agricultura
      de Aragón, España — no Panamá
  Los 5 marcados correctamente vía `mark-ingested <url>` (fix aplicado arriba).

## 2026-08-01 08:25
INGEST: 6 artículos finales evaluados (3ª tanda) — 0 ingestados, 6 FALSOS
  POSITIVOS, ninguno sobre agro de Panamá:
    - nyfb.org "New York Farm Bureau" (EE.UU.)
    - heraldo.es "Arvensis Agro amplía instalaciones" (Aragón, España)
    - spa.gov.sa "Reef Saudi, rain-fed agriculture" (Arabia Saudita)
    - agenciabrasil.ebc.com.br "Finep... agricultura familiar" (Brasil)
    - whc.unesco.org "The Persian Qanat" (Irán, patrimonio UNESCO)
    - heraldo.es "Luis Biendicho asume consejería de Medio Ambiente... caso
      Forestalia" (Aragón, España)
  Los 6 marcados vía `mark-ingested <url>`. Pendientes de ingesta: 0.

## 2026-08-01 08:30
DIAGNÓSTICO — CAUSA RAÍZ de los 16 falsos positivos únicos de esta sesión
  (5 + 4 detectados por el bug de mark-all-ingested + 1 + 6, ver entradas
  anteriores) y de los 7 falsos positivos previos registrados en metrics.md
  el 2026-06-22 (23 en total acumulados):
  Las 23 fuentes "prensa.com" en `processed.json` NO vienen del RSS real de
  La Prensa Panamá — vienen de `fetch_ddg_search()` (búsqueda DuckDuckGo
  configurada como `site:prensa.com agropecuario OR agricultura OR
  ganadería OR MIDA OR cosecha Panamá` en `config/sources.yaml`). El operador
  `site:` de DDG News no se respeta de forma confiable, y el resultado se
  etiquetaba como fuente "prensa.com" sin verificar el dominio real de la URL.
  Además, en la query OR-separada, "Panamá" solo calificaba al último término
  ("cosecha Panamá"), así que cualquier resultado global con solo "MIDA" o
  "agricultura" bastaba para pasar el filtro `is_agro_relevant()`.
  De los 23 artículos con fuente "prensa.com", los 16 que estaban pendientes
  se revisaron todos individualmente en esta sesión (contenido/URL leído
  directamente) y el 100% eran de dominios ajenos (sltrib.com, paultan.org,
  msn.com, heraldo.es, nyfb.org, spa.gov.sa, agenciabrasil.ebc.com.br,
  whc.unesco.org, ieeexplore.ieee.org, archive.org) — ninguno de prensa.com
  ni de Panamá. Los 7 restantes ya habían sido descartados el 2026-06-22.
  FIX aplicado en `scripts/fetch_news.py` (`fetch_ddg_search`): ahora se
  verifica que el dominio real de la URL devuelta coincida con `site` antes
  de aceptar el resultado, descartando el resto. Esto debería eliminar la
  mayoría de los falsos positivos futuros de la fuente `prensa_agro`.
  Pendiente: la query OR sigue sin exigir "Panamá" en todos los términos;
  revisar en una sesión futura si el fix de dominio no es suficiente.
  Estado del fetch automático (GitHub Actions):
    - Última corrida con contenido nuevo: 2026-07-30 (3 artículos)
    - Última corrida: 2026-07-31 (0 artículos nuevos) — 1 día sin novedades,
      dentro del rango aceptable (umbral de alarma: 3 días)
    - Ventanas GDELT completadas: 60 (≥45 según el umbral simple de
      CLAUDE.md), pero desbalanceadas por año: 2015 y 2016 tienen 0
      ventanas completadas (el backfill nunca llegó al inicio real de la
      cobertura objetivo, 2015-02-19), mientras 2017-2026 están completos
      o sobre-cubiertos (2026 tiene 24 ventanas). El umbral simple ">=45 =
      rango agotado" es engañoso aquí — ver tabla corregida en metrics.md.
      Acción sugerida para la próxima sesión: priorizar backfill histórico
      de 2015-2016.
  Nota adicional: `Artículos ingestados` pasó de 13 a 29 en esta sesión, pero
  0 artículos reales se añadieron al wiki (todos los pendientes eran falsos
  positivos). El conteo de "13 ya ingestados" al inicio de la sesión incluía
  6 semillas reales + 7 falsos positivos ya descartados en la auditoría del
  2026-06-22 — ver wiki/metrics.md.
