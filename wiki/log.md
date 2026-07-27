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

## 2026-07-27 16:03
INGEST (routine): 5 artículos revisados de pending_ingest.md → 0 ingestados, 5 falsos positivos
  Falsos positivos (NO ingestados, marcados como procesados vía mark-all-ingested):
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org) →
      MIDA = Malaysian Investment Development Authority (Malasia), no MIDA panameño
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com) →
      MIDA = Military Installation Development Authority (Utah, EE.UU.)
    - "Box Elder data center opponents hope for a vote..." (sltrib.com) → mismo MIDA de Utah
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) → mismo MIDA de Utah
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) → mención tangencial al MIDA de Utah
  Ninguno trata sobre agro de Panamá. Tasa de falsos positivos de esta sesión: 5/5 (100%).

CAUSA RAÍZ IDENTIFICADA: `scripts/fetch_news.py::fetch_ddg_search()` construía la query DDG
como `site:prensa.com agropecuario OR agricultura OR ... OR MIDA OR ...`, pero DuckDuckGo News
no respeta de forma confiable el operador `site:`. Resultado: llegaban artículos de dominios
completamente ajenos (sltrib.com, paultan.org, msn.com, thestar.com.my, fox13now.com,
ieeexplore.ieee.org, spa.gov.sa, nyfb.org, archive.org, whc.unesco.org, worldbank.org genérico)
etiquetados con `source: prensa.com`, simplemente porque contenían alguna palabra suelta como
"MIDA" o "agricultura" (`is_agro_relevant()` no exige relación con Panamá). Revisando
`sources/processed.json`, la inmensa mayoría de los artículos ingeridos desde finales de mayo
son de este tipo — solo los 6 artículos semilla del 2026-05-24 son contenido real de Panamá.

FIX APLICADO: se agregó verificación de dominio en `fetch_ddg_search()` — el resultado debe
provenir realmente del dominio configurado en `site:` (usando `_url_domain()` +
`_is_blocked_domain()`, igual que ya hacía `fetch_rss()`). Esto habría bloqueado los 5 falsos
positivos de esta sesión y la mayoría de los ~18 previamente marcados como "prensa.com".

DIAGNÓSTICO ADICIONAL:
  - Sin artículos nuevos en sources/ desde 2026-07-20 (commits de Actions del 07-21 al 07-26
    reportan "0 artículos nuevos") → 6 días consecutivos sin ingesta nueva, supera el umbral
    de 3 días de `CLAUDE.md`. GitHub Actions sí está corriendo diariamente (commits [skip ci]
    presentes cada día), el problema es de calidad/filtrado de fuentes, no de que el workflow
    esté caído.
  - Ventanas GDELT completadas: 56 (supera el estimado de 45-46) → por regla de CLAUDE.md,
    el rango de fechas 2015-2027 configurado en `config/sources.yaml` está agotado y debería
    expandirse o revisarse por qué tantas ventanas retornan 0 artículos útiles.
  - Pendientes tras esta sesión: 6 (de los 11 originales, se procesaron 5). Los 6 restantes en
    cola (Utah uranium/agricultura, NY Farm Bureau, "Reef Saudi", "The Persian Qanat", IoT de
    precisión, catálogo de dípteros) también aparentan ser falsos positivos por el mismo patrón
    de causa raíz — pendientes de revisión en la próxima sesión.

## 2026-07-27 16:05
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-27 16:20
BUGFIX: 2 bugs adicionales encontrados y corregidos en `scripts/ingest.py`, descubiertos al
verificar que `mark-all-ingested --limit 5` hubiera marcado exactamente los 5 artículos
mostrados en pending_ingest.md:
  1. `mark_all_ingested()` llamaba `find_pending(limit=5)`, que trunca por orden alfabético de
     archivo (glob), mientras que `ingest --limit 5` (vía `run_prepare()`) selecciona por score
     de relevancia (`prioritize(..., strategy="score")`). Ambos comandos elegían conjuntos de
     artículos DISTINTOS. Efecto real detectado: se marcaron como "ingestados" 3 artículos
     nunca mostrados ni revisados por Claude (uranio en Utah, IoT de precisión, catálogo de
     dípteros), mientras 3 artículos sí revisados y confirmados como falsos positivos (MITI
     NCM, Box Elder, orden del Gob. Cox) quedaban sin marcar. Corregido: `mark_all_ingested()`
     ahora usa el mismo `prioritize(strategy="score")` que `run_prepare()`.
  2. `mark_ingested(url)` iteraba `processed.items()` sin excluir la clave interna
     `_gdelt_windows` (una lista, no dict) → `AttributeError: 'list' object has no attribute
     'get'` al intentar marcar por URL individual. Corregido: ahora itera
     `article_entries(processed)`, igual que el resto del código.
  Estado corregido manualmente en `sources/processed.json`: se revirtieron los 3 artículos no
  revisados a `ingested: false` y se marcaron los 3 revisados pendientes vía `mark-ingested`.
  El conjunto final de "ingestados" en esta sesión coincide exactamente con los 5 falsos
  positivos documentados arriba (16:03). Sin este chequeo, el wiki habría perdido silenciosamente
  el registro de qué se revisó — riesgo directo para la meta de "Tasa falsos positivos: 0%".
