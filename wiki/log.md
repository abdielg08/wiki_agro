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

## 2026-07-07 00:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-07 (routine)
INGEST: 6 pendientes revisados — 6 falsos positivos rechazados, 0 artículos reales
  Ningún artículo agregado al wiki esta sesión (0% falsos positivos mantenido: nada se ingestó al wiki).
  Falsos positivos detectados y marcados como revisados (ingested=true, sin páginas creadas):
    - sltrib.com "Kevin O'Leary data center timeline" (2026-05-19) — MIDA = Military Installation
      Development Authority de Utah, no Ministerio de Desarrollo Agropecuario de Panamá
    - sltrib.com "Box Elder data center opponents" (2026-05-27) — ídem, MIDA-Utah
    - sltrib.com "Utah Gov. Cox... data centers" (2026-05-29) — ídem, MIDA-Utah
    - sltrib.com "Utah nuclear energy state" (2025-06-13) — ídem, MIDA-Utah
    - nyfb.org "New York Farm Bureau" (2026-06-17) — agricultura de Nueva York, no de Panamá
    - spa.gov.sa "'Reef Saudi' rain-fed agriculture" (2026-06-24) — agricultura de Arabia Saudita
  CAUSA RAÍZ identificada y corregida en `scripts/fetch_news.py::fetch_ddg_search()`:
    La búsqueda web `web_searches.prensa_agro` (config/sources.yaml) usa DuckDuckGo con la query
    "agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá" y `site:prensa.com`.
    DDG no respeta el operador `site:` de forma confiable en su backend de noticias, y
    `fetch_ddg_search()` no verificaba el dominio real del resultado ni aplicaba los filtros
    anti-falso-positivo (`_is_blocked_domain`, `_is_panama_related`) que sí tiene `fetch_rss()`
    desde el fix del 2026-06-22. Resultado: cualquier resultado que matcheara SOLO el término
    suelto "MIDA" o "cosecha" (sin mención de Panamá) se aceptaba y se etiquetaba con
    source="prensa.com" aunque viniera de sltrib.com, nyfb.org o spa.gov.sa.
    FIX aplicado: se agregó verificación de dominio real contra `site` configurado, más los
    mismos filtros `_is_blocked_domain()` / `_is_panama_related()` usados en `fetch_rss()`.
  NOTA: Esta misma causa raíz y el mismo fix ya fueron identificados y aplicados de forma
    independiente en ~30+ PRs abiertos anteriores (ramas claude/modest-galileo-*,
    claude/loving-lovelace-*, PRs #13–#73) que nunca se fusionaron a main — por eso el bug
    seguía presente. Se recomienda al usuario fusionar uno de estos PRs (o este) y cerrar los
    duplicados para romper el ciclo de re-descubrimiento.
  Bug adicional corregido: `scripts/ingest.py::mark_ingested()` fallaba con
    AttributeError al iterar sobre `processed.items()` sin excluir la clave interna
    `_gdelt_windows` (una lista, no dict). Corregido para usar `article_entries()`.

DIAGNÓSTICO AVANZADO — fetch automático (GitHub Actions):
  - El workflow `wiki_daily.yml` SÍ corrió exitosamente los días 2026-07-04, 07-05 y 07-06
    (conclusion=success), pero 07-05 y 07-06 no generaron ningún commit ("Sin artículos nuevos").
  - Logs del run 2026-07-06 (job 85394933293) muestran la causa: TODAS las consultas a
    `api.gdeltproject.org` fallaron por timeout de conexión o bloqueo 403/429 desde la IP de
    GitHub Actions ese día. Esto incluye reintentos de las ventanas GDELT 2015-2017 que
    NUNCA se han completado (no están en `_gdelt_windows`) y la ventana de cola actual
    (2026-06-18 → hoy).
  - Ventanas GDELT completadas: 45. Esto es MENOS de las ~54 necesarias para cobertura completa
    2015→hoy (faltan las 9 ventanas trimestrales de 2015-01-01 a 2017-03-29, nunca completadas
    por timeouts persistentes). Diagnóstico: GDELT bloqueado/timeout intermitente, NO rango
    agotado — el backfill histórico 2015-2017 sigue pendiente.
  - Problema de diseño adicional en `fetch_gdelt_historical()`: la ventana de "cola" (desde el
    último trimestre completo hasta "ayer") se recalcula con una fecha de fin distinta cada día,
    por lo que nunca coincide con una ventana ya completada y se re-descarga por completo cada
    día (se ven 3 entradas casi idénticas: 20260618_20260701/02/03). No se corrigió esta sesión
    (fuera de alcance inmediato) pero se documenta para una futura sesión.
  - Fuentes RSS (IICA, La Prensa) no se pudieron verificar en los logs de esta sesión;
    revisar en la próxima corrida si siguen activas.
