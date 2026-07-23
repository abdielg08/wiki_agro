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

## 2026-07-23 00:00
ROUTINE: `python wiki_agro.py stats` mostró 11 pendientes. Los 11 son 100% FALSOS
POSITIVOS — 0 ingestados al wiki (regla de 0% falsos positivos).
  Falsos positivos detectados y marcados (`ingested: true, skipped: true`):
    - paultan.org (Malasia) — MIDA = Malaysian Investment Development Authority
    - sltrib.com ×4 (Utah, EEUU) — MIDA = Military Installation Development Authority
      de Utah (data centers Kevin O'Leary, Box Elder, orden del gobernador Cox, uranio)
    - msn.com — artículo de etiqueta cultural para viajeros (mención tangencial a MIDA-Utah)
    - spa.gov.sa (Arabia Saudita) — programa "Reef Saudi" de agricultura de secano
    - nyfb.org (EEUU) — New York Farm Bureau
    - whc.unesco.org (Irán) — sistema de qanats persas
    - ieeexplore.ieee.org — paper técnico genérico de IoT/6G para agricultura de precisión
    - archive.org — catálogo entomológico de dípteros de América (1966/1967)
  Ninguno menciona Panamá ni el sector agropecuario panameño. Pendientes tras
  la limpieza: 0.

DIAGNÓSTICO (Paso 5 — pendientes llegó a 0 tras la limpieza):
  - GitHub Actions (wiki_daily.yml) SÍ está corriendo diariamente y en success
    (runs 07-13 a 07-22 verificados vía API, salvo 1 failure el 07-13). No es
    un problema de cron ni de permisos.
  - Causa raíz real: de los 24 artículos descargados en total, solo 6 son
    reales (la carga semilla del 2026-05-24). Los 18 restantes — el 100% de
    todo lo descargado por el fetch automático desde entonces — son falsos
    positivos, y TODOS provienen de la fuente `web_searches.prensa_agro` en
    `config/sources.yaml` (búsqueda DDG con `site:prensa.com`). El operador
    `site:` de DDGS no está filtrando resultados: `ddgs.news()` devuelve
    noticias de cualquier dominio (sltrib.com, paultan.org, msn.com,
    archive.org, ieeexplore.org, etc.) que solo coinciden por palabra clave
    ("MIDA", "agriculture"), y el pipeline las guarda etiquetadas como fuente
    "prensa.com" sin validar que la URL real pertenezca al dominio configurado.
  - RSS (IICA, La Prensa) y GDELT no han aportado ningún artículo nuevo desde
    la carga semilla — 0 artículos reales en ~60 días de operación continua.
  - Backfill histórico GDELT: 37 ventanas trimestrales completadas (2017 Q1 →
    presente), faltan ~8 ventanas de 2015-2016. Además hay 15 ventanas
    "diarias" redundantes (todas con inicio fijo 2026-06-18) mezcladas en
    `_gdelt_windows` que no representan avance del backfill histórico real.
  - RECOMENDACIÓN (no aplicada en esta sesión — requiere cambio de código,
    fuera del alcance de la routine de ingesta): en `fetch_news.py`, validar
    que el dominio de la URL devuelta por `ddgs.news()` coincida con el
    `site:` configurado antes de guardar el artículo, o deshabilitar
    temporalmente la fuente `prensa_agro` hasta corregir el filtro.
  Métricas actualizadas en wiki/metrics.md.
