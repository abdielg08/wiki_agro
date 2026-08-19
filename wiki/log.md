---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-19
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

## 2026-08-19 00:00
FALSOS POSITIVOS: 5/5 artículos del lote de ingesta rechazados — NO ingestados al wiki
  Causa raíz: colisión de la sigla "MIDA" en la fuente prensa.com (búsqueda ddgs/DDGS.news
  en scripts/fetch_news.py). "MIDA" también corresponde a Military Installation Development
  Authority (Utah, EE.UU.) y aparece en coberturas de MITI/MARii (Malasia). Ninguno de los
  5 artículos menciona a Panamá (0 coincidencias de "panama"/"panamá" en el texto completo).
  Artículos rechazados:
    - 20260708_prensacom_...miti-working-on-simplified-ncm... → MITI/MIDA Malasia (incentivos industriales), no Panamá
    - 20260527_prensacom_...box-elder-data-center-opponents → MIDA = Military Installation Development Authority, Utah
    - 20260529_prensacom_...utah-governor-issues-order-prote → mismo caso, Utah/Great Salt Lake
    - 20260519_prensacom_...kevin-oleary-data-center-timeline → mismo caso, Utah
    - 20260307_prensacom_...cultural-rules-for-staying-with-locals-abro → sin relación agropecuaria ni con Panamá
  Acción: marcados como `ingested: true` en processed.json vía `mark-ingested <url>`
  individual (ver bug de mark-all-ingested abajo), SIN crear páginas en
  wiki/summaries|topics|entities.
  Recomendación: filtrar por "Panama"/"Panamá" en la query de fetch_news.py (DDGS.news) para
  reducir falsos positivos futuros de la sigla MIDA.

## 2026-08-19 16:14
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-19 16:20
BUGFIX (scripts/ingest.py): dos bugs encontrados y corregidos durante la sesión de rutina:
  1. `mark_ingested()` iteraba `processed.items()` crudo, incluyendo la clave interna
     `_gdelt_windows` (una lista, no dict) → `AttributeError: 'list' object has no
     attribute 'get'` al ejecutar `mark-ingested <url>`. Corregido: ahora itera
     `article_entries(processed)`, que ya filtra las claves `_meta`.
  2. `mark_all_ingested()` seleccionaba los "primeros N pendientes" con `find_pending()`
     (orden alfabético por nombre de archivo), mientras que `ingest --limit N` (lo que
     realmente se le muestra a Claude para procesar) usa `prioritize()` con `strategy="score"`.
     Como resultado, `mark-all-ingested --limit 5` marcaba artículos DISTINTOS a los 5
     mostrados en pending_ingest.md — de los 5 artículos rechazados como falsos positivos
     arriba, solo 1 quedó marcado correctamente por `mark-all-ingested`. Corregido:
     `mark_all_ingested()` ahora usa el mismo `prioritize(strategy="score")` que
     `run_prepare()`, garantizando que marque exactamente lo que se mostró.
  Impacto: sin este fix, `mark-all-ingested` podía marcar artículos no revisados como
  ingestados (saltándolos silenciosamente) mientras dejaba los realmente procesados
  pendientes — riesgo de falsos negativos en las métricas de cobertura.

## 2026-08-19 16:35
FALSOS POSITIVOS: 5/5 artículos del segundo lote rechazados — NO ingestados al wiki
  Ninguno menciona a Panamá (0 coincidencias en full_text+summary_raw), pese a tener
  `country: PA` en su metadata (ver bug de causa raíz abajo):
    - Maine.gov — Division of Agricultural Resource Development (agricultura de Maine, EE.UU.)
    - agenciabrasil.ebc.com.br — Finep financia agricultura familiar en Brasil
    - whc.unesco.org — sistema de qanats persas (Irán), patrimonio UNESCO
    - heraldo.es — AEGA, organización agraria de Aragón, España
    - nyfb.org — New York Farm Bureau, EE.UU.
  Acción: marcados como `ingested: true` vía `mark-ingested <url>` individual, sin crear
  páginas de wiki.

## 2026-08-19 16:40
BUGFIX (scripts/fetch_news.py): causa raíz de los 10 falsos positivos de esta sesión
  (2 lotes de 5, ambos de la fuente "prensa.com"), identificada y corregida:
  - La fuente "prensa.com" en config/sources.yaml usa `fetch_ddg_search()` (búsqueda
    DDGS.news) con `site: "prensa.com"` y query
    `"agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá"`.
  - `fetch_ddg_search()` NO aplicaba el filtro `_is_panama_related()` que sí tiene
    `fetch_rss()` — solo llamaba a `is_agro_relevant()` (términos agro genéricos, sin
    exigir Panamá). Además, el operador `site:` de DDGS no se respeta de forma
    confiable por el motor de búsqueda subyacente: los 10 resultados problemáticos
    venían de dominios completamente ajenos a prensa.com (maine.gov, ebc.com.br,
    whc.unesco.org, heraldo.es, nyfb.org, sltrib.com, paultan.org, msn.com) — nunca de
    prensa.com. `country: "PA"` también estaba hardcodeado sin verificar el contenido.
  - Corregido: se agregó `_matches_site(url, site)` (nuevo helper, valida que el
    dominio del resultado coincida con el `site` configurado — filtro post-búsqueda
    ya que DDGS no lo garantiza) y se aplicó el mismo filtro `_is_panama_related()`
    (más chequeo de "panam" en el cuerpo) que ya usa `fetch_rss()`. También se añadió
    `_is_blocked_domain()` a esta ruta, que antes solo se aplicaba en RSS.
  Impacto esperado: la fuente "prensa.com" (DDG search) dejará de traer artículos de
  Maine, Brasil, Irán, España, Utah y Malasia — puede que ahora traiga 0 resultados
  hasta que DDGS realmente indexe contenido de prensa.com sobre agro panameño, lo cual
  es preferible a seguir violando la regla de 0% falsos positivos. Cambio no probado
  en vivo (requiere acceso de red a DDGS no verificado en esta sesión) — próxima
  routine debe confirmar que "prensa.com" sigue aportando artículos válidos o
  documentar si quedó en 0.

