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

## 2026-08-10 00:00
ROUTINE: Sesión de rutina — pip install -r requirements.txt (click faltaba en el entorno)
  Stats iniciales: 29 descargados, 13 ingestados, 16 pendientes

FALSOS POSITIVOS (5/5 del lote): ningún artículo del lote ingest --limit 5 es sobre
agro de Panamá. NO se ingestó ninguno. Detalle:
  1. "MITI working on simplified NCM..." (paultan.org) — MIDA = Malaysian Investment
     Development Authority (Malasia), no Panamá. Tema: incentivos industriales Malasia.
  2. "Timeline: Kevin O'Leary data center..." (sltrib.com) — MIDA = Military Installation
     Development Authority (Utah, EE.UU.). Tema: centro de datos en Utah.
  3. "Box Elder data center opponents..." (sltrib.com) — mismo MIDA de Utah, oposición
     vecinal a centro de datos.
  4. "Utah Gov. Cox issues order..." (sltrib.com) — mismo MIDA de Utah, calidad del aire.
  5. "Cultural Rules For Staying With Locals Abroad" (msn.com) — mención de demanda
     contra MIDA (Utah) en un artículo de viajes, sin relación con agro.

CAUSA RAÍZ IDENTIFICADA (afecta a la fuente "prensa.com" en general — revisada
también una muestra del resto de la cola de 16 pendientes: Aragón/heraldo.es,
Utah uranium, Brasil Finep, Arabia Saudita, catálogo de dípteros — TODOS son
falsos positivos del mismo origen, ninguno es de Panamá):
  - `config/sources.yaml` → `web_searches: prensa_agro` usa `site: "prensa.com"` +
    query con términos OR, incluyendo "MIDA" como término suelto.
  - `scripts/fetch_news.py::fetch_ddg_search()` construye `site:prensa.com ...` pero
    DDGS().news() no respeta de forma confiable el operador `site:` — llegan
    resultados de dominios arbitrarios (heraldo.es, sltrib.com, paultan.org, msn.com).
  - Esos resultados se guardan con `"source": site or name` → SIEMPRE quedan
    etiquetados como "prensa.com" sin importar el dominio real de origen,
    ocultando el problema en `stats`.
  - `is_agro_relevant()` hace match de substring simple sobre `search_terms`
    (incluye "MIDA" sin contexto de Panamá) → cualquier "MIDA" en inglés
    (Malasia, Utah) pasa el filtro.
  - Recomendación para el usuario: (a) quitar "MIDA" de `search_terms.primary` o
    exigir coocurrencia con "Panamá"/"Panama", (b) validar el dominio real
    (`urlparse(url).netloc`) contra el `site` esperado antes de guardar, en vez
    de confiar en el operador `site:` de DDG, (c) usar el dominio real como
    `source`, no el `site` configurado.

ACCIÓN: se detectó que `mark-all-ingested --limit 5` marca los primeros 5
pendientes por orden alfabético de archivo (`find_pending`), NO los mismos 5
seleccionados por score que aparecen en `pending_ingest.md` (`ingest` usa
`strategy=score` por defecto) — iba a marcar 4 artículos nunca revisados en
esta sesión. Se revirtió `sources/processed.json` (`git checkout`) y en su
lugar se usó `mark-ingested <url>` con las 5 URLs exactas ya revisadas
arriba. Bug adicional encontrado y corregido en el mismo paso: `mark_ingested()`
en `scripts/ingest.py` iteraba `processed.items()` sin filtrar la clave interna
`_gdelt_windows` (una lista, no un dict) → `AttributeError` al primer intento.
Fix: usar `article_entries(processed)` (ya definida en `core.py`) igual que el
resto de las funciones del módulo. Verificado con diff que las 5 URLs marcadas
coinciden exactamente con las 5 revisadas — ninguna otra fue tocada.

DIAGNÓSTICO AVANZADO (Paso 5 — pendientes bajó a 11, no llegó a 0, pero se
investigó igual porque "días sin artículos nuevos" ya está en alarma):
  - GitHub Actions (wiki_daily.yml) SÍ corrió todos los días recientes y con
    éxito: runs #66–75 (2026-07-31 a 2026-08-09), todos "completed / success"
    (verificado con la API de GitHub Actions, no solo por commits).
  - Pero no ha llegado NINGÚN artículo genuino desde 2026-07-30 (11 días) —
    confirmado por ausencia de commits "chore(sources): N>0 artículos" desde
    esa fecha. El workflow solo commitea cuando hay diffs reales.
  - `_gdelt_windows` en processed.json tiene 63 entradas (min quarterly
    windows). Análisis por año: 2017–2025 tienen 4/4 ventanas completas cada
    uno; **2015 y 2016 tienen 0/4 — nunca se han descargado**, a pesar de que
    `config/sources.yaml.gdelt.date_range.start = 2015-01-01` y de que
    `CLAUDE.md` fija la cobertura objetivo en "2015-02-19 → hoy". El resto
    (27 ventanas) son de 2026, con claves solapadas y de duración variable
    (ej. 20260618_20260701, _20260709, _20260717, _20260723) — indicio de que
    `fetch_gdelt_historical()` solo persiste `_gdelt_windows` en disco cada
    50 artículos guardados o al final de `run_fetch()`; si el job de Actions
    se corta (timeout de 30 min) antes de esos puntos de guardado, el
    progreso de esa corrida se pierde y el día siguiente reintenta desde el
    mismo punto, sin avanzar hacia 2015-2016 hasta agotar 2017+.
  - RSS: fuentes activas configuradas son IICA y La Prensa (confirmado en
    CLAUDE.md); no se verificó su respuesta HTTP hoy por límite de alcance
    de esta sesión.
  - CONCLUSIÓN: el sistema no está "atascado" por bloqueo/timeout de GDELT
    en general — está sano en 2017-2026, pero el backfill histórico 2015-2016
    (el inicio real de la cobertura objetivo) nunca se ha ejecutado, y el
    único aporte diario reciente (búsqueda DDG "prensa.com") es 100% ruido
    por el bug de "MIDA" descrito arriba.
  - RECOMENDACIÓN adicional: correr manualmente
    `python wiki_agro.py fetch-historical --years 2015-2016 --mode gdelt`
    en una sesión interactiva (sin límite de 30 min) para cerrar el hueco de
    2015-2016 de una vez, en vez de depender del job diario con timeout corto.

## 2026-08-10 03:40
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
