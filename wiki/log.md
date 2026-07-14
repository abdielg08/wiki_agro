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

## 2026-07-14 00:00
INGEST: 5 artículos revisados — 5/5 FALSOS POSITIVOS, 0 ingestados al wiki
  Ningún artículo se agregó a wiki/summaries/, topics/ ni entities/ — todos rechazados.

  Artículos rechazados:
    1. "MITI working on simplified NCM customised incentive mechanism..."
       URL: paultan.org/2026/07/07/... | Fuente etiquetada: prensa.com | país real: Malasia
       Motivo: menciona "MIDA" pero se refiere a Malaysian Investment Development
       Authority (agencia de Malasia), no al Ministerio de Desarrollo Agropecuario de Panamá.
       Artículo en inglés sobre incentivos industriales/comerciales de Malasia — 0% relación
       con agro panameño.
    2. "Box Elder data center opponents hope for a vote..."
       URL: sltrib.com/news/2026/05/27/box-elder-data-center-opponents | país real: EE.UU. (Utah)
       Motivo: "MIDA" = Military Installation Development Authority de Utah. Artículo sobre
       oposición a un centro de datos de Kevin O'Leary. Sin relación con agro panameño.
    3. "Utah Gov. Cox issues order to protect Great Salt Lake, air quality from data centers"
       URL: sltrib.com/news/environment/2026/05/29/... | país real: EE.UU. (Utah)
       Motivo: mismo caso — "MIDA" = agencia estatal de Utah. Tema: calidad de aire y
       centros de datos. Sin relación con agro panameño.
    4. "Timeline: How the Kevin O'Leary data center plan came to be..."
       URL: sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline | país real: EE.UU. (Utah)
       Motivo: mismo caso — "MIDA" = agencia estatal de Utah (board que aprobó el plan Stratos).
    5. "Utah wants to process uranium on the Wasatch Front for nuclear energy..."
       URL: sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state | país real: EE.UU. (Utah)
       Motivo: "MIDA" = Military Installation Development Authority (Utah). Tema: energía
       nuclear/uranio. Sin relación con agro panameño.

  DIAGNÓSTICO DE CAUSA RAÍZ (bug sistémico, no son casos aislados):
  Los 5 artículos — y de hecho los 8/8 pendientes en cola actualmente (`python wiki_agro.py queue`) —
  vienen de la búsqueda web `web_searches: prensa_agro` en `config/sources.yaml`, que usa
  DuckDuckGo (`ddgs.news()`) con la consulta `site:prensa.com agropecuario OR ... OR MIDA OR ...`.
  Dos problemas combinados:
    a. `ddgs.news()` NO respeta de forma confiable el operador `site:` — devuelve resultados
       de dominios arbitrarios (paultan.org, sltrib.com) en vez de solo prensa.com.
    b. `fetch_ddg_search()` en `scripts/fetch_news.py` etiqueta el `source`, `country="PA"` y
       `language="es"` de forma FIJA según la config de búsqueda, sin verificar que la URL
       real del resultado pertenezca al dominio esperado ni que el idioma/país coincidan.
       Por eso artículos en inglés sobre Utah/Malasia terminan marcados como
       `source: prensa.com`, `country: PA`, `language: es`.
    c. `is_agro_relevant()` (scripts/fetch_news.py:123) solo hace un substring match de
       términos como "MIDA" contra título+cuerpo, sin desambiguar significado ni exigir
       coincidencia de país — cualquier "MIDA" en cualquier idioma/país pasa el filtro.

  Impacto: 8/8 artículos en la cola de ingesta actual son falsos positivos (100%),
  todos originados por esta búsqueda. Viola la métrica "Tasa de falsos positivos: 0%".

  RECOMENDACIÓN (no aplicada en esta sesión — requiere cambio de código, se notifica
  al usuario para autorización):
    - Verificar que el dominio de la URL devuelta por ddgs coincida con `site` antes de aceptar
      el resultado (o descartar si no coincide).
    - Quitar "MIDA" como término aislado de `search_terms.primary` (o exigir co-ocurrencia con
      "Panamá"/"panameñ" para evitar colisión con acrónimos homónimos de otros países).
    - Restaurar/mantener el `country`/`language` reales del resultado en vez de forzar "PA"/"es".

  Quedan 3 artículos más en la cola (`python wiki_agro.py queue`), con el mismo patrón
  (Persian Qanat, New York Farm Bureau, "Reef Saudi") — se espera que también sean
  falsos positivos por la misma causa raíz; se revisarán en la próxima sesión de ingesta.

## 2026-07-14 00:05
MAINTENANCE: Diagnóstico avanzado del fetch automático
  GitHub Actions SÍ corrió hoy (commit 8c765c0, 2026-07-14): 1 artículo nuevo descargado.
  Ese único artículo nuevo de hoy es el falso positivo #1 documentado arriba (MITI/Malasia) —
  es decir, 0 artículos ÚTILES nuevos hoy pese a que el fetch funcionó.
  Ventanas GDELT completadas: 48 (`_gdelt_windows` en sources/processed.json) — por encima
  del umbral de 45 estimadas → el rango de fechas GDELT 2015-hoy está agotado y necesitaría
  expansión/nueva estrategia de backfill si se quiere seguir creciendo por esa vía.
  Fuentes RSS activas (IICA, La Prensa) no aportaron artículos nuevos hoy; el único ingreso
  vino de la búsqueda DDG "prensa_agro", que es la fuente del bug de falsos positivos arriba.

## 2026-07-14 19:33
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
