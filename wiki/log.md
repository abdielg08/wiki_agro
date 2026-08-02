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

## 2026-08-02 00:00
INGEST (routine automática): lote de 5 artículos pendientes revisado — **5/5 FALSOS POSITIVOS, 0 ingestados**
  Causa raíz: colisión de la sigla "MIDA" con entidades no relacionadas al agro panameño:
    - MIDA = Malaysian Investment Development Authority (agencia bajo MITI, Malasia)
    - MIDA = Military Installation Development Authority (Utah, EE.UU.)
  Artículos rechazados (ninguno trata sobre agro de Panamá):
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, 2026-07-08) — política industrial/automotriz de Malasia, no agro panameño.
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19) — centro de datos en Utah; MIDA = Military Installation Development Authority.
    - "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27) — mismo caso, oposición local a centro de datos en Utah.
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29) — mismo caso, calidad de aire/agua en Utah.
    - "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07) — artículo de viajes/cultura, sin relación con agro ni con Panamá.
  Acción: no se crearon páginas de wiki. Los 5 artículos se marcaron `ingested: true` (vía `mark-all-ingested`) para despejar la cola de pendientes, sin generar contenido — cumpliendo la regla de 0% falsos positivos.
  Recomendación: si el fetch usa "MIDA" como término de búsqueda sin contexto ("Panamá", "agropecuario", "arroz", etc.), seguirá trayendo estos falsos positivos de Malasia/Utah. Considerar refinar la query de búsqueda/RSS para exigir contexto panameño.

## 2026-08-02 08:10
FIX (herramientas): 3 bugs encontrados y corregidos durante la routine
  1. `scripts/fetch_news.py::fetch_ddg_search()` no aplicaba los filtros
     `_is_panama_related()` / `_is_blocked_domain()` que ya protegen las rutas
     RSS y GDELT (comentario existente: "no acronyms (MIDA matches Malaysia too)").
     Causa raíz de que los 11 artículos pendientes al cierre de esta sesión sean
     100% de dominios no panameños (sltrib.com, heraldo.es, ieeexplore.org,
     archive.org, whc.unesco.org, agenciabrasil.ebc.com.br, spa.gov.sa, nyfb.org).
     Fix: se agregó el mismo filtro de relevancia panameña al buscador DDG.
  2. `scripts/ingest.py::mark_ingested()` iteraba `processed.items()` sin excluir
     la clave interna `_gdelt_windows` (una lista) → `AttributeError` en toda
     invocación. El comando CLI `mark-ingested <url>` estaba roto. Fix: usar
     `article_entries(processed)`.
  3. `scripts/ingest.py::mark_all_ingested()` usaba `find_pending()` (orden por
     nombre de archivo) mientras que `run_prepare()`/`ingest --limit N` usa
     `prioritize(..., strategy="score")` — dos selecciones distintas. Al correr
     `mark-all-ingested --limit 5` esta sesión se marcaron 5 artículos
     **diferentes** a los 5 realmente mostrados en `pending_ingest.md` (solo 1
     coincidió), sin haber sido revisados ni tener página de wiki. Se revirtieron
     manualmente los 4 mal marcados (`ingested: false` de nuevo, ver
     `sources/processed.json`) y se corrigió `mark_all_ingested()` para usar la
     misma priorización por score que `run_prepare()`.
  Verificación: tras el fix, se ejecutó `mark-ingested` individualmente para los
  4 artículos MITI/Utah realmente revisados — funcionó correctamente.

## 2026-08-02 08:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
