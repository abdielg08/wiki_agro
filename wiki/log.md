---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-15
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

## 2026-07-15 00:05
ROUTINE: 8 artículos pendientes revisados — 8/8 FALSOS POSITIVOS (0 ingestados)
  Todos venían de la búsqueda DDG "prensa_agro" (config/sources.yaml, web_searches).
  Ninguno menciona Panamá, Panamá, ni ningún término panameño; todos fueron
  descartados sin crear páginas de wiki, y marcados como revisados
  (`mark-ingested`) para no bloquear la cola:
    1. "MITI working on simplified NCM..." (paultan.org) — MITI/MIDA Malasia
       (Ministry of Investment, Trade and Industry), no MIDA Panamá.
    2. "Box Elder data center opponents..." (sltrib.com) — MIDA = Military
       Installation Development Authority de Utah, EE.UU.
    3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com)
       — mismo MIDA de Utah.
    4. "Timeline: Kevin O'Leary data center plan..." (sltrib.com) — ídem.
    5. "Utah wants to process uranium..." (sltrib.com) — ídem, MIDA Utah +
       Utah National Guard.
    6. "The Persian Qanat" (whc.unesco.org) — patrimonio agrícola de Irán.
    7. "New York Farm Bureau" (nyfb.org) — agricultura de EE.UU.
    8. "'Reef Saudi'..." (spa.gov.sa) — agricultura de secano en Arabia Saudita.

  CAUSA RAÍZ IDENTIFICADA Y CORREGIDA:
  `scripts/fetch_news.py::fetch_ddg_search()` (usada por la búsqueda DDG
  "prensa_agro" con query `"... OR MIDA OR cosecha Panamá"`) NO aplicaba los
  filtros `_is_panama_related()` ni `_is_blocked_domain()` que sí tienen
  `fetch_rss()` y `fetch_gdelt_batch()`. El operador `site:prensa.com` de DDG
  no se respeta estrictamente en el buscador de noticias, así que artículos
  de dominios totalmente ajenos (paultan.org, sltrib.com, whc.unesco.org,
  nyfb.org, spa.gov.sa) se colaban por coincidir con términos genéricos como
  "agricultura", "cosecha" o el acrónimo "MIDA" (que también nombra
  entidades de Malasia y Utah). Además, `source` y `country` se asignaban
  ciegamente como `"prensa.com"`/`"PA"` sin validar el dominio real, lo que
  ocultaba el problema en `stats`.
  Fix aplicado: se agregaron los mismos chequeos (`_is_blocked_domain`,
  `_is_panama_related` sobre título/URL/cuerpo) a `fetch_ddg_search()`.

  BUG SECUNDARIO ENCONTRADO Y CORREGIDO:
  `scripts/ingest.py::mark_ingested()` iteraba `processed.items()` sin
  filtrar la clave interna `_gdelt_windows` (una lista, no un dict),
  causando `AttributeError: 'list' object has no attribute 'get'` en todo
  intento de `mark-ingested`. Se corrigió para usar `article_entries()`
  como ya hacían `find_pending()` y `mark_all_ingested()`.

  Resultado: Pendientes de ingesta = 0. Páginas wiki sin cambios (20).
  Tasa de falsos positivos de la sesión: 8/8 = 100% de lo pendiente, pero
  0% terminó en el wiki (regla de "0% falsos positivos" respetada).

## 2026-07-15 00:05
DIAGNÓSTICO: Backfill histórico GDELT — gap en 2015-01-01 → 2017-03-29
  `sources/processed.json._gdelt_windows` tiene 48 ventanas completadas,
  cubriendo continuamente 2017-03-30 → 2026-07-09. Faltan 9 ventanas
  trimestrales al inicio del rango objetivo:
    20150101_20150401, 20150402_20150701, 20150702_20150930,
    20151001_20151230, 20151231_20160330, 20160331_20160629,
    20160630_20160928, 20160929_20161228, 20161229_20170329
  Causa probable: `fetch_gdelt_batch()` no marca una ventana como completa
  si la petición HTTP falla (para reintentarla), pero el loop de
  `fetch_gdelt_historical()` avanza igual a la siguiente ventana sin
  reintentar en la misma corrida — si las ventanas 2015-2017 fallan de
  forma consistente (posible rate-limit/timeout de GDELT para rangos tan
  antiguos), nunca se completan mientras las corridas diarias siguen
  avanzando y completando ventanas más recientes.
  No se pudo confirmar la causa exacta en esta sesión: el entorno sandbox
  de Claude Code no tiene salida de red a `api.gdeltproject.org` (proxy
  403), a diferencia de GitHub Actions donde el fetch diario sí corre.
  Sin nuevos artículos en `sources/` hoy 2026-07-15 (última corrida de
  Actions fue 2026-07-14, 1 artículo) — dentro del umbral normal (<3 días).
  Acción sugerida para próxima sesión: revisar logs de Actions del fetch
  diario para ver si las 9 ventanas 2015-2017 devuelven error o vacío, y
  considerar disparar manualmente `wiki_historical.yml` con
  `years=2015-2017 mode=gdelt` si el fetch diario sigue sin poder
  completarlas.
