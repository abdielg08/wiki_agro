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

## 2026-07-13 16:02
FALSOS POSITIVOS: 5/5 artículos del lote ingest --limit 5 rechazados — 0% falsos
positivos mantenido, ninguno se ingestó al wiki.
  Causa raíz: coincidencia de la sigla "MIDA" con la Military Installation
  Development Authority de Utah (EE.UU.), no con el Ministerio de Desarrollo
  Agropecuario de Panamá. El fetch automático (GDELT/RSS) está trayendo
  artículos de noticias de Utah sobre centros de datos que no tienen relación
  con el agro panameño.
  Artículos rechazados:
    - 20260527_prensacom_news-2026-05-27-box-elder-data-center-opponents.json
      "Box Elder data center opponents hope for a vote" (sltrib.com) — centro de
      datos en Utah, MIDA = Military Installation Development Authority (Utah)
    - 20260529_prensacom_news-environment-2026-05-29-utah-governor-issues-order-prote.json
      "Utah Gov. Cox issues order to protect Great Salt Lake" (sltrib.com) —
      calidad de aire/agua en Utah, sin relación con Panamá
    - 20260519_prensacom_news-2026-05-19-kevin-oleary-data-center-timeline.json
      "Timeline: How the Kevin O'Leary data center plan came to be" (sltrib.com)
      — mismo caso de centro de datos en Utah
    - 20250613_prensacom_news-environment-2025-06-12-utah-nuclear-energy-state.json
      "Utah wants to process uranium on the Wasatch Front" (sltrib.com) —
      energía nuclear en Utah, MIDA = Military Installation Development
      Authority (Utah)
    - 20260707_prensacom_en-list-1506.json
      "The Persian Qanat" (whc.unesco.org) — sistema de riego histórico de Irán,
      sin relación con Panamá ni con el período 2015–hoy
  Acción: marcados como ingestados (mark-all-ingested) para vaciar la cola sin
  crear páginas de wiki. Recomendación para el usuario: la fuente
  "prensa.com" en config/ parece estar mal configurada o el filtro de
  keywords "MIDA" está generando falsos positivos sistemáticos — revisar
  scripts/prioritize.py o config de fuentes para excluir sltrib.com y
  agregar desambiguación de "MIDA" (Panamá) vs otras siglas.

