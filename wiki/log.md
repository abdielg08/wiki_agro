---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-11
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

## 2026-07-11 00:00
ROUTINE: 7 artículos pendientes revisados — **7/7 falsos positivos, 0 ingestados**
  Falsos positivos detectados (marcados como procesados, NO agregados al wiki):
    - sltrib.com/.../kevin-oleary-data-center-timeline (Utah, EE.UU. — "MIDA" = Military
      Installation Development Authority de Utah, no el MIDA panameño)
    - sltrib.com/.../box-elder-data-center-opponents (Utah, EE.UU. — mismo caso de MIDA)
    - sltrib.com/.../utah-governor-issues-order-protect (Utah, EE.UU. — mismo caso de MIDA)
    - sltrib.com/.../utah-nuclear-energy-state (Utah, EE.UU. — mismo caso de MIDA)
    - spa.gov.sa/en/N2096157 "Reef Saudi" (agricultura de secano en Arabia Saudita, no Panamá)
    - whc.unesco.org/en/list/1506 "The Persian Qanat" (sistema de riego histórico de Irán)
    - nyfb.org "New York Farm Bureau" (gremio agrícola de Nueva York, EE.UU.)
  Causa raíz identificada: `fetch_ddg_search()` en `scripts/fetch_news.py` nunca aplicaba
  los filtros `_is_blocked_domain()` / `_is_panama_related()` que sí protegen a `fetch_rss()`
  y `fetch_gdelt_batch()` (agregados en el fix del 2026-06-22, PR #20). La búsqueda DDG solo
  validaba `is_agro_relevant()` (términos sectoriales como "MIDA", "riego", "agricultura"),
  que hacen falso match con entidades homónimas fuera de Panamá (MIDA de Utah) o con
  agricultura de otros países.
  Fix aplicado: se agregaron ambos filtros a `fetch_ddg_search()` en scripts/fetch_news.py,
  igual que en fetch_rss()/fetch_gdelt_batch(). Commit en esta sesión.
  Resultado: Pendientes de ingesta = 0. Artículos reales en wiki sin cambios (20 descargados,
  20 procesados, 0 nuevas páginas — todo el backlog pendiente era ruido).
  Bug adicional corregido: `mark_ingested()` en scripts/ingest.py lanzaba AttributeError al
  iterar sobre `processed.json` porque no excluía la clave interna `_gdelt_windows` (una
  lista, no un dict de artículo). Ahora usa `article_entries()` como `mark_all_ingested()`.
  Diagnóstico de backfill: 48 ventanas GDELT completadas (≥45 estimadas) → el rango de
  fechas configurado está agotado; considerar expandir cobertura o fuentes adicionales.
  Última descarga de artículos nuevos: 2026-07-10 (1 artículo) — 1 día sin nuevos, dentro
  del umbral de 3 días.
