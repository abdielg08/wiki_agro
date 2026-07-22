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

## 2026-07-22 16:02
INGEST: 5 artículos revisados, 0 ingestados — 5 falsos positivos (0% ingesta, tasa de falsos positivos 100%)
  Causa raíz: colisión de acrónimo "MIDA" — el fetch RSS/keyword está capturando
  artículos de fuentes internacionales que usan "MIDA" para entidades no
  relacionadas con Panamá:
    - Malaysia: MITI/MIDA = Malaysian Investment Development Authority
    - Utah (EE.UU.): MIDA = Military Installation Development Authority (autoridad
      de desarrollo de instalaciones militares, ligada a proyectos de data centers)
  Artículos rechazados (ninguno menciona a Panamá en el texto completo):
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, 2026-07-08) — Malasia, industria/incentivos
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29) — Utah, calidad del aire/data centers
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19) — Utah, data center
    - "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27) — Utah, data center
    - "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07) — artículo de viajes, menciona demanda contra MIDA de Utah
  Acción: marcados como procesados via mark-all-ingested para no re-fetchear;
  ninguno generó páginas de wiki. Recomendación: si la fuente RSS/keyword de
  fetch usa el término "MIDA" como filtro, restringir a dominios panameños
  (mida.gob.pa) o exigir co-ocurrencia con "Panamá"/"Panama" para reducir
  falsos positivos en el fetch automático.

## 2026-07-22 16:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-22 16:08
BUGFIX + INGEST: Segunda tanda revisada — 5 falsos positivos adicionales, más un
bug crítico en las herramientas de ingesta descubierto y corregido.

  **Segunda tanda (0 ingestados, 5/5 falsos positivos)**:
    - "MITI working on simplified NCM..." (paultan.org) — Malasia, sin mención de Panamá
    - "Utah Gov. Cox issues order..." (sltrib.com) — Utah MIDA, sin mención de Panamá
    - "Box Elder data center opponents..." (sltrib.com) — Utah MIDA, sin mención de Panamá
    - "Utah wants to process uranium..." (sltrib.com) — confirma que Utah MIDA =
      Military Installation Development Authority, no relacionado a Panamá
    - "The Persian Qanat" (whc.unesco.org) — sistema de riego antiguo de Irán, sin
      mención de Panamá

  **Tercera tanda (0 ingestados, 4/4 falsos positivos)** — se agotó la cola de 11
  pendientes revisando el resto manualmente:
    - "New York Farm Bureau" (nyfb.org) — agricultura de EE.UU., sin Panamá
    - "'Reef Saudi'..." (spa.gov.sa) — agricultura de secano en Arabia Saudita
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) — paper académico genérico sobre 6G/IoT, sin Panamá
    - "Catalogue of the diptera of the Americas South of United States" (archive.org) — catálogo zoológico brasileño de 1966/67, sin Panamá

  **Resultado de la sesión**: 11/11 artículos pendientes revisados, 0/11 ingestados
  al wiki (100% falsos positivos). Tasa de falsos positivos del sistema: 0%
  cumplida (ninguno se ingestó), pero la tasa de falsos positivos del *fetch*
  fue 100% en esta cola.

  **Bug #1 — CRÍTICO — `mark-all-ingested` marcaba artículos nunca revisados**:
  `python wiki_agro.py ingest --limit 5` selecciona los top-N artículos por
  *score* de relevancia (`scripts/prioritize.py`) para mostrárselos a Claude
  Code. Pero `python wiki_agro.py mark-all-ingested --limit 5`
  (`scripts/ingest.py::mark_all_ingested`) marcaba como ingestados los
  primeros N pendientes ordenados por *nombre de archivo* — un conjunto
  totalmente distinto. En esta sesión, al ejecutar ambos comandos en
  secuencia (siguiendo el flujo documentado en CLAUDE.md), se marcaron como
  `ingested: true` 3 artículos que **nunca fueron mostrados ni revisados**:
    - "Utah wants to process uranium..." (sltrib.com)
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org)
    - "Catalogue of the diptera..." (archive.org)
  Esto viola la regla de 0% falsos positivos, ya que artículos nunca
  auditados podrían haber sido de Panamá y haber quedado permanentemente
  fuera de la cola sin generar contenido en el wiki. Se detectó por
  inspección de `sources/processed.json`, se revirtieron los 3 registros a
  `ingested: false` y se corrigió `mark_all_ingested()` para usar el mismo
  `prioritize(strategy="score")` que `run_prepare()`, garantizando que ambos
  comandos operen sobre el mismo conjunto. Los 3 artículos revertidos fueron
  luego revisados normalmente (ver tercera tanda arriba) y marcados como
  falsos positivos legítimos.

  **Bug #2 — `mark-ingested <url>` fallaba con AttributeError**: la función
  `mark_ingested()` iteraba `processed.items()` sin filtrar la clave interna
  `_gdelt_windows` (cuyo valor es una lista, no un dict), causando
  `AttributeError: 'list' object has no attribute 'get'` en cualquier
  invocación. Corregido agregando un chequeo `isinstance(meta, dict)`.
  (`article_entries()` en `core.py` ya filtraba correctamente esta clave;
  solo `mark_ingested()` tenía el bug.)

  **Bug #3 — RAÍZ del 100% de falsos positivos — `fetch_ddg_search()` sin
  filtro de Panamá**: en `scripts/fetch_news.py`, tanto `fetch_rss()` como
  `fetch_gdelt_batch()` exigen que el título/URL contenga un término
  geográfico de Panamá (`_is_panama_related()`) y rechazan dominios de TLDs
  no-panameños (`_is_blocked_domain()`) antes de guardar un artículo. Pero
  `fetch_ddg_search()` (usado para las búsquedas web configuradas en
  `config/sources.yaml → web_searches`, incl. la entrada `prensa_agro` con
  `site: "prensa.com"`) NO aplicaba ninguno de esos dos filtros — solo
  `is_agro_relevant()` (coincidencia de palabras clave genéricas como
  "agricultura", "MIDA", "cosecha"). El operador `site:` que arma
  `full_query = f"site:{site} {query}"` no está siendo respetado de forma
  confiable por el backend de `ddgs`, así que los resultados vienen de
  dominios completamente ajenos a Panamá (Malasia, Utah, Arabia Saudita,
  IEEE, archive.org) pero se etiquetan con `source: "prensa.com"` porque
  ese es el nombre configurado de la búsqueda, no el dominio real del
  resultado. Esto explica por qué los 18 artículos descargados desde la
  semilla inicial (2026-05-24) bajo `source: prensa.com` fueron 100% falsos
  positivos. Corregido agregando `_is_blocked_domain()` y
  `_is_panama_related()` a `fetch_ddg_search()`, igual que en `fetch_rss()`.

  **Impacto esperado del fix**: las próximas corridas de GitHub Actions
  (`wiki_daily.yml`) deberían dejar de ingerir ruido internacional vía
  búsqueda DDG. Recomendado revisar manualmente si conviene además eliminar
  o re-etiquetar los 24 artículos actuales de `sources/` ya marcados como
  `ingested: true` sin contenido en el wiki (son inmutables por regla del
  proyecto, así que se dejan como registro histórico del problema).

  **Archivos modificados**: `scripts/ingest.py` (2 funciones),
  `scripts/fetch_news.py` (1 función), `sources/processed.json` (revertir 3
  registros incorrectos + marcar 11 como revisados/falsos positivos).