## 2026-08-19 16:50
FALSOS POSITIVOS: 3/3 artículos del tercer lote rechazados — NO ingestados al wiki
  Ninguno menciona a Panamá:
    - heraldo.es — Arvensis Agro amplía instalaciones en Aragón, España
    - spa.gov.sa — Programa "Reef Saudi" de agricultura de secano en Arabia Saudita
    - heraldo.es — Nuevo consejero de Medio Ambiente de Aragón, España
  Acción: marcados como `ingested: true` vía `mark-ingested <url>` individual.

## 2026-08-19 16:52
RESUMEN DE SESIÓN: Cola de ingesta vaciada — Pendientes de ingesta = 0
  Total revisados vía pending_ingest.md: 13 artículos (3 lotes: 5+5+3)
  Falsos positivos rechazados: 13/13 (100%) — todos de la fuente "prensa.com" (DDG
  search), ninguno mencionaba a Panamá; ver diagnóstico de causa raíz arriba.
  Artículos ingestados al wiki (páginas nuevas/actualizadas): 0
  Nota sobre la meta de "≥5 artículos ingestados por sesión": no se cumplió, porque
  ningún artículo pendiente era válido — priorizar 0% falsos positivos (regla
  innegociable de CLAUDE.md) sobre la meta de volumen.
  Bugs corregidos en la sesión: mark_ingested() (crash con _gdelt_windows), 
  mark_all_ingested() (orden alfabético vs. score), y fetch_ddg_search() (sin filtro
  Panamá, sin verificación real de site:) — ver entradas de BUGFIX arriba.

## 2026-08-19 17:05
AUDITORÍA DE INTEGRIDAD: 4 artículos adicionales marcados `ingested: true` sin revisión
  Al ejecutar `mark-all-ingested --limit 5` ANTES de descubrir el bug de ordenamiento
  (ver BUGFIX 16:20), ese primer llamado marcó 5 artículos según el orden alfabético
  incorrecto — no los 5 que aparecían en pending_ingest.md. 1 de esos 5 (msn.com,
  cultural-rules-for-staying-with-locals-abro) coincidía por casualidad con el lote
  revisado. Los otros 4 NUNCA pasaron por revisión editorial:
    - ieeexplore.ieee.org/document/10945742 — "Ambient IoT: Communications Enabling
      Precision Agriculture" (paper técnico 6G, sin relación con Panamá)
    - heraldo.es/.../aragon-celebra-sentencia-supremo... — sentencia sobre espacio para
      cerdos en granjas de Aragón, España
    - archive.org/details/Cataloguedipter2SaoP — catálogo de dípteros de Sudamérica
      (Secretaria da Agricultura, Brasil, 1966/67) — nota: fecha del artículo 2016-05-13,
      dentro del rango de gap 2015-2016, pero contenido no es de Panamá
    - sltrib.com/.../utah-nuclear-energy-state — acuerdo de energía nuclear en Utah,
      menciona "MIDA" = Military Installation Development Authority (mismo patrón de
      colisión de sigla que los demás falsos positivos de esta sesión)
  Verificación: se releyó el `full_text`/`summary_raw` completo de los 4 — 0 menciones
  de "panama"/"panamá" en todos. Confirmado que también son falsos positivos legítimos;
  ningún artículo real de Panamá fue marcado incorrectamente como ingestado.
  Total real de falsos positivos de la sesión: 17 (13 revisados en pending_ingest.md + 4
  detectados en esta auditoría posterior).

## 2026-08-19 17:00
DIAGNÓSTICO — Backfill GDELT: gap real en 2015-2016
  Al analizar `_gdelt_windows` en processed.json (70 ventanas) por año: 2017-2025 tienen
  4/4 trimestres completados cada uno (36 ventanas históricas reales); 2015 y 2016 tienen
  0/4 cada uno — nunca se ejecutó backfill para esos años. Las 34 ventanas restantes
  (etiquetadas "2026") no son backfill trimestral: son la ventana rodante del fetch diario
  (`wiki_daily.yml`, formato `20260618_<fecha-de-hoy>`, se re-registra cada corrida) y no
  cuentan para el progreso del backfill histórico.
  Como la cobertura objetivo del wiki es "2015-02-19 → hoy" (CLAUDE.md), este es el único
  vacío real pendiente. `wiki_historical.yml` (crawl histórico) es de disparo manual
  (workflow_dispatch, rango default 2010-2025) — no hay evidencia de que se haya corrido
  para 2015-2016 específicamente.
  Recomendación (acción manual, fuera del alcance de esta rutina): disparar
  `wiki_historical.yml` con `years: "2015-2016"`, `mode: gdelt` para cerrar el gap.
