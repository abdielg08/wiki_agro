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

## 2026-08-08 00:00
ROUTINE: 16 pendientes revisados — 16/16 falsos positivos (0 artículos reales ingestados)
  Todos los 16 artículos en cola (marcados fuente "prensa.com") resultaron ser de dominios
  no relacionados con Panamá: heraldo.es y sltrib.com/paultan.org/msn.com (Utah "MIDA" =
  Military Installation Development Authority; Malaysia MITI/MARii), agenciabrasil.ebc.com.br
  (Brasil), whc.unesco.org (Irán), heraldo.es ×2 (Aragón, España), ieeexplore.ieee.org
  (paper genérico sin país), archive.org (catálogo de dípteros 1966). Ninguno mencionaba
  Panamá ni agro panameño. Documentados aquí y marcados como ingestados (manejados, sin
  contenido creado en wiki/) siguiendo el precedente del 2026-06-22.

  CAUSA RAÍZ IDENTIFICADA y CORREGIDA en scripts/fetch_news.py::fetch_ddg_search():
  - El operador `site:` en las búsquedas DuckDuckGo (vía ddgs.news()) no se estaba
    respetando de forma confiable — una búsqueda `site:prensa.com ... MIDA ...` devolvía
    resultados de dominios globales sin relación (heraldo.es, sltrib.com, ieeexplore.ieee.org,
    archive.org, etc.) que simplemente mencionaban algún término agro genérico o "MIDA"
    (coincide con "Military Installation Development Authority" en Utah y con agencias de
    Malaysia, no con el Ministerio de Desarrollo Agropecuario de Panamá).
  - Además, el campo "source" se fijaba como `site or name` (ej. "prensa.com") y "country"
    como "PA" de forma incondicional, SIN verificar el dominio real de la URL devuelta —
    por eso los 16 artículos aparecían mal etiquetados como fuente "prensa.com" / país PA
    en sources/processed.json y en `wiki_agro.py stats`.
  - FIX: se añadió un filtro que descarta cualquier resultado cuyo dominio real
    (urlparse(url).netloc) no contenga el `site` configurado, antes de aceptar el artículo.
    El campo "source" ahora usa el `name` de la búsqueda en vez de reusar `site` sin validar.

  BUG SEPARADO corregido en scripts/ingest.py::mark_ingested(): iteraba
  `processed.items()` sin filtrar la clave interna `_gdelt_windows` (una lista, no un
  dict), causando `AttributeError` en cada llamada a `mark-ingested`. Se cambió a iterar
  `article_entries(processed).items()` (igual que el resto del código).

  DIAGNÓSTICO GDELT: `_gdelt_windows` tiene 63 ventanas marcadas completas, pero:
  (a) faltan las ventanas 2015-01-01 → 2017-03-29 (~9 ventanas) — el rango histórico más
      antiguo aún no se ha procesado a pesar de que `config/sources.yaml` ya apunta a
      start=2015-01-01; debería auto-completarse en la próxima corrida ya que el loop
      siempre reintenta desde `start`.
  (b) desde 2026-06-18 se están generando ventanas nuevas casi a diario
      (20260618_20260623, 20260618_20260624, ... 20260618_20260806) — el trimestre en
      curso se re-marca "completo" cada día con una fecha final distinta (ayer), en vez
      de reutilizar una clave estable, inflando el conteo sin aportar cobertura nueva.
      No se corrigió en esta sesión (bajo impacto, no genera falsos positivos) — queda
      documentado para una futura sesión de mantenimiento del pipeline de fetch.
  Ningún artículo real vino de GDELT en esta sesión ni en las anteriores — los 6 artículos
  reales en el wiki son datos semilla manuales, no fetches automáticos confirmados.

  Estado final: Pendientes de ingesta = 0. Total páginas wiki sin cambios: 20.
