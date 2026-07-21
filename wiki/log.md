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

## 2026-07-21 08:05
FALSOS POSITIVOS: 11/11 artículos pendientes rechazados — 0 ingestados esta sesión.
  Ningún artículo fue agregado al wiki (regla de 0% falsos positivos).
  Todos etiquetados `source: prensa.com` / `country: PA` pero el contenido real
  no tiene relación con Panamá ni con su sector agropecuario:
    - MITI/MIDA/MARii (paultan.org) → MIDA = Malaysian Investment Development
      Authority, no el MIDA panameño. Artículo sobre Malasia.
    - Utah Gov. Cox / calidad del aire (sltrib.com) → MIDA = Military
      Installation Development Authority (Utah, EE.UU.), no relacionado.
    - Timeline Kevin O'Leary data center (sltrib.com) → mismo MIDA de Utah.
    - Box Elder data center opponents (sltrib.com) → mismo MIDA de Utah.
    - Utah uranium processing / Wasatch Front (sltrib.com) → mismo MIDA de Utah.
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) → artículo de
      viajes, mención tangencial al MIDA de Utah.
    - "The Persian Qanat" (whc.unesco.org) → sistema de riego antiguo de Irán.
    - "New York Farm Bureau" (nyfb.org) → agricultura de Nueva York, EE.UU.
    - "Reef Saudi" (spa.gov.sa) → programa agrícola de Arabia Saudita.
    - "Ambient IoT... Precision Agriculture" (ieeexplore.ieee.org) → paper
      técnico genérico sobre 6G, sin mención de Panamá.
    - Catálogo de dípteros de Sudamérica (archive.org, 1966) → documento de
      zoología brasileña escaneado, sin relación agropecuaria ni con Panamá.
  Todos marcados `ingested: true` en processed.json (revisados y rechazados)
  para despejar la cola sin contaminar el wiki con contenido falso.

DIAGNÓSTICO DE CAUSA RAÍZ: el 100% de los 11 pendientes venían de la búsqueda
DuckDuckGo (`fetch_ddg_search` en scripts/fetch_news.py, config `prensa_agro`
con `site: "prensa.com"` y query que incluye el término ambiguo "MIDA"). A
diferencia de `fetch_rss` y `fetch_gdelt_batch`, esta función NO verificaba
que el dominio real del resultado coincidiera con el `site:` solicitado, NI
aplicaba los filtros `_is_blocked_domain` / `_is_panama_related` ya existentes
en el archivo. El operador `site:` de DDG no se respeta de forma confiable,
así que la búsqueda devolvía resultados de cualquier dominio que mencionara
"MIDA" o "agricultura" en el mundo (Malasia, Utah, Irán, Arabia Saudita, etc.)
y el código los etiquetaba ciegamente como `prensa.com` / `country: PA`.

FIX aplicado en `scripts/fetch_news.py::fetch_ddg_search`:
  1. Verifica que el dominio real de la URL contenga el `site` configurado
     antes de aceptar el resultado (rechaza si DDG ignoró el filtro).
  2. Aplica `_is_blocked_domain()` (dominios de TLDs no-panameños conocidos).
  3. Aplica `_is_panama_related()` (exige término panameño inequívoco en
     título/URL), salvo para dominios `.gob.pa` (gobierno panameño directo).
  4. Usa el dominio real verificado como `source`, no el nombre configurado.
  Nota: había además 7 artículos de sesiones anteriores marcados
  `ingested: true` sin `ingested_at` y sin entrada en este log (thestar.com.my,
  fox13now.com, worldbank.org/ext genérico, ieeexplore.ieee.org) — verificado
  que ninguno tiene contenido en wiki/, es decir no contaminaron páginas
  existentes, pero el rechazo no quedó documentado en su momento.
  Fuentes con cobertura: MIDA (2), TVNNoticias (1), LaPrensaEco (1), BDA (1), IICA (1)
