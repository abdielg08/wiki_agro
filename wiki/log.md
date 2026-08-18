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

## 2026-08-18 00:00
ROUTINE: 16 artículos pendientes revisados — 16/16 FALSOS POSITIVOS (0 ingestados)
  Ninguno trataba del sector agropecuario panameño. Todos fueron marcados
  ingested=true en processed.json (sin crear páginas de wiki) para despejar
  la cola, y documentados aquí en vez de omitirse (regla 9 de CLAUDE.md):
    - MITI/MIDA Malasia (incentivos industriales) — homónimo de MIDA-Panamá
    - 3x MIDA Utah (Military Installation Development Authority, data centers,
      uranio, orden del gobernador) — mismo homónimo
    - 1x artículo de viajes que menciona el caso MIDA-Utah de pasada
    - Finep/agricultura familiar — Brasil
    - The Persian Qanat — Irán (UNESCO)
    - 2x Aragón (España): sentencia sobre espacio por cerdo, elecciones AEGA
    - Arvensis Agro — España (nutrición vegetal)
    - Reef Saudi — Arabia Saudita (agricultura de secano)
    - Luis Biendicho / Inaga — Aragón, España (medio ambiente)
    - New York Farm Bureau — EE.UU.
    - Ambient IoT precision agriculture — paper IEEE genérico, sin país
    - Catálogo de Diptera de las Américas (1966/67) — archive.org, sin relación

CAUSA RAÍZ IDENTIFICADA Y CORREGIDA:
  `scripts/fetch_news.py::fetch_ddg_search()` (usada por la búsqueda DDG
  "prensa_agro") NO aplicaba los guards `_is_blocked_domain()` /
  `_is_panama_related()` que sí tiene `fetch_rss()`. DDGS no respeta de forma
  confiable el operador `site:`, así que la búsqueda "site:prensa.com
  agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá" devolvía
  resultados de dominios completamente ajenos (heraldo.es, sltrib.com,
  agenciabrasil.ebc.com.br, spa.gov.sa, ieeexplore.ieee.org, archive.org...)
  etiquetados igualmente como fuente "prensa.com", y el filtro `is_agro_relevant`
  solo exige UNA palabra clave genérica (ej. "MIDA", "agricultura", "cosecha")
  sin exigir ningún término panameño. Esto explica el 100% de falsos positivos
  de hoy y, revisando el historial, también los de las ingestas de 2026-06-27,
  2026-07-14 y 2026-07-20 (mismos patrones).
  FIX aplicado en este commit: `fetch_ddg_search()` ahora exige que la URL
  pertenezca al dominio configurado en `site`, rechaza `_is_blocked_domain()`,
  y exige `_is_panama_related()` en título+URL+cuerpo — igual que `fetch_rss()`.
  También se corrigió un bug de `mark-ingested` (crasheaba con
  `AttributeError` al iterar `processed.json` porque no excluía la clave
  interna `_gdelt_windows`, que es una lista, no un dict).

DIAGNÓSTICO AVANZADO — 19 días consecutivos sin artículos nuevos reales:
  Último commit con artículos genuinamente nuevos: 2026-07-30 (3 artículos).
  Desde entonces, GitHub Actions corre a diario con éxito ("completed success")
  pero descarga 0 artículos — muy por encima del umbral de 3 días de CLAUDE.md.
  Log de la corrida de hoy (run 32130922392, job 95691665945) muestra que
  **las 4 fuentes de fetch fallan simultáneamente**:
    1. RSS IICA (`iica.int/es/rss/noticias`) → 0 entradas en el feed
    2. RSS LaPrensaGeneral (`prensa.com/feed/`) → 0 entradas en el feed
       (ambos feeds responden HTTP 200 pero sin items — posible URL obsoleta
       o cambio de estructura; no verificable desde este sandbox, egress
       bloqueado hacia esos dominios)
    3. Búsquedas DDG por dominio oficial (oirsa.org, mida.gob.pa, idiap.gob.pa,
       bda.gob.pa, fao.org, bancomundial.org, iica.int) → TODAS "No results
       found". Solo la búsqueda genérica "prensa_agro" (sin site: efectivo)
       devuelve resultados, y hasta hoy eran básicamente puros falsos positivos.
    4. GDELT histórico → **bloqueado 100% de las ventanas intentadas hoy**
       (`GET blocked (403/429): api.gdeltproject.org/api/v2/doc/doc` en
       2015-01-01→2015-04-01, 2015-07-02→2015-09-30, 2015-10-01→2015-12-30,
       2015-12-31→2016-03-30, 2016-03-31→2016-06-29, 2016-06-30→2016-09-28,
       2016-09-29→2016-12-28, 2016-12-29→2017-03-29, y también la ventana
       incremental reciente 2026-06-18→2026-08-17). El backfill histórico
       real de Panamá cubre solo 2017-03-30 → 2026-06-17 (70 ventanas ya
       marcadas `ya descargado`); el rango 2015-02-19 → 2017-03-29 sigue
       sin cubrirse y el script gasta ~7 min/día reintentando esas mismas
       ventanas sin éxito antes de agotar el timeout del job.
    World Bank API tampoco aportó artículos nuevos hoy.
  RECOMENDACIÓN para próxima sesión: (a) verificar manualmente si
  `iica.int/es/rss/noticias` y `prensa.com/feed/` siguen siendo las URLs
  correctas de esos feeds; (b) evaluar backoff/rotación de IP o reducir
  frecuencia de golpes a GDELT para las ventanas 2015-2017 (bloqueo
  persistente sugiere rate-limit por IP compartida de GitHub Actions);
  (c) las búsquedas DDG restringidas a dominios .gob.pa no devuelven nada —
  investigar si `ddgs.news()` indexa esos dominios en absoluto, o si conviene
  cambiar de método (scraping directo, sitemap) para MIDA/IDIAP/BDA.
