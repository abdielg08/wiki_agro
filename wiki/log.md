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

## 2026-08-23 08:15
INGEST: 0 artículos reales ingestados — 9 falsos positivos detectados y marcados (0 páginas wiki nuevas)
  `python wiki_agro.py ingest --limit 5` mostró 5 artículos en pending_ingest.md; ninguno era
  sobre agro de Panamá. Los 5:
    1. "MITI working on simplified NCM..." (paultan.org) → MITI/MIDA/MARii de **Malasia**
       (ministerio de inversión, comercio e industria), no relacionado con Panamá.
    2. "Box Elder data center opponents..." (sltrib.com) → MIDA = **Military Installation
       Development Authority de Utah, EE.UU.** (proyecto de centro de datos), no Panamá.
    3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) → mismo MIDA de Utah.
    4. "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com) → mismo MIDA de Utah.
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com) → mención incidental de MIDA
       (Utah) en artículo de etiqueta de viajes, sin relación con agro.
  Los 5 fueron marcados `skipped: true` con `skip_reason` en `sources/processed.json` y
  excluidos de `wiki/` (regla CLAUDE.md #9 — 0% falsos positivos es innegociable).

  **Bug de herramienta descubierto**: al correr `mark-all-ingested --limit 5` para despejar
  esos 5 de la cola, el comando marcó como ingestados 5 artículos **distintos** a los revisados
  (solo 1 coincidió). Causa: `ingest` selecciona por score de `prioritize.py` (orden de
  relevancia), mientras `find_pending()` (usado por `mark-ingested`/`mark-all-ingested` en
  `scripts/ingest.py:31-46`) ordena por nombre de archivo (fecha), sin relación con el orden
  mostrado en `pending_ingest.md`. Esto significa que el flujo estándar
  ingest→revisar→mark-all-ingested puede marcar artículos NO revisados como ingestados
  silenciosamente — riesgo de perder artículos reales sin generar página wiki, o de dejar
  falsos positivos sin marcar como tal.
  Los 4 artículos marcados de más por el bug se verificaron post-hoc (texto completo, sin
  mención de Panamá en ninguno) y también resultaron ser falsos positivos:
    - "Utah wants to process uranium..." (sltrib.com) — Utah, EE.UU.
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) — paper genérico 6G/IoT
    - "Catalogue of the diptera of the Americas..." (archive.org, 1966/67) — catálogo entomológico
    - "Aragón celebra la sentencia..." (heraldo.es) — normativa de granjas porcinas en España
  Se etiquetaron igualmente con `skipped`/`skip_reason` y `ingested: true` para mantener
  `sources/processed.json` consistente. **Recomendación**: revisar/arreglar
  `scripts/ingest.py::find_pending()` para que use el mismo orden de prioridad que `ingest`,
  o para que `mark-all-ingested` reciba explícitamente la lista de URLs a marcar en vez de
  re-derivarla.

  **Causa raíz de los falsos positivos**: `scripts/fetch_news.py::fetch_ddg_search()` (fuente
  `prensa.com`, búsqueda vía DuckDuckGo) NO aplica el filtro `_is_panama_related()` que sí usan
  `fetch_rss()` y `fetch_gdelt_batch()` — solo llama `is_agro_relevant()`, que verifica términos
  agro genéricos sin exigir mención de Panamá. Además etiqueta `source` con el sitio buscado
  (`site:` de la query DDG), no con el dominio real del resultado, lo que oculta el origen
  real (paultan.org, sltrib.com, msn.com, ieeexplore.ieee.org, archive.org, heraldo.es —
  ninguno es prensa.com). Este es el mismo patrón de falsos positivos "MIDA" ya visto el
  2026-06-22 (7 falsos positivos por MIDA de Malasia). El bug NO fue corregido en ese momento;
  sigue generando ~100% de falsos positivos en la cola de `prensa.com` vía DDG search.
  Revisando la cola completa de pendientes (`python wiki_agro.py queue`), los 8 artículos
  restantes también parecen ser falsos positivos por el mismo patrón (Aragón/España, Brasil,
  Arabia Saudita, EE.UU., catálogos académicos — ninguno menciona Panamá en el título).
  **Recomendación para el mantenedor humano**: aplicar `_is_panama_related(title, url)` como
  filtro adicional dentro de `fetch_ddg_search()` antes de `yield`, y corregir el campo
  `source` para reflejar el dominio real del artículo, no el `site:` de búsqueda.

  Pendientes tras esta sesión: 17 → 8 (9 marcados como falso positivo, 0 ingestados a wiki/).
  Artículos ingestados reales: 13 (sin cambio — cero contenido nuevo se agregó a wiki/topics,
  wiki/entities o wiki/summaries esta sesión, por diseño: ningún artículo pasó el filtro
  0%-falsos-positivos).

## 2026-08-23 08:11
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-23 08:14
LINT: 20 páginas revisadas, 55 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:12, no_index:1
