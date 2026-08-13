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

## 2026-08-13 17:45
ROUTINE: 16 pendientes al inicio → 0 al final. 0 artículos reales ingestados.
  **TODOS los 16 pendientes eran falsos positivos** — 0% tasa de aceptación de la fuente "prensa.com".

  FALSOS POSITIVOS DETECTADOS Y RECHAZADOS (no se creó contenido wiki para ninguno):
    1. paultan.org — "MITI working on simplified NCM..." (incentivos de inversión de Malasia, MIDA=Malaysian Investment Development Authority)
    2. sltrib.com — "Kevin O'Leary data center timeline" (MIDA=Utah Military Installation Development Authority)
    3. sltrib.com — "Box Elder data center opponents" (Utah, MIDA)
    4. sltrib.com — "Utah Gov. Cox... data centers" (Utah, MIDA)
    5. msn.com — "Cultural Rules For Staying With Locals Abroad" (menciona MIDA de Utah de pasada)
    6. heraldo.es — "Aragón celebra sentencia... espacio por cerdo" (España, ganadería porcina de Aragón)
    7. sltrib.com — "Utah wants to process uranium..." (Utah, MIDA)
    8. heraldo.es — "Arvensis Agro amplía instalaciones" (empresa española, Aragón)
    9. spa.gov.sa — "Reef Saudi" (programa agrícola de Arabia Saudita)
    10. agenciabrasil.ebc.com.br — "Finep... agricultura familiar" (Brasil)
    11. whc.unesco.org — "The Persian Qanat" (sistema de riego histórico de Irán)
    12. heraldo.es — "AEGA pide elecciones al campo en Aragón" (España)
    13. nyfb.org — "New York Farm Bureau" (EE.UU.)
    14. heraldo.es — "Luis Biendicho asume consejería Medio Ambiente" (Aragón, España)
    15. ieeexplore.ieee.org — "Ambient IoT: Precision Agriculture" (paper académico genérico, sin mención de Panamá)
    16. archive.org — "Catalogue of the diptera of the Americas South of United States" (catálogo zoológico de 1966/67, Brasil)

  CAUSA RAÍZ IDENTIFICADA Y CORREGIDA:
    La búsqueda DuckDuckGo "prensa_agro" en config/sources.yaml usaba la query:
      site:prensa.com agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá
    Sin paréntesis, el operador "site:" solo se aplica al primer término ("agropecuario"),
    dejando el resto de los OR ("agricultura", "ganadería", "MIDA", "cosecha", "Panamá")
    sin restricción de dominio — por eso DDG devolvía resultados de cualquier sitio del
    mundo que contuviera alguna de esas palabras sueltas (especialmente "MIDA", que
    colisiona con la Malaysian Investment Development Authority y la Utah Military
    Installation Development Authority).
    Además, `fetch_ddg_search()` en scripts/fetch_news.py no aplicaba los filtros
    `_is_blocked_domain()` / `_is_panama_related()` que sí tiene `fetch_rss()`, así que
    no había una segunda línea de defensa contra el bug del query.

  FIXES APLICADOS (código, no `sources/`):
    1. config/sources.yaml: query reescrita con paréntesis para que "site:" aplique a
       todo el grupo OR: "(agropecuario OR agricultura OR ganadería OR MIDA OR cosecha) Panamá"
    2. scripts/fetch_news.py: fetch_ddg_search() ahora aplica _is_blocked_domain() y
       _is_panama_related() igual que fetch_rss() (defensa en profundidad)
    3. scripts/ingest.py: mark_ingested() iteraba processed.items() crudo y crasheaba
       (AttributeError) al encontrar la key interna "_gdelt_windows" (lista, no dict) —
       ahora usa article_entries() como mark_all_ingested()

  DIAGNÓSTICO ADICIONAL:
    - Ventanas GDELT completadas: 66 (≥45 estimadas) → backfill histórico 2015→hoy AGOTADO
    - Última corrida de GitHub Actions: 2026-08-13 (corre normalmente cada pocos días)
    - Días sin artículos REALES nuevos: ≥14 (desde 2026-07-30) — supera el umbral de 3 días
      del CLAUDE.md, pero la causa no era que Actions no corriera, sino que el 100% de lo
      que traía la fuente "prensa.com" eran falsos positivos que inflaban "Pendientes"
      artificialmente
    - Recomendación: con GDELT agotado y DDG corregido pero de rendimiento incierto, evaluar
      activar RSS oficiales de MIDA/IDIAP/BDA (actualmente sin RSS configurado, ver
      config/sources.yaml ~línea 150) para sostener el ritmo de ~1 artículo/día hábil

  Artículos en sources/: 29 | Ingestados reales: 6 | Pendientes: 0
  Total páginas wiki: 20 (8 topics, 3 entities, 6 summaries, 3 overview)

## 2026-08-13 17:42
LINT: 20 páginas revisadas, 55 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:12, no_index:1
