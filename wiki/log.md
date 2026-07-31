---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-31
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
ROUTINE: Sesión automática — diagnóstico y batch de ingesta
  Pendientes al inicio: 16
  Batch de 5 artículos evaluado — **5/5 falsos positivos, 0 ingestados**
  Causa raíz: colisión de palabra clave "MIDA" — el fetch de prensa.com trajo
  artículos en inglés donde "MIDA" no es el Ministerio de Desarrollo
  Agropecuario de Panamá, sino otras siglas homónimas:
    - "MIDA" = Malaysian Investment Development Authority (MITI, Malasia)
      → 20260708_prensacom_...miti-working-on-simplified-ncm...json
    - "MIDA" = Military Installation Development Authority (Utah, EE.UU.)
      → 20260519_prensacom_...kevin-oleary-data-center-timeline.json
      → 20260527_prensacom_...box-elder-data-center-opponents.json
      → 20260529_prensacom_...utah-governor-issues-order-prote.json
      → 20260307_prensacom_...cultural-rules-for-staying-with-locals-abro.json
  Ninguno de los 5 menciona Panamá ni temas agropecuarios (0 menciones
  verificadas programáticamente). NO se creó contenido de wiki para estos
  artículos, conforme a la regla de 0% falsos positivos.
  Acción: marcados como `ingested: true` en processed.json (mark-all-ingested)
  para sacarlos de la cola de pendientes sin generar páginas de wiki — quedan
  documentados aquí como descartados, no como procesados.
  RECOMENDACIÓN: el filtro de fetch para prensa.com/GDELT debería excluir o
  penalizar artículos en inglés / fuera de dominios de Panamá que solo
  matchean por la sigla "MIDA" sin contexto agropecuario panameño, para
  reducir el desperdicio de la cuota de ingesta diaria.

## 2026-07-31 00:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-31 00:10
ROUTINE: Verificación de los 11 pendientes restantes — **11/11 falsos positivos, 0 ingestados**
  Se verificó texto completo (no solo título) de cada artículo pendiente contra
  "panamá"/"panama": 0 menciones en los 11 casos.
    - AEGA pide elecciones al campo en Aragón (heraldo.es, España)
    - New York Farm Bureau (nyfb.org, EE.UU.)
    - Arvensis Agro amplía instalaciones (heraldo.es, España)
    - 'Reef Saudi', rain-fed agriculture program (spa.gov.sa, Arabia Saudita)
    - Finep paga R$220M innovación agricultura familiar (agenciabrasil.ebc.com.br, Brasil)
    - The Persian Qanat (whc.unesco.org, Irán)
    - Luis Biendicho asume consejería Medio Ambiente Aragón (heraldo.es, España)
    - MITI/MIDA Malasia — NCM incentive mechanism (paultan.org, Malasia)
    - Kevin O'Leary data center timeline (sltrib.com, Utah EE.UU.)
    - Box Elder data center opponents (sltrib.com, Utah EE.UU.)
    - Utah Gov. Cox order re: data centers (sltrib.com, Utah EE.UU.)
  Total del backlog descargado hasta hoy: 29 artículos, de los cuales 23
  provienen de la fuente etiquetada "prensa.com" — y los 23 son contaminación
  (0/23 mencionan Panamá). Solo los 6 artículos semilla (MIDA, IDIAP-relacionados,
  BDA, IICA, TVNNoticias, LaPrensaEco) son legítimos.

  DIAGNÓSTICO DE CAUSA RAÍZ (código, no solo datos):
  `scripts/fetch_news.py::fetch_ddg_search()` (usado por la fuente configurada
  `web_searches.prensa_agro` en `config/sources.yaml`, query
  `site:prensa.com agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá`)
  NO aplicaba los filtros `_is_blocked_domain()` / `_is_panama_related()` que sí
  usa `fetch_rss()`. Como el operador `site:` de DuckDuckGo no se respeta de forma
  confiable, la búsqueda devolvió resultados de dominios completamente ajenos
  (sltrib.com, heraldo.es, paultan.org, spa.gov.sa, agenciabrasil.ebc.com.br,
  whc.unesco.org, nyfb.org) que solo coincidían por la palabra "MIDA" o
  "agricultura" sin relación con Panamá. Además, el código etiquetaba
  incorrectamente el `source` de todos estos artículos como `"prensa.com"`
  (usaba `site or name` en vez de `name`), ocultando que en realidad venían de
  dominios no verificados.

  FIX APLICADO: `scripts/fetch_news.py::fetch_ddg_search()` ahora:
    1. Verifica que el dominio del resultado realmente contenga `site` antes
       de aceptarlo (no confía en el operador `site:` de DDG)
    2. Aplica `_is_blocked_domain()` (rechaza TLDs no-Panamá conocidos)
    3. Aplica `_is_panama_related()` sobre título/URL/resumen (exige al menos
       un término panameño explícito, igual que `fetch_rss()`)
    4. Usa `name` (nombre de la búsqueda configurada) en vez de `site` para
       el campo `source`, para que la fuente real quede trazable
  Esto no modifica `sources/` (inmutable) — solo el pipeline de fetch para
  futuras descargas. El backlog contaminado ya descargado permanece en
  `sources/articles/` como registro histórico, pero fue evaluado, documentado
  y descartado (no ingerido).

  Acción: los 11 restantes también se marcan `ingested: true` (mark-all-ingested)
  para vaciar la cola de pendientes — quedan documentados aquí como
  descartados por falso positivo, no como contenido procesado en el wiki.
  Pendientes tras esta sesión: 0. Artículos wiki nuevos esta sesión: 0
  (0% falsos positivos ingeridos — regla innegociable respetada).

## 2026-07-31 00:05
INGEST: 11 artículos marcados como ingestados por sesión Claude Code
