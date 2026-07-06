---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-06
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

## 2026-07-06 16:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-06 16:20
FALSOS POSITIVOS: 6/6 artículos pendientes revisados y descartados — 0 ingestados al wiki
  Ninguno trata sobre agro panameño. Causa raíz: colisión de la sigla "MIDA" —
  el fetch (GDELT/RSS) captura noticias que mencionan "MIDA" sin verificar que se trate
  del Ministerio de Desarrollo Agropecuario de Panamá.
  Artículos descartados (marcados ingested=true para vaciar la cola, NO agregados al wiki):
    - sltrib.com "Kevin O'Leary data center timeline" → MIDA = Military Installation
      Development Authority (Utah, EE.UU.), no el MIDA panameño
    - sltrib.com "Box Elder data center opponents" → mismo MIDA de Utah
    - sltrib.com "Utah Gov. Cox... Great Salt Lake" → mismo MIDA de Utah
    - sltrib.com "Utah wants to process uranium" → mismo MIDA de Utah (Military Installation
      Development Authority + Utah National Guard)
    - spa.gov.sa "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" →
      agricultura real pero de Arabia Saudita, no de Panamá
    - nyfb.org "New York Farm Bureau" → organización agrícola real pero del estado de
      Nueva York, EE.UU., no de Panamá
  Tasa de falsos positivos de la sesión: 6/6 = 100% de lo pendiente (0 artículos nuevos
  válidos para ingestar). Cumple regla de 0% falsos positivos en el wiki: no se creó
  ninguna página nueva a partir de estos artículos.
  Recomendación: si el fetch usa GDELT con keyword "MIDA", agregar filtro de contexto
  (Panamá, agropecuario) para reducir esta colisión de sigla a futuro.

BUGFIX: scripts/ingest.py `mark_ingested()` fallaba con AttributeError al iterar
  processed.json sin filtrar la clave interna `_gdelt_windows` (una lista, no dict).
  Corregido para usar `article_entries()` como ya hacía `mark_all_ingested()`.

DIAGNÓSTICO DE CAUSA RAÍZ (fetch): confirmado el origen de los 6 falsos positivos.
  `fetch_ddg_search()` en scripts/fetch_news.py es la única de las 3 rutas de fetch
  (RSS, GDELT, DDG search) que NO aplicaba los filtros `_is_blocked_domain()` /
  `_is_panama_related()` ya existentes en el archivo (sí se usan en `fetch_rss` y
  `fetch_gdelt_historical`). `ddgs.news()` no respeta de forma confiable el operador
  `site:`, así que la búsqueda "site:prensa.com ..." devolvió noticias de sltrib.com
  (Utah) y spa.gov.sa (Arabia Saudita) que solo coincidían con el término genérico
  "MIDA" o "agricultura", y el código las etiquetaba ciegamente como
  source="prensa.com", country="PA".
  BUGFIX aplicado: se agregaron los mismos dos filtros a `fetch_ddg_search()`,
  igualando el comportamiento a los otros dos fetchers. Esto debería llevar la tasa
  de falsos positivos de esa ruta a 0% en las próximas corridas de GitHub Actions.
  Nota: Los artículos con `saved_at` 2026-06-26 a 2026-07-02 (los 6 descartados hoy)
  fueron los únicos "nuevos" desde el 2026-05-24 (datos semilla) — es decir, la
  ingesta real al wiki lleva ~6 semanas sin artículos nuevos válidos porque la ruta
  DDG search contaminaba el 100% de lo que llegaba. Con el fix, la próxima corrida
  de Actions debería o bien traer contenido real de La Prensa, o bien 0 resultados
  (si `ddgs.news()` realmente no tiene cobertura de prensa.com), lo cual sería una
  señal sana en vez de falsos positivos.
