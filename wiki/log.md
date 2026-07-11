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

## 2026-07-11 00:00
FALSOS POSITIVOS: 5/5 artículos del lote de ingesta RECHAZADOS — 0 ingestados
  Ninguno trata sobre agro panameño. No se creó contenido de wiki para ninguno.
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com) →
      centro de datos en Utah; "MIDA" = Military Installation Development Authority (Utah), NO Ministerio
      de Desarrollo Agropecuario de Panamá.
    - "Box Elder data center opponents hope for a vote..." (sltrib.com) → mismo caso MIDA-Utah.
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) → mismo caso MIDA-Utah.
    - "Utah wants to process uranium on the Wasatch Front..." (sltrib.com) → Military Installation
      Development Authority (Utah), procesamiento de uranio — sin relación agropecuaria ni con Panamá.
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa) → programa agrícola
      de Arabia Saudita, no de Panamá.
  CAUSA RAÍZ IDENTIFICADA: los 5 artículos fueron obtenidos por `fetch_ddg_search()` (búsqueda web
  DuckDuckGo, fuente configurada `prensa_agro` en config/sources.yaml con query que incluye el término
  ambiguo "MIDA"). A diferencia de `fetch_rss()` y el crawl de GDELT, `fetch_ddg_search()` en
  scripts/fetch_news.py NO aplica los filtros `_is_blocked_domain()` ni `_is_panama_related()` — solo
  llama a `is_agro_relevant()`. Además el operador `site:prensa.com` de DDGS news search no se respetó
  (los resultados vinieron de sltrib.com y spa.gov.sa) y la función además fuerza
  `country: "PA"` / `language: "es"` de forma incondicional, ocultando el origen real del artículo.
  ACCIÓN: se agregaron los mismos filtros Panamá-específicos a `fetch_ddg_search()` en
  scripts/fetch_news.py (ver commit) para evitar que este patrón de falso positivo se repita.
  Los 5 artículos se marcaron como `ingested: true` en processed.json (revisados y descartados) para
  no bloquear la cola de pendientes; NO se agregó ningún contenido a wiki/.

## 2026-07-11 00:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-11 00:10
BUG DE PIPELINE ENCONTRADO Y CORREGIDO: `mark-all-ingested --limit N` usaba un orden
(alfabético por nombre de archivo, vía `find_pending()`) DISTINTO al que usa
`ingest --limit N` para seleccionar qué artículos mostrar a Claude Code (por score de
relevancia, vía `prioritize()` en scripts/prioritize.py). Efecto observado en esta sesión:
  - El lote de `ingest --limit 5` mostró 5 artículos (incluyendo "'Reef Saudi'...").
  - Al ejecutar `mark-all-ingested --limit 5` inmediatamente después, se marcó como
    ingestado un artículo DISTINTO y nunca mostrado a Claude — "New York Farm Bureau"
    (https://www.nyfb.org/, source prensa.com) — saltándose por completo la verificación
    de "¿es 100% sobre agro de Panamá?" exigida por CLAUDE.md. A la vez, "'Reef Saudi'..."
    (que sí fue revisado y rechazado) quedó `ingested: false` y reapareció en el siguiente
    lote de `ingest --limit 5`.
  CORRECCIÓN: `nyfb.org` se revirtió a `ingested: false` en sources/processed.json para
  que pase por revisión real (es igualmente un falso positivo — "New York Farm Bureau" es
  un gremio agrícola de EE.UU., sin relación con Panamá — ver rechazo abajo).
  Se corrigió `scripts/ingest.py::mark_all_ingested()` para que use la misma función
  `prioritize()` (estrategia "score" por defecto) que `run_prepare()`, garantizando que
  ambos comandos operen siempre sobre el mismo subconjunto/orden de artículos.
  IMPACTO: este bug pudo haber estado marcando artículos no revisados como ingestados en
  sesiones previas de la routine automática — se recomienda auditoría de
  `sources/processed.json` en una sesión futura para detectar otros casos.

## 2026-07-11 00:12
FALSOS POSITIVOS: 3/3 artículos RECHAZADOS — 0 ingestados (incluye "'Reef Saudi'..." ya
documentado arriba, que reapareció por el bug de orden descrito, más 2 nuevos)
    - "New York Farm Bureau" (https://www.nyfb.org/) → gremio agrícola de Nueva York,
      EE.UU. Sin relación con Panamá. Detectado al revertir el bug de mark-all-ingested.
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa) →
      ya rechazado en la entrada de las 00:00; reapareció por el bug de orden, se confirma
      el mismo rechazo.
    - "The Persian Qanat" (https://whc.unesco.org/en/list/1506) → sitio Patrimonio Mundial
      UNESCO sobre el sistema de irrigación qanat en Irán. Sin relación con Panamá.
  Los 3 se marcaron como `ingested: true` (revisados y descartados); no se agregó
  contenido a wiki/.
