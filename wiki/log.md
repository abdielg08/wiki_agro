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

## 2026-07-03 00:00
INGEST: 6 artículos pendientes revisados — 0 ingestados, 6 falsos positivos (0% tasa de aceptación)
  Falsos positivos detectados (NO son sobre agro panameño):
    - Kevin O'Leary data center timeline (sltrib.com) → "MIDA" = Military Installation
      Development Authority de Utah, no Ministerio de Desarrollo Agropecuario de Panamá
    - Box Elder data center opponents (sltrib.com) → misma colisión MIDA-Utah
    - Utah Gov. Cox order Great Salt Lake (sltrib.com) → misma colisión MIDA-Utah
    - Utah uranium/nuclear energy Wasatch Front (sltrib.com) → misma colisión MIDA-Utah
    - New York Farm Bureau (nyfb.org) → agricultura de EE.UU., no de Panamá
    - "Reef Saudi" rain-fed agriculture program (spa.gov.sa) → agricultura de Arabia Saudita
  Los 6 se marcaron `ingested: true` en processed.json sin crear contenido de wiki
  (ningún summary, topic ni entity creado — cero contaminación del wiki).

BUG RAÍZ IDENTIFICADO Y CORREGIDO en scripts/fetch_news.py:
  `fetch_ddg_search()` (fuente de estos 6 artículos + los 7 falsos positivos ya
  detectados el 2026-06-22) NO aplicaba los filtros `_is_blocked_domain()` ni
  `_is_panama_related()` que sí tienen `fetch_rss()` y `fetch_gdelt_historical()`.
  Resultado: 13/13 artículos traídos por búsqueda DuckDuckGo hasta hoy han sido
  falsos positivos (thestar.com.my Malasia, sltrib.com/fox13now.com Utah,
  spa.gov.sa Arabia Saudita, worldbank.org genérico, ieeexplore.ieee.org, nyfb.org) —
  tasa de falsos positivos de esa fuente: 100%.
  FIX: se agregaron los mismos dos filtros a `fetch_ddg_search()` (scripts/fetch_news.py).
  Recomendación de seguimiento: considerar deshabilitar `web_searches` en
  config/sources.yaml si sigue produciendo 0% de artículos válidos tras el fix.

BUG SECUNDARIO IDENTIFICADO Y CORREGIDO en scripts/ingest.py:
  `mark_ingested()` iteraba `processed.items()` crudo (incluye la clave interna
  `_gdelt_windows`, cuyo valor es una lista) en vez de `article_entries(processed)`,
  causando `AttributeError: 'list' object has no attribute 'get'` en cada llamada.
  FIX: ahora usa `article_entries(processed).items()`, igual que `mark_all_ingested()`.

DIAGNÓSTICO — Estado del fetch automático (GitHub Actions):
  Corrió correctamente 2026-06-26, 27, 28, 29 y 07-02 (commits "chore(sources): N
  artículos nuevos descargados [skip ci]"). Aún no corre hoy 2026-07-03.
  Ventanas GDELT completadas: 43 de 47 esperadas (2015-01-01 → 2026-07-02, ventanas
  de 90 días). Se comparó la lista real de `_gdelt_windows` contra el calendario
  esperado y se encontró que las **9 ventanas de 2015-01-01 a 2017-03-29 nunca se
  han marcado como completadas** — es decir, el backfill NO ha avanzado en el tramo
  más antiguo (2015-2016 + Q1 2017), pese a que 2017-Q2 en adelante sí está 100%
  completo. Esto coincide con el criterio de CLAUDE.md ("< 45 ventanas completadas
  → GDELT bloqueado o timeout"), pero el bloqueo parece concentrado específicamente
  en el rango 2015-2017, no distribuido al azar.
  No se pudo probar la GDELT API directamente desde este sandbox (el proxy de red
  bloquea api.gdeltproject.org con 403 — dominio fuera del allowlist), así que no
  se pudo confirmar si la causa es timeout, rate-limit, o falta real de cobertura
  de GDELT para 2015-2016 (GDELT 2.0 se lanzó oficialmente el 2015-02-19; su
  cobertura multi-idioma antes de ~2017 es conocida por ser más débil).
  RECOMENDACIÓN: revisar el log de la próxima corrida de GitHub Actions específicamente
  para las ventanas `20150101_20150401` en adelante — si siguen devolviendo error de
  red, confirmarían un problema real (no solo falta de datos).
  Nota menor: se detectaron 6 ventanas "extra" con claves como `20260618_2026062X`
  (fragmentos del día final que se re-generan cada corrida porque `end` se recalcula
  como `hoy - 1 día`). No afecta la cobertura, solo genera entradas redundantes en
  `_gdelt_windows`; no se corrigió por ser de bajo impacto.
  Artículos reales netos ingestados desde el inicio: 6 (los de semilla) — el fetch
  automático vía DDG search no ha aportado ningún artículo válido aún (100% falsos
  positivos); el fetch GDELT (con filtro Panama correcto) es la fuente que debe
  cerrar el backfill histórico, pero tiene el hueco 2015-2017 descrito arriba.
  Total páginas wiki: 20 (8 topics, 3 entities, 6 summaries, 3 overview)
  Total falsos positivos acumulados: 13 (7 previos + 6 de esta sesión)