## 2026-07-13 16:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-13 16:10
CORRECCIÓN + FALSOS POSITIVOS ADICIONALES: `mark-all-ingested --limit 5` usa un
orden distinto (alfabético por nombre de archivo, `find_pending`) al de
`ingest --limit 5` (por score de prioridad). Sobre los 7 artículos pendientes
al inicio de la sesión, ambos comandos operaron sobre conjuntos de 5 no
idénticos:
  - "New York Farm Bureau" (https://www.nyfb.org/) quedó marcado ingested=true
    por el paso 4 SIN haber sido revisado en el lote leído. Verificado ahora:
    es la organización gremial agrícola del estado de Nueva York (EE.UU.),
    sin ninguna relación con Panamá → confirmado como falso positivo,
    ningún contenido fue añadido al wiki por este artículo (correcto en
    sustancia, documentación corregida aquí).
  - "The Persian Qanat" (https://whc.unesco.org/en/list/1506) y "'Reef Saudi',
    a Successful Program Based on Rain-Fed Agriculture"
    (https://www.spa.gov.sa/en/N2096157) quedaron pendientes en vez de
    marcarse — se revisan y rechazan a continuación.
  Recomendación adicional: usar `mark-ingested <url>` por artículo individual
  (no `mark-all-ingested`) cuando se procesa un lote específico de
  `pending_ingest.md`, para evitar este desfase de orden.

FALSOS POSITIVOS: 2/2 artículos rechazados — 0% falsos positivos mantenido.
  - 20260707_prensacom_en-list-1506.json — "The Persian Qanat"
    (whc.unesco.org) — sistema de riego histórico (qanat) de Irán,
    patrimonio UNESCO, sin relación con Panamá ni con el período 2015–hoy.
  - 20260624_prensacom_en-n2096157.json — "'Reef Saudi', a Successful
    Program Based on Rain-Fed Agriculture" (spa.gov.sa) — programa de
    agricultura de secano del Reino de Arabia Saudita, sin relación con
    Panamá.
  Acción: marcados individualmente como ingestados con `mark-ingested` para
  vaciar la cola, sin crear páginas de wiki.

## 2026-07-13 16:20
DIAGNÓSTICO AVANZADO (Paso 4-5, pendientes=0 tras esta sesión):

**⚠ FALLO DEL SISTEMA — 3 días consecutivos sin artículos nuevos**
  Último commit que toca `sources/` fue `88389fe` (2026-07-10, 1 artículo —
  que además resultó ser falso positivo). No hay ningún commit sobre
  `sources/` para 2026-07-11, 2026-07-12 ni 2026-07-13. Incluso los días
  sin artículos nuevos normalmente generan un commit "0 artículos nuevos
  descargados" (porque `sources/processed.json` cambia al marcar ventanas
  GDELT completas) — la ausencia total de commits sugiere que el workflow
  `wiki_daily.yml` (cron diario 6am Panamá) dejó de ejecutarse o está
  fallando antes de llegar al paso de commit. Recomendación: el usuario
  debe revisar el historial de runs de Actions para `wiki_daily.yml` en
  GitHub (posible causa: cron deshabilitado por inactividad del repo,
  fallo silencioso en el paso `fetch`, o cambios recientes al workflow).

**Causa raíz de los falsos positivos — encontrada y corregida en esta sesión**
  12 de los últimos 14 artículos etiquetados con fuente "prensa.com" NO
  eran sobre Panamá. Causa: `scripts/fetch_news.py::fetch_ddg_search()`
  arma la consulta a DDGS().news() con el prefijo `site:prensa.com`, pero
  la búsqueda de noticias de DuckDuckGo no respeta ese operador de forma
  confiable — devuelve resultados de dominios arbitrarios (sltrib.com,
  thestar.com.my, worldbank.org, ieeexplore.ieee.org, spa.gov.sa,
  whc.unesco.org, nyfb.org, fox13now.com). El filtro `is_agro_relevant()`
  solo exige que aparezca alguna palabra clave genérica (p.ej. "MIDA",
  "agricultura", "riego") en el título/cuerpo, sin exigir relación con
  Panamá, así que términos como "MIDA" (que también es la sigla de la
  Military Installation Development Authority de Utah o la Malaysian
  Investment Development Authority) generaban falsos positivos
  sistemáticos etiquetados incorrectamente como fuente "prensa.com".
  Fix aplicado: `fetch_ddg_search()` ahora descarta cualquier resultado
  cuyo dominio no contenga literalmente el `site` configurado, antes de
  aplicar el filtro de palabras clave (scripts/fetch_news.py).
  Nota: el pipeline de GDELT (`fetch_gdelt_historical` en el mismo
  archivo) YA exige mención de Panamá en el query y filtra dominios
  bloqueados — no fue la fuente de estos falsos positivos.

**Bug adicional corregido**: `ingest.mark_ingested()` fallaba con
  `AttributeError` al iterar `processed.json` porque no excluía la clave
  interna `_gdelt_windows` (una lista, no un dict de metadatos). Corregido
  para usar `article_entries()` como el resto del código
  (scripts/ingest.py).

**Backfill histórico GDELT — brecha sin explicar**
  `sources/processed.json["_gdelt_windows"]` tiene 48 ventanas completas:
  36 trimestrales consecutivas desde 2017-03-30 hasta 2026-03-18, más 12
  ventanas de "alcance reciente" con inicio fijo 2026-06-18 y fin
  creciente (hasta 2026-07-09). Falta por completo el rango
  2015-01-01 → 2017-03-29 (~9 trimestres) exigido por config/sources.yaml
  (`date_range.start: 2015-01-01`) y por la cobertura objetivo de
  CLAUDE.md (2015-02-19 → hoy). No se identificó la causa exacta en esta
  sesión (posible timeout/rate-limit de GDELT en ventanas más antiguas,
  o ejecuciones anteriores con un rango de años distinto). El workflow
  manual `wiki_historical.yml` (crawl histórico dedicado) nunca se ha
  ejecutado — no existe `sources/historical_progress.json`. Recomendación:
  disparar `wiki_historical.yml` manualmente con `years=2015-2017
  mode=gdelt` para cerrar la brecha en vez de depender del catch-up lento
  del fetch diario.

**Métricas actualizadas** (ver wiki/metrics.md):
  Artículos descargados: 20 | ingestados: 20 | pendientes: 0
  Artículos reales (con contenido en el wiki): 6 | falsos positivos
  acumulados: 14 (7 nuevos hoy, 7 de sesiones previas)
  Páginas wiki: 20 (8 topics, 3 entidades, 6 resúmenes, 3 overview)
