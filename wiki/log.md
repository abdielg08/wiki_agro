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

## 2026-07-15 08:00
ROUTINE: 8 artículos pendientes revisados — 8/8 FALSOS POSITIVOS (0 ingestados al wiki)
  No se creó contenido nuevo en wiki/topics, wiki/entities ni wiki/summaries — ninguno de los
  8 artículos trata sobre el sector agropecuario de Panamá.

  Lote 1 (5 artículos) — colisión del acrónimo "MIDA":
    - paultan.org (Malasia) — MITI/MIDA malasio (Malaysian Investment Development Authority)
    - sltrib.com x3 (Utah, EEUU) — MIDA = Military Installation Development Authority
      (data centers, Kevin O'Leary, Gran Lago Salado, uranio)
    - Todas marcadas: ingested=true, skipped=true, skip_reason documentado en processed.json

  Lote 2 (3 artículos) — agricultura genérica global sin mención de Panamá:
    - whc.unesco.org — "The Persian Qanat" (sistema de riego antiguo, Irán)
    - nyfb.org — New York Farm Bureau (EEUU)
    - spa.gov.sa — Programa "Reef Saudi" de agricultura de secano (Arabia Saudita)
    - Todas marcadas: ingested=true, skipped=true, skip_reason documentado en processed.json

  DIAGNÓSTICO — causa raíz identificada:
  El web_search "prensa_agro" (config/sources.yaml) usa DuckDuckGo (ddgs.news) con un filtro
  `site:prensa.com` que la API NO respeta de forma confiable — devuelve resultados de dominios
  arbitrarios (thestar.com.my, sltrib.com, fox13now.com, worldbank.org, ieeexplore.ieee.org,
  paultan.org, whc.unesco.org, nyfb.org, spa.gov.sa). Además, `is_agro_relevant()` solo exige
  coincidencia de palabras clave genéricas (ej. "MIDA", "agricultura", "cosecha", "riego") SIN
  exigir mención de Panamá, por lo que cualquier artículo agrícola global pasaba el filtro.
  El código también etiquetaba `source` como el `site` configurado ("prensa.com") sin validar
  el dominio real del resultado — por eso 15/21 artículos en sources/ aparecen mal etiquetados
  como "prensa.com" cuando en realidad vienen de sitios no relacionados.

  Impacto acumulado: 15 de 21 artículos descargados hasta hoy (71%) son falsos positivos de
  esta única fuente de búsqueda — 100% de precisión inversa (0% relevantes).

  FIX APLICADO en scripts/fetch_news.py (fetch_ddg_search):
    1. Se valida que el dominio real de la URL devuelta contenga el `site` configurado
       (usando urllib.parse.urlparse) antes de aceptar el resultado.
    2. Se exige que "panam" aparezca en título+cuerpo del artículo (además del chequeo
       genérico is_agro_relevant existente).
  Esto no elimina la fuente "prensa_agro" pero bloquea el patrón exacto de falsos positivos
  observado hasta ahora. Recomendación pendiente de validar en próximas corridas de Actions.

  FIX APLICADO en scripts/ingest.py (mark_ingested):
    Bug: la función iteraba `processed.items()` directamente, incluyendo la clave interna
    `_gdelt_windows` (una lista, no un dict de metadata), causando AttributeError al intentar
    marcar cualquier artículo como ingestado. Corregido para usar `article_entries(processed)`,
    igual que ya hacía `mark_all_ingested`.

  Estado GDELT: 48 ventanas registradas en `_gdelt_windows`, pero la ventana más antigua
  comienza en 2017-03-30 (no 2015-01-01 como exige la cobertura objetivo) — el rango
  2015-01-01 → 2017-03-29 nunca se completó. Además, 11/48 ventanas registradas comparten el
  mismo inicio "20260618" con distintos finales, lo que sugiere que el ciclo de backfill re-
  consulta la ventana final (la más reciente) cada día en vez de avanzar hacia atrás en el
  tiempo para llenar el vacío 2015-2017. Requiere investigación adicional de
  `fetch_gdelt_historical()` en scripts/fetch_news.py — no se modificó en esta sesión por
  quedar fuera del alcance de este diagnóstico rápido.

  Días sin artículos nuevos: 1 (último commit a sources/ fue 2026-07-14; hoy es 2026-07-15).
  Dentro del umbral normal (alerta a partir de 3 días consecutivos).

  Pendientes de ingesta al cierre: 0
