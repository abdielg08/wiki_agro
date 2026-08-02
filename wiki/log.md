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

## 2026-08-02 16:02
INGEST: 5 artículos revisados — 5 falsos positivos (0 ingestados al wiki)
  Causa raíz: colisión de la sigla "MIDA" — el scraper de GDELT/RSS trae artículos que
  mencionan "MIDA" pero en otro contexto: Malaysian Investment Development Authority
  (MITI/MIDA/MARii, Malasia) y la Military Installation Development Authority
  de Utah, EE.UU. (caso de datacenters de Kevin O'Leary). Ninguno de los 5 tiene
  menciones a Panamá (0 ocurrencias de "panama"/"panamá" en el texto completo).
  Artículos descartados (NO agregados al wiki):
    - paultan.org/.../miti-working-on-simplified-ncm... (MIDA Malasia, incentivos industriales)
    - sltrib.com/.../kevin-oleary-data-center-timeline (MIDA Utah, datacenter Stratos)
    - sltrib.com/.../box-elder-data-center-opponents (MIDA Utah, oposición vecinal)
    - sltrib.com/.../utah-governor-issues-order-protect (MIDA Utah, calidad del aire)
    - msn.com/.../cultural-rules-for-staying-with-locals-abroad (menciona MIDA Utah de pasada)
  Acción: marcados como `ingested: true` en processed.json vía `mark-all-ingested`
  para sacarlos de la cola de pendientes, sin crear páginas de wiki.
  Recomendación: el filtro de ingesta debería excluir artículos cuyo `country` no
  sea Panamá o cuyo dominio de origen sea de otro país (paultan.org=MY, sltrib.com=UT/US),
  ya que el 100% de los 12 falsos positivos acumulados hasta ahora comparten la sigla MIDA.

## 2026-08-02 16:07
INGEST: sesión completa — 16/16 pendientes revisados, 16 falsos positivos, 0 ingestados al wiki
  Se amplió la revisión a los 11 pendientes restantes (batch `ingest --limit 11`) y también
  se auditaron 4 artículos que el bug de `mark-all-ingested` (ver abajo) había marcado
  `ingested` sin revisión previa. Los 16 artículos, sin excepción, tienen 0 menciones de
  "panama"/"panamá" en el texto completo pese a `country: PA` en sus metadatos:
    - 4 sobre "MIDA" = Military Installation Development Authority (Utah, EE.UU.):
      Kevin O'Leary data center timeline, Box Elder opponents, Utah Gov. Cox order, Utah uranium/nuclear
    - 1 sobre "MIDA" = Malaysian Investment Development Authority (MITI/MARii, Malasia)
    - 4 de heraldo.es sobre Aragón, España (Inaga, AEGA, Arvensis Agro, sentencia cerdos)
    - 1 IEEE paper genérico de IoT/agricultura de precisión (sin referencia geográfica)
    - 1 catálogo de dípteros de las Américas de 1966/1967 (archive.org)
    - 1 New York Farm Bureau (EE.UU.)
    - 1 "Reef Saudi" — programa de agricultura de secano en Arabia Saudita
    - 1 Finep (Brasil) — financiamiento a agricultura familiar
    - 1 UNESCO — sistema de qanats en Irán
  Resultado: `Pendientes de ingesta` = 0. `Artículos ingestados` (processed.json) = 29/29,
  pero **0 páginas nuevas de wiki** — los 16 quedaron marcados `ingested: true` únicamente
  para vaciar la cola, sin contenido agregado a topics/entities/summaries.

  BUGS DE HERRAMIENTA encontrados y corregidos (scripts/ingest.py):
  1. `mark_all_ingested()` ordenaba los pendientes por nombre de archivo (glob sort),
     pero `run_prepare()` (la que genera pending_ingest.md) los ordena por score de
     prioridad. Al correr `mark-all-ingested --limit 5` después de revisar los 5
     artículos mostrados, marcó como ingestados 4 artículos DISTINTOS nunca revisados
     (por suerte, también falsos positivos — pero pudo haber ocultado un artículo real
     de Panamá sin revisión). Fix: `mark_all_ingested()` ahora usa `prioritize()` con
     la misma estrategia "score", igualando el orden de `pending_ingest.md`.
  2. `mark_ingested(url)` fallaba con `AttributeError` al iterar `processed.json`
     porque no saltaba la clave interna `_gdelt_windows` (una lista, no un dict),
     dejando el comando `mark-ingested <url>` completamente roto. Fix: se agregó un
     filtro `if url.startswith("_") or not isinstance(meta, dict): continue`.
  Recomendación pendiente (no aplicada, requiere validación en vivo): filtrar en el
  fetch/scoring por `country != PA` o dominio no panameño antes de meter artículos
  a la cola de pendientes — evitaría que "MIDA" como término de alta prioridad siga
  trayendo falsos positivos de Utah/Malasia al tope del ranking de score.

## 2026-08-02 16:07
DIAGNÓSTICO: fetch automático corrió hoy, pero backfill histórico 2015–2017 sigue en 0
  - Último commit tocando `sources/` es de hoy (2026-08-02) → GitHub Actions SÍ corrió.
  - `_gdelt_windows` tiene 61 entradas pero solo 38 ventanas trimestrales distintas
    (rango real: 2017-03-30 → 2026-06-18, secuencia limpia sin huecos).
  - **2015-01-01 → 2017-03-29 (9 ventanas trimestrales, el inicio mismo del objetivo
    2015-02-19) nunca aparece en `_gdelt_windows`** pese a que `fetch_gdelt_historical()`
    siempre reinicia `current = start = 2015-01-01` en cada corrida. Esto implica que
    esas 9 ventanas más antiguas fallan consistentemente (`batch is None`, error de red
    o rechazo de GDELT) en cada una de las ~126 corridas desde el reset del 2026-06-22,
    y por diseño el código las reintenta sin marcarlas — nunca se "resuelven".
  - Las 23 entradas restantes de las 61 son variantes de una sola ventana con
    `start=20260618` y `end` distinto cada día (20260623 … 20260801): la ventana más
    reciente usa `end = min(config_end, hoy-1d)`, que crece un día por corrida. Como la
    `window_key` incluye el `end`, cada corrida genera una clave nueva y re-consulta
    casi el mismo rango en vez de esperar a que pasen los 90 días completos — desperdicia
    cupo de requests de GDELT sin avanzar cobertura real.
  - Ventanas completadas (61) > 45 estimadas → por regla de CLAUDE.md esto normalmente
    indicaría "rango de fechas agotado, necesita expansión", pero en este caso el
    verdadero problema es que el extremo más antiguo (2015-2017) nunca se completa,
    no que el rango esté agotado. No se aplicó ningún cambio a `scripts/fetch_news.py`
    en esta sesión — requiere validación contra la API real de GDELT antes de tocar la
    lógica de ventanas (fuera del alcance de esta sesión de ingesta).

## 2026-08-02 16:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
