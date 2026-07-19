---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-19
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

## 2026-07-19 16:05
INGEST: 0 artículos reales ingestados | 9 falsos positivos detectados y rechazados
  Se revisaron los 9 artículos pendientes (2 tandas de `ingest --limit 5`). NINGUNO
  trataba sobre agro panameño — se marcaron `ingested: true, skipped: true` con
  `skip_reason` documentado en `sources/processed.json`, sin crear contenido de wiki.
  Falsos positivos (tanda 1/2):
    - paultan.org (MITI/MIDA Malasia — incentivos industriales)
    - sltrib.com ×4 (MIDA = Military Installation Development Authority, Utah EEUU —
      data centers de Kevin O'Leary, calidad del aire/agua, procesamiento de uranio)
  Falsos positivos (tanda 2/2):
    - whc.unesco.org (sitio patrimonio qanat de Irán)
    - nyfb.org (New York Farm Bureau, EEUU)
    - spa.gov.sa (programa "Reef Saudi" de agricultura de secano, Arabia Saudita)
    - ieeexplore.ieee.org (paper académico IoT/6G y agricultura de precisión, genérico)

DIAGNÓSTICO CRÍTICO — causa raíz de los 16 falsos positivos consecutivos desde 2026-05-30:
  Los 22 artículos en `sources/` incluyen 6 reales (semilla manual 2026-05-24) y 16
  falsos positivos consecutivos ingresados por `fetch_ddg_search()` (búsqueda DuckDuckGo
  `prensa_agro`, `config/sources.yaml`). Esa función NO aplicaba `_is_blocked_domain()`
  ni `_is_panama_related()` — filtros que sí usan `fetch_rss()` y `fetch_gdelt_batch()`
  en el mismo archivo. Solo exigía que el título/cuerpo contuviera un término genérico
  de `search_terms` (p.ej. "MIDA", "agricultura"), sin exigir mención de Panamá. Además,
  el operador `site:prensa.com` de DDG no se respeta de forma confiable — `ddgs.news()`
  devolvía resultados internacionales sin relación con prensa.com, y el código los
  etiquetaba igual como `source: "prensa.com", country: "PA"`.
  FIX APLICADO: `scripts/fetch_news.py::fetch_ddg_search()` ahora aplica los mismos
  filtros `_is_blocked_domain(url)` y `_is_panama_related(title, url)` que ya usan
  `fetch_rss()` y `fetch_gdelt_batch()`, antes de aceptar un resultado de DDG.
  Impacto esperado: el fetch diario/histórico debería dejar de traer ruido internacional
  vía la búsqueda `prensa_agro`, liberando la cuota de ~15 artículos/día para contenido
  real de Panamá. A validar en la próxima corrida de GitHub Actions.
  Tasa de falsos positivos ingresados al wiki en esta sesión: 0% (cumple la meta).

HALLAZGO SECUNDARIO — backfill GDELT estancado en la ventana final (no bloqueante, no corregido):
  `_gdelt_windows` en `processed.json` tiene 51 entradas, pero las últimas 5 son
  "20260618_20260708", "20260618_20260709", "20260618_20260714", "20260618_20260717",
  "20260618_20260718" — mismo inicio, fin creciente. Causa: en
  `fetch_gdelt_historical()` (scripts/fetch_news.py), cuando el cursor `current` está a
  menos de 90 días de `end` (= ayer), la ventana final se calcula como
  `next_q = min(current + 90d, end)`. Como `end` cambia cada día que corre el workflow,
  esa ventana de cola nunca coincide con una ya completada (la clave incluye la fecha
  fin), así que se vuelve a consultar —y a marcar como "completada"— cada vez con un
  rango ligeramente más ancho, sin que `current` avance nunca más allá de 2026-06-18.
  Efecto: el backfill quedó permanentemente estancado ahí en vez de seguir avanzando en
  incrementos fijos de 90 días; genera entradas duplicadas/redundantes en
  `_gdelt_windows` y llamadas GDELT repetidas para rangos solapados.
  NO se corrigió en esta sesión (requiere rediseñar cómo se persiste el cursor de la
  ventana final, p.ej. guardando un `_gdelt_cursor` explícito en vez de inferirlo de las
  claves de ventana) — queda documentado para una próxima sesión.
