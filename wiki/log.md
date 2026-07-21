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

## 2026-07-21 00:03
INGEST: 5 artículos revisados, 0 ingestados — 5 falsos positivos (0% tolerancia respetada)
  Causa raíz: colisión de la palabra clave "MIDA" — el fetch (RSS/GDELT) etiquetó estos
  artículos como `country: PA` pero ninguno menciona a Panamá (0 menciones verificadas
  en full_text/summary_raw/title de cada uno). "MIDA" en estos artículos se refiere a:
    - MITI/MIDA de Malasia (Ministry of Investment, Trade and Industry / agencia de
      desarrollo industrial malaya)
    - MIDA = Military Installation Development Authority de Utah, EE.UU. (autoridad de
      desarrollo de centros de datos militares, nada agropecuario)
  Artículos descartados (NO ingestados, sin páginas de wiki creadas):
    - 20260708_prensacom_...miti-working-on-simplified-ncm... (MITI/MIDA Malasia)
    - 20260529_prensacom_...utah-governor-issues-order-prote... (MIDA Utah, calidad del aire)
    - 20260519_prensacom_...kevin-oleary-data-center-timeline... (MIDA Utah, data center)
    - 20260527_prensacom_...box-elder-data-center-opponents... (MIDA Utah, data center)
    - 20260307_prensacom_...cultural-rules-for-staying-with-locals-abro... (MIDA Utah, viajes)
  Acción: marcados como `ingested: true` vía `mark-all-ingested` para sacarlos de la cola
  de pendientes (ya fueron revisados y descartados), sin generar contenido en wiki/.
  Recomendación: el fetcher de RSS/GDELT debería filtrar por relevancia geográfica real
  (mención explícita de Panamá) además del match de keyword "MIDA", para reducir el ruido
  de esta fuente de falsos positivos en sesiones futuras.

## 2026-07-21 00:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
  (bug detectado y corregido en el mismo momento: `mark-all-ingested` usaba un orden
  distinto al de `ingest`, ver siguiente entrada)

