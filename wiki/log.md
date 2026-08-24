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

## 2026-08-24 00:17
FALSOS POSITIVOS: 5/5 artículos del lote de ingesta descartados — ninguno es sobre agro de Panamá.
  El fetch (GDELT/keyword "MIDA") capturó ruido de coincidencias de sigla, no de contenido agropecuario panameño.
  - "MITI working on simplified NCM..." (paultan.org) — MIDA = Malaysian Investment Development Authority (Malasia), no agro.
  - "Box Elder data center opponents..." (sltrib.com) — MIDA = Military Installation Development Authority (Utah, EE.UU.), centros de datos.
  - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) — mismo MIDA de Utah, calidad de aire/agua, no agro Panamá.
  - "Timeline: Kevin O'Leary data center plan..." (sltrib.com) — mismo MIDA de Utah, centro de datos.
  - "Cultural Rules For Staying With Locals Abroad" (msn.com) — artículo de viajes, sin relación con MIDA/agro; capturado por error del fetch.
  Acción: no se creó ninguna página wiki/summary. Los 5 se marcaron como ingestados vía mark-all-ingested para vaciar la cola (no vuelven a aparecer en pending).
  Nota para diagnóstico de fuentes: el fetch por RSS/GDELT está trayendo resultados de "MIDA" sin filtro de país — considerar afinar el query a "MIDA Panamá" o "Ministerio de Desarrollo Agropecuario" en scripts/ de fetch.

## 2026-08-24 00:18
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
  NOTA: esta entrada la generó automáticamente `mark-all-ingested`, pero se detectó que ese comando
  marcó artículos DISTINTOS a los 5 que Claude realmente revisó (ver bug documentado abajo).
  Los cambios de esa llamada fueron revertidos (`git checkout -- sources/processed.json`) y se
  volvieron a marcar los 5 artículos correctos con `mark-ingested <url>` uno por uno.

## 2026-08-24 00:25
BUG DE HERRAMIENTA: `mark-all-ingested --limit N` no corresponde a `ingest --limit N`.
  `ingest --limit N` selecciona artículos por score de prioridad (scripts/prioritize.py).
  `mark-all-ingested --limit N` selecciona los primeros N pendientes por orden alfabético de archivo
  (scripts/ingest.py: find_pending() ordena por SOURCES_DIR.glob("*.json") sorted, no por prioridad).
  Resultado: al ejecutar ambos comandos en secuencia con el mismo --limit, se marcan como "ingested"
  artículos DIFERENTES a los que Claude realmente leyó y evaluó en pending_ingest.md — incluyendo,
  en esta sesión, un artículo IEEE sobre "Ambient IoT: Communications Enabling Precision Agriculture"
  que nunca fue revisado antes de marcarse.
  Bug adicional: `mark-ingested <url>` (comando individual) falla con
  `AttributeError: 'list' object has no attribute 'get'` porque itera sobre TODAS las claves de
  processed.json, incluida `_gdelt_windows` (que es una lista, no un dict de metadata de artículo).
  Mitigación aplicada esta sesión: se revirtió el marcado incorrecto y se marcaron los artículos
  correctos editando processed.json directamente en Python, replicando la lógica de mark_ingested()
  pero saltando la clave `_gdelt_windows`.
  RECOMENDACIÓN: corregir scripts/ingest.py — (a) find_pending() en mark_all_ingested debe usar el
  mismo orden de prioridad que ingest(), o mejor, mark-all-ingested debería marcar exactamente los
  artículos listados en el pending_ingest.md más reciente; (b) mark_ingested() debe excluir claves
  que no sean dicts de artículo (como _gdelt_windows) al iterar processed.items().
  Hasta que se corrija: usar SIEMPRE `mark-ingested '<url>'` individual por cada URL revisada,
  nunca `mark-all-ingested`.

## 2026-08-24 00:20
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-24 00:30
FIX: corregidos dos bugs en scripts/ingest.py (ver diagnóstico de las 00:25):
  1. mark_ingested() ahora itera article_entries(processed) en vez de processed.items(),
     evitando el AttributeError al toparse con la clave interna `_gdelt_windows`.
  2. mark_all_ingested() ahora lee las URLs directamente de pending_ingest.md (el lote exacto
     que ingest() generó y que Claude procesó), en vez de re-derivar un "pendiente" por orden
     alfabético de archivo. Así mark-all-ingested siempre coincide con lo que realmente se revisó.
  Verificado: tras el fix, mark-all-ingested --limit 5 marcó exactamente los 5 artículos del
  pending_ingest.md vigente (Aragón/heraldo.es, Utah uranio/sltrib, Maine ARD, Finep/Brasil,
  Qanat persa/UNESCO) — ninguno inesperado.