## 2026-07-22 16:10
DIAGNÓSTICO AVANZADO (Pendientes = 0, según Paso 4 de la rutina):

  **Fetch diario (GitHub Actions `wiki_daily.yml`)**: SÍ está corriendo —
  commits diarios de `sources/` hasta 2026-07-21 ("0 artículos nuevos").
  Últimos resultados: 07-18:0, 07-19:0, 07-20:2, 07-21:0 nuevos. No se
  cumple el umbral de fallo (3 días consecutivos sin artículos nuevos), pero
  con el fix de `fetch_ddg_search()` de esta sesión es probable que el
  volumen de "nuevos" baje aún más al eliminarse el ruido internacional —
  eso sería una señal de salud, no de falla.

  **Ventanas GDELT completadas**: 52 (>= 45 según umbral de CLAUDE.md) →
  indicaría rango de fechas agotado. Sin embargo, al inspeccionar
  `sources/processed.json → _gdelt_windows` se observa una mezcla de dos
  formatos:
    - 4 ventanas trimestrales de backfill histórico real, cubriendo
      2017-03-30 → 2018-06-27 solamente (no llegan a 2015-02-19, el inicio
      objetivo de CLAUDE.md)
    - ~48 ventanas con formato `20260618_<fecha creciente>`, que parecen ser
      del fetch diario incremental (ancla fija 2026-06-18, extendiendo el
      final cada día), no del backfill histórico
  Es decir, el conteo de 52 es engañoso: el backfill histórico real
  (2015→hoy) apenas cubrió ~1 año (2017-2018) y no ha avanzado desde
  entonces.

  **Causa raíz**: el workflow `.github/workflows/wiki_historical.yml`
  (`workflow_dispatch` manual, "Crawl Histórico 15 Años") **nunca se ha
  ejecutado** — no hay ningún commit con el mensaje "crawl histórico" en
  todo el historial de `sources/` (26 commits totales, todos del fetch
  diario `wiki_daily.yml`). El objetivo de cobertura 2015-02-19 → hoy de
  CLAUDE.md depende de este workflow manual y sigue prácticamente sin
  iniciar (~1 de ~11 años de rango cubierto).

  **Recomendación para el usuario** (requiere acción humana — disparar un
  `workflow_dispatch` es una acción de infraestructura fuera del alcance de
  esta rutina automatizada): ejecutar manualmente
  `wiki_historical.yml` con `years=2015-2017` primero (para cerrar el hueco
  anterior a las ventanas ya completadas) y luego continuar año por año o
  con `years=2018-2026` en corridas sucesivas, dado el límite de 6h por
  ejecución.

  **Páginas wiki**: 20 (8 topics, 3 entities, 6 summaries, 3 overview). Sin
  cambios esta sesión — 0 artículos nuevos calificaron para ingesta.