## 2026-07-21 00:20
BUGFIX: dos bugs corregidos en scripts/ingest.py durante esta sesión de rutina
  1. `mark_all_ingested` reordenaba los pendientes de forma alfabética (find_pending),
     distinta al orden priorizado (prioritize()) que usa `ingest` para generar
     pending_ingest.md — esto causó que se marcaran como ingestados 3 artículos NUNCA
     revisados (utah-nuclear-energy-state, IEEE document/10945742, archive.org
     Cataloguedipter2SaoP) mientras 3 de los 5 artículos SÍ revisados y documentados
     como falsos positivos quedaban sin marcar y reaparecían en el siguiente batch.
     Fix: `ingest` ahora persiste el batch exacto mostrado en
     `sources/.last_ingest_batch.json`, y `mark_all_ingested` lo consume en vez de
     re-derivar su propio orden.
  2. `mark_ingested` iteraba sobre `processed.items()` sin filtrar la clave interna
     `_gdelt_windows` (una lista, no un dict), causando `AttributeError` y que NINGÚN
     artículo se marcara individualmente. Fix: usa `article_entries()` (ya existente
     en core.py) para filtrar claves internas.
  Verificación post-fix: los 3 artículos marcados por error sin revisión
  (utah-nuclear-energy-state, IEEE 10945742, diptera catalog) fueron revisados
  retroactivamente — los 3 son también falsos positivos genuinos (0 menciones de
  Panamá), así que no se generó contenido incorrecto en el wiki, pero el proceso de
  revisión no se siguió correctamente para ellos hasta este punto.
  - 20250613_prensacom_...utah-nuclear-energy-state (MIDA = Utah Military Installation
    Development Authority, sin relación agropecuaria)
  - 20250331_prensacom_document-10945742 (paper IEEE "Ambient IoT: Communications
    Enabling Precision Agriculture", genérico/global, sin mención de Panamá)
  - 20160513_prensacom_details-cataloguedipter2saop (catálogo de dípteros,
    Secretaria da Agricultura de Brasil, sin relación con Panamá)
  Los 3 artículos correctamente documentados en la entrada anterior pero no marcados
  por el bug (paultan MITI/Malasia, utah-governor-issues-order-protect,
  box-elder-data-center-opponents) fueron marcados como ingestados manualmente tras
  el fix.

## 2026-07-21 00:25
INGEST: 3 artículos revisados, 0 ingestados — 3 falsos positivos adicionales (último
  batch de la cola de pendientes de esta sesión, 0% tolerancia respetada)
  Causa raíz: colisión de la palabra clave genérica "agriculture" (sin contexto
  panameño) en el fetch RSS/GDELT. Ninguno menciona a Panamá (0 menciones verificadas).
    - 20260707_prensacom_en-list-1506 → "The Persian Qanat" (UNESCO, sistema de riego
      ancestral de Irán)
    - 20260617_prensacom_ → "New York Farm Bureau" (gremio agrícola de Nueva York, EE.UU.)
    - 20260624_prensacom_en-n2096157 → "Reef Saudi" (programa de agricultura de secano
      de Arabia Saudita)
  Acción: marcados como `ingested: true`, sin generar contenido en wiki/.
  Con esto, Pendientes de ingesta = 0 (24 descargados, 24 revisados; 13 ingestados con
  contenido real en el wiki, 11 descartados como falsos positivos en esta sesión).

## 2026-07-21 00:30
BUGFIX: causa raíz de los 11 falsos positivos identificada y corregida en
  scripts/fetch_news.py (`fetch_ddg_search`)
  Diagnóstico: `is_agro_relevant()` acepta contenido si CUALQUIER término suelto de
  `config/sources.yaml:search_terms` aparece (ej. "MIDA", "agricultura", "cosecha"),
  sin exigir mención de Panamá. El fetcher DDG (búsqueda web con `site:prensa.com`)
  no aplica ninguna restricción geográfica adicional — y el filtro `site:` de DDG no
  se está respetando de forma confiable, devolviendo resultados de dominios no
  panameños (paultan.org, sltrib.com, whc.unesco.org, nyfb.org, spa.gov.sa,
  archive.org, ieeexplore.ieee.org). Los otros fetchers (RSS de fuentes panameñas,
  CDX restringido a dominio prensa.com, GDELT con `sourcecountry:PA`) sí están
  geográficamente acotados y no sufren este problema.
  Fix: nueva función `has_panama_context()` que exige mención explícita de
  "panama"/"panamá" en título+cuerpo, aplicada como filtro adicional SOLO en
  `fetch_ddg_search` (no en RSS/CDX/GDELT, que ya están acotados por fuente/dominio
  y podrían tener títulos cortos sin la palabra "Panamá" explícita).
  Verificación: los 11 artículos falsos positivos de esta sesión, re-evaluados con
  el fix, son rechazados 11/11 por `has_panama_context()`.
  Impacto esperado: el próximo fetch de GitHub Actions debería dejar de traer este
  tipo de ruido, liberando el cupo de 5 artículos/routine para contenido real.

## 2026-07-21 00:40
DIAGNÓSTICO (Paso 5): backfill GDELT auditado contra `sources/processed.json`
  Positivo: el fetch SÍ está corriendo — último commit con artículos nuevos fue ayer
  (2026-07-20, 2 artículos). 0 días sin artículos nuevos hoy. No se activa la alarma
  de "3 días consecutivos sin nuevos".
  Ventanas GDELT: 51 completadas — más de las ~45 estimadas en CLAUDE.md, PERO ese
  umbral era solo una estimación de referencia, no evidencia real de que el rango de
  fechas esté agotado. Al desglosar `_gdelt_windows` por año se encontraron dos
  anomalías reales (detalle completo en wiki/metrics.md → "Progreso del Backfill
  GDELT"):
    1. 2015 y 2016 — el arranque explícito de la cobertura objetivo — tienen 0
       ventanas completadas. Hueco real en el backfill, pendiente de investigar
       (posible error de red repetido en esas ventanas, o un `date_range.start`
       distinto en corridas anteriores al reset del 2026-06-22).
    2. Las ventanas de 2026 están fragmentadas en 15 entradas casi idénticas
       (mismo inicio, fin creciente día a día) en vez de trimestres limpios —
       ineficiente pero no bloqueante.
  Ninguna de las dos requiere acción inmediata de esta sesión; quedan documentadas
  para que la próxima routine (o una sesión interactiva) las investigue.
