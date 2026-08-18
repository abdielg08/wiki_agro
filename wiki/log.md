---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-18
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
ROUTINE: 16 artículos pendientes revisados — LOS 16 SON FALSOS POSITIVOS (0 ingestados)
  Verificación: ninguno de los 16 menciona "Panamá"/"Panamá" en su texto completo
  (búsqueda de texto sobre los .json fuente confirmó 0 coincidencias en cada uno)

  Artículos rechazados (todos etiquetados source="prensa.com" incorrectamente):
    - https://www.spa.gov.sa/en/N2096157 — agricultura de secano en Arabia Saudita
    - https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/ — MIDA = Utah Military Installation Development Authority
    - https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/ — ídem (Utah MIDA)
    - https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/ — ídem (Utah MIDA)
    - https://www.nyfb.org/ — New York Farm Bureau
    - https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/ — ídem (Utah MIDA)
    - https://whc.unesco.org/en/list/1506 — Qanats persas (patrimonio UNESCO)
    - https://paultan.org/2026/07/07/miti-working-on-simplified-ncm-... — MITI/MIDA = Malaysian Investment Development Authority
    - https://ieeexplore.ieee.org/document/10945742 — IoT agrícola genérico, sin país
    - https://www.msn.com/en-us/news/other/cultural-rules-for-staying-with-locals-abroad/... — no agro
    - https://archive.org/details/Cataloguedipter2SaoP — catálogo entomológico histórico
    - https://www.heraldo.es/noticias/aragon/.../luis-biendicho-vox-... — política ambiental de Aragón, España
    - https://www.heraldo.es/noticias/economia/.../aragon-celebra-sentencia-supremo-... — granjas porcinas de Aragón, España
    - https://www.heraldo.es/noticias/economia/.../aega-pide-elecciones-campo-aragon-... — gremio agrícola de Aragón, España
    - https://agenciabrasil.ebc.com.br/economia/noticia/2026-07/finep-vai-pagar-... — agricultura familiar en Brasil
    - https://www.heraldo.es/noticias/economia/.../arvensis-agro-amplia-... — empresa agro de Aragón, España

  CAUSA RAÍZ IDENTIFICADA: config/sources.yaml define la búsqueda web_searches
  "prensa_agro" (site: "prensa.com", query con términos agro genéricos + "MIDA").
  scripts/fetch_news.py::fetch_ddg_search() construye `site:prensa.com <query>`
  pero el operador `site:` de la librería ddgs/DuckDuckGo NO se respeta de forma
  confiable en resultados de noticias — la búsqueda devolvió artículos de
  agricultura de dominios totalmente ajenos (heraldo.es, sltrib.com, paultan.org,
  ieee, unesco, etc.), y la función los etiquetaba source="prensa.com",
  country="PA" sin verificar el dominio real ni exigir mención de Panamá.
  Además "MIDA" como término de búsqueda colisiona con la Malaysian Investment
  Development Authority y la Utah Military Installation Development Authority.

  FIX APLICADO (este commit):
    - scripts/fetch_news.py::fetch_ddg_search() — ahora verifica que el dominio
      del resultado coincida realmente con `site` antes de aceptarlo.
    - scripts/fetch_historical.py::fetch_gdelt_window() — ahora aplica
      _is_panama_related()/_is_blocked_domain() (mismo filtro ya usado por
      fetch_gdelt_batch en fetch_news.py), que antes faltaba en esta ruta
      histórica y permitía la misma colisión de "MIDA".

  Los 16 artículos se marcaron `ingested: true` (sin crear páginas de wiki)
  vía `mark-all-ingested` para no bloquear el pipeline; Pendientes de ingesta: 0.

DIAGNÓSTICO AVANZADO (Pendientes = 0):
  - Último commit a sources/: 2026-08-17 (ayer) — 0 artículos nuevos.
  - 12 días consecutivos (2026-08-06 → 2026-08-17, con la excepción de estos
    16 falsos positivos) sin artículos genuinamente nuevos sobre agro de Panamá.
  - De los 29 artículos descargados en total, solo 6 son reales (la semilla
    manual del 2026-05-24). Los 23 restantes son falsos positivos — 7 ya
    corregidos el 2026-06-22 (ver wiki/metrics.md) y 16 corregidos hoy.
    Tasa de falsos positivos del fetch automatizado hasta ahora: ~79% (23/29).
  - Ventanas GDELT completadas: 70 (por encima del estimado de ~45) → el rango
    de fechas vía GDELT (`fetch_gdelt_historical`, con filtro Panamá correcto)
    está efectivamente agotado; no se esperan más artículos nuevos de esa vía
    sin expandir términos de búsqueda o el rango de fechas.
  - Con el fix de hoy a fetch_ddg_search, la próxima corrida de GitHub Actions
    debería dejar de generar falsos positivos de "prensa_agro"; validar mañana
    si aparecen artículos nuevos legítimos o si el conteo de nuevos sigue en 0
    (en cuyo caso el problema sería que RSS/DDG simplemente no encuentran
    contenido agro de Panamá reciente, no un bug de filtrado).

## 2026-08-18 08:15
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-18 08:15
INGEST: 11 artículos marcados como ingestados por sesión Claude Code
