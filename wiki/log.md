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

## 2026-07-17 00:00
FALSOS_POSITIVOS: 5 artículos de `pending_ingest.md` rechazados — 0% ingestados al wiki
  Causa raíz: colisión de acrónimo "MIDA". El fetch (GDELT/RSS) está indexando
  noticias sobre "MIDA" = Military Installation Development Authority (Utah, EE.UU.)
  y "MITI/MARii" (Malasia), NO el Ministerio de Desarrollo Agropecuario de Panamá.
  Verificado: ninguno de los 5 textos menciona "Panamá"/"Panama".
  Artículos rechazados (marcados ingested=true, false_positive=true en processed.json
  para sacarlos de la cola sin crear contenido de wiki falso):
    - 20260708_prensacom_...miti-working-on-simplified-ncm... (MITI/MARii Malasia)
    - 20260527_prensacom_...box-elder-data-center-opponents (MIDA=Utah data center authority)
    - 20260529_prensacom_...utah-governor-issues-order-prote (MIDA=Utah data center authority)
    - 20260519_prensacom_...kevin-oleary-data-center-timeline (MIDA=Utah data center authority)
    - 20250613_prensacom_...utah-nuclear-energy-state (MIDA=Utah data center authority)
  Acumulado histórico de falsos positivos: 7 (previos, ver metrics.md) + 5 (hoy) = 12
  RECOMENDACIÓN: el filtro de relevancia en `scripts/prioritize.py` / fetch debe
  excluir o penalizar fuertemente artículos con dominio `sltrib.com`/Utah y verificar
  que "MIDA" aparezca junto a contexto panameño antes de asignarles score alto.
  NOTA TÉCNICA: comando `wiki_agro.py mark-ingested <url>` está roto — falla con
  AttributeError al iterar claves internas de processed.json (p.ej. `_gdelt_windows`,
  que es una lista) porque no usa `article_entries()` para filtrar. Se marcaron los
  5 artículos directamente vía script Python usando `article_entries()`. Pendiente
  de fix en `scripts/ingest.py::mark_ingested()`.
  NOTA TÉCNICA 2: `wiki_agro.py mark-all-ingested --limit N` también es riesgoso —
  usa `find_pending()` (orden alfabético por nombre de archivo) mientras que
  `wiki_agro.py ingest --limit N` usa `prioritize()` (orden por score). Los primeros
  N alfabéticos NO son los mismos N que Claude Code revisó. Se evitó ese comando
  y se marcaron URLs específicas directamente para no ingestar el artículo
  equivocado. Pendiente de fix: unificar el orden de selección entre ambas funciones.

## 2026-07-17 00:05
FALSOS_POSITIVOS: 4 artículos adicionales rechazados — 0% ingestados al wiki
  Cola completa revisada (9/9 pendientes de esta sesión = falsos positivos).
  Ninguno de los 4 menciona Panamá; son contenido genérico de agricultura mundial:
    - 20260707_prensacom_en-list-1506 → "The Persian Qanat" (UNESCO, sistema de riego de Irán)
    - 20260617_prensacom_ → "New York Farm Bureau" (EE.UU., gremio agrícola de NY)
    - 20260624_prensacom_en-n2096157 → "Reef Saudi" (programa agrícola de secano, Arabia Saudita)
    - 20250331_prensacom_document-10945742 → paper IEEE sobre IoT/6G y agricultura de precisión (sin país específico)
  Marcados ingested=true, false_positive=true en processed.json para vaciar la cola.
  RESULTADO DE SESIÓN: Pendientes de ingesta = 0. Artículos reales ingestados al wiki = 0.
  Falsos positivos totales acumulados: 7 (previos) + 9 (hoy) = 16.
  DIAGNÓSTICO CRÍTICO: el pipeline de fetch/scoring (`scripts/prioritize.py` y/o
  la fuente `prensa.com`) está trayendo y puntuando alto artículos de agricultura
  genérica mundial sin filtro geográfico de Panamá. Esto viola la meta de 0% falsos
  positivos y bloquea el avance medible del backfill. Se recomienda revisar el
  scoring/keyword-matching antes de la próxima corrida de fetch — ver detalle en
  wiki/metrics.md.