## 2026-08-24 00:30
FALSOS POSITIVOS: 5/5 artículos del segundo lote de ingesta descartados — ninguno es sobre agro de Panamá.
  Confirma el mismo patrón sistémico: el fetch trae contenido agropecuario genérico/global sin
  filtro de país, o coincidencias de sigla ("MIDA") ajenas a Panamá.
  - "Aragón celebra la sentencia del Supremo..." (heraldo.es) — Aragón, España; ganadería porcina española, no Panamá.
  - "Utah wants to process uranium..." (sltrib.com) — mismo MIDA de Utah (Military Installation Development Authority), energía nuclear, no agro.
  - "Agricultural Resource Development Division" (maine.gov) — agencia agrícola del estado de Maine, EE.UU., no Panamá.
  - "Finep vai pagar R$ 220 milhões..." (agenciabrasil.ebc.com.br) — agricultura familiar en Brasil, no Panamá.
  - "The Persian Qanat" (whc.unesco.org) — sistema de riego histórico de Irán (patrimonio UNESCO), no Panamá.
  Acción: no se creó ninguna página wiki/summary. Los 5 se marcaron como ingestados (mark-all-ingested,
  ya corregido) para vaciar la cola.

## 2026-08-24 00:35
FALSOS POSITIVOS: 7/7 artículos del tercer y último lote pendiente descartados — ninguno es sobre agro de Panamá.
  - "AEGA pide elecciones al campo en Aragón..." (heraldo.es) — política agraria de Aragón, España.
  - "New York Farm Bureau" (nyfb.org) — gremio agrícola del estado de Nueva York, EE.UU.
  - "Arvensis Agro amplía sus instalaciones..." (heraldo.es) — empresa aragonesa de nutrición vegetal, España.
  - "'Reef Saudi'..." (spa.gov.sa) — programa de agricultura de secano en Arabia Saudita.
  - "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es) — gobierno regional de Aragón, España.
  - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) — paper técnico 6G/IoT genérico, sin mención de Panamá.
  - "Catalogue of the diptera of the Americas South of United States" (archive.org) — catálogo de zoología (moscas) de 1966/67, ni siquiera es noticia agropecuaria.
  Acción: no se creó ninguna página wiki/summary. Los 7 se marcaron como ingestados para vaciar la cola.

## 2026-08-24 00:40
DIAGNÓSTICO DE RAÍZ Y FIX: se identificó la causa de los 17/17 falsos positivos de esta sesión.
  scripts/fetch_news.py tiene tres mecanismos de fetch (RSS, DuckDuckGo/ddgs, GDELT) y dos filtros
  de relevancia geográfica: `_is_blocked_domain()` (rechaza TLDs no-panameños conocidos) y
  `_is_panama_related()` (exige al menos un término panameño explícito en título/URL — diseñado
  específicamente para evitar falsos positivos por sigla, ej. "MIDA" también es la Malaysian
  Investment Development Authority y la Military Installation Development Authority de Utah).
  RSS (fetch_rss) y GDELT (fetch_gdelt_window) SÍ aplican ambos filtros. `fetch_ddg_search()`
  (búsqueda vía DuckDuckGo/ddgs, la que alimenta la mayoría de los artículos etiquetados
  "prensa.com" en processed.json) NO los aplicaba — solo llamaba a `is_agro_relevant()`, que
  únicamente verifica términos agropecuarios genéricos sin exigir relación con Panamá. Además,
  el operador `site:` de DDG no se respeta de forma confiable, así que la búsqueda devolvía
  resultados de dominios completamente ajenos (paultan.org, sltrib.com, heraldo.es, nyfb.org,
  spa.gov.sa, ieeexplore.org, archive.org, maine.gov, agenciabrasil.ebc.com.br, whc.unesco.org,
  msn.com) etiquetados igualmente como fuente "prensa.com" — explicando el 100% de falsos
  positivos de esta sesión.
  FIX aplicado en scripts/fetch_news.py: fetch_ddg_search() ahora aplica `_is_blocked_domain(url)`
  y `_is_panama_related(title, url)` antes de aceptar un resultado, igual que fetch_rss() y
  fetch_gdelt_window(). No se modificó `is_agro_relevant()` ni las listas `_PANAMA_TERMS` /
  `_NON_PA_TLDS` (ya bien diseñadas, solo faltaba invocarlas en esta ruta).
  Pendiente de verificar: correr un fetch real (GitHub Actions o `python wiki_agro.py fetch`) para
  confirmar que el volumen de artículos capturados por DDG baja a ~0 con el query actual, y si
  hace falta, revisar/ajustar el `query`/`site` de los search_cfg en la config de fuentes para que
  la búsqueda incluya explícitamente "Panamá" en el texto de búsqueda (no solo como filtro post-hoc).

## 2026-08-24 00:22
INGEST: 7 artículos marcados como ingestados por sesión Claude Code
