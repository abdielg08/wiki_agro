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

## 2026-07-31 00:00
ROUTINE: Diagnóstico + 16 falsos positivos rechazados + fix de causa raíz

`stats` reportó 16 Pendientes de ingesta. `ingest --limit 5` mostró 5 artículos
en `pending_ingest.md`; ninguno era sobre agro panameño (Malasia MITI/MIDA,
data centers de Utah — MIDA = "Military Installation Development Authority" ahí,
y "Cultural Rules For Staying With Locals Abroad"). Se inspeccionó
`sources/processed.json` directamente y se confirmó que los 16 pendientes
completos eran falsos positivos — 0/16 mencionan Panamá:

  - 3× thestar.com.my / paultan.org — MITI/MIDA de Malasia (agencia de inversión)
  - 4× sltrib.com / fox13now.com — MIDA = Military Installation Development
    Authority de Utah (data centers, no agro)
  - 4× heraldo.es — agricultura de Aragón, España
  - 1× agenciabrasil.ebc.com.br — agricultura familiar de Brasil
  - 1× spa.gov.sa — programa agrícola de Arabia Saudita
  - 1× whc.unesco.org — sistema de qanats de Irán (patrimonio UNESCO)
  - 1× nyfb.org — New York Farm Bureau (EE.UU.)
  - 1× ieeexplore.ieee.org — paper técnico sin relación
  - 1× archive.org — catálogo de zoología de 1966/67 (Brasil)
  - 1× msn.com — artículo de viajes que menciona "MIDA" (Utah) de pasada

NINGUNO fue ingestado al wiki (0% falsos positivos en contenido, intacto).
Los 16 se marcaron `ingested: true` en `processed.json` vía
`mark-ingested` (uno por uno) para limpiarlos de la cola de pendientes,
dejando registro explícito aquí en vez de perderlos en un mensaje genérico.

**Causa raíz identificada**: `fetch_ddg_search()` en `scripts/fetch_news.py`
(fuente `web_searches: prensa_agro`, query `site:prensa.com agropecuario OR
... OR MIDA ...`) solo aplicaba el filtro `is_agro_relevant()` — a diferencia
del fetcher RSS, que además exige `_is_panama_related()` (línea 226) y excluye
dominios bloqueados. Dos problemas compuestos:
  1. El calificador `site:prensa.com` de DDG no se respeta de forma
     confiable en el backend de `ddgs` — llegaron resultados de dominios
     totalmente ajenos (sltrib.com, paultan.org, heraldo.es, etc.) etiquetados
     como fuente "prensa.com".
  2. Sin el filtro de Panamá, cualquier resultado que mencionara "MIDA"
     (acrónimo ambiguo: Malasia, Utah, Panamá) o "agricultura" en general
     pasaba el filtro `is_agro_relevant`.

**Fix aplicado** (`scripts/fetch_news.py`, `fetch_ddg_search`):
  - Se agregó `_is_blocked_domain(url)` (dominios no-Panamá conocidos).
  - Se agregó verificación de que el dominio del resultado coincida con el
    `site` solicitado en la búsqueda (cuando se especifica uno).
  - Se agregó `_is_panama_related()` sobre título/URL/cuerpo, igual que en
    el fetcher RSS.

**Bug adicional encontrado y corregido**: `mark_ingested()` (singular, en
`scripts/ingest.py`) iteraba `processed.items()` sin filtrar la clave interna
`_gdelt_windows` (una lista), causando `AttributeError` inmediato en cada
llamada — el comando `python wiki_agro.py mark-ingested <url>` estaba roto
para cualquier URL. Se corrigió usando el helper `article_entries()`
(igual que ya hacía `mark_all_ingested`).

**Diagnóstico GDELT**: `_gdelt_windows` tiene 59 ventanas completadas (por
encima del estimado de ~45) → el rango histórico 2015→hoy vía GDELT está
efectivamente agotado. El crecimiento de artículos nuevos ahora depende de
RSS (IICA, La Prensa) y de la búsqueda DDG recién corregida.

**Hallazgo de fondo**: desde la carga semilla del 2026-05-24 (6 artículos
reales), NINGÚN artículo nuevo genuinamente sobre agro panameño ha entrado
al wiki pese a >20 corridas diarias de GitHub Actions — las 23 descargas
posteriores a la semilla fueron 100% falsos positivos (7 detectados en el
fix previo `c032e62` del 2026-06-22, 16 detectados en esta sesión). El fetch
automático está funcionando (corre a diario, trae artículos) pero su fuente
principal de volumen (`web_searches: prensa_agro` vía DDG) no traía ninguna
señal real; con el fix de hoy debería empezar a filtrar correctamente.
Pendiente de validar en la próxima corrida de Actions.

Estado tras esta sesión: Pendientes de ingesta = 0. No se creó contenido
nuevo de wiki (no había artículos legítimos que ingestar).

## 2026-07-31 08:07
LINT: 20 páginas revisadas, 55 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:12, no_index:1
