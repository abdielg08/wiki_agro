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

## 2026-08-05 00:00
INGEST: 5 artículos revisados, 0 ingestados — 5 falsos positivos detectados (0% falsos positivos preservado)
  Falsos positivos (NO ingestados):
    - "MITI working on simplified NCM..." (paultan.org) → MIDA = Malaysian Investment Development Authority, no relación con Panamá
    - "Timeline: Kevin O'Leary data center..." (sltrib.com) → MIDA = Military Installation Development Authority (Utah, EE.UU.), no relación con Panamá
    - "Box Elder data center opponents..." (sltrib.com) → mismo MIDA de Utah, no relación con Panamá
    - "Utah Gov. Cox issues order..." (sltrib.com) → mismo MIDA de Utah, no relación con Panamá
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) → menciona MIDA de Utah tangencialmente, artículo de viajes sin relación agropecuaria
  Marcados como ingested=true vía `mark-all-ingested --limit 5` para despejar la cola (decisión de rechazo ya tomada, no deben reaparecer en pending_ingest.md).

DIAGNÓSTICO — causa raíz identificada (afecta a los 16 pendientes, no solo a este batch de 5):
  Se inspeccionó `sources/processed.json`: los 16 artículos pendientes de ingesta provienen TODOS
  de dominios ajenos a Panamá y sin relación agropecuaria: sltrib.com (Utah, x3), paultan.org
  (Malasia), spa.gov.sa (Arabia Saudita), nyfb.org (NY Farm Bureau, EE.UU.), whc.unesco.org,
  ieeexplore.ieee.org, archive.org, msn.com, heraldo.es (Aragón, España, x3), agenciabrasil.ebc.com.br
  (Brasil). Ninguno es sobre agro panameño.
  Causa: en `config/sources.yaml` (fuente ddg_search "laprensa_agro"), la búsqueda usa
  `site:prensa.com` + query con el término "MIDA" (para capturar noticias del Ministerio de
  Desarrollo Agropecuario). `scripts/fetch_news.py::fetch_ddg_search()` arma
  `full_query = f"site:{site} {query}"` y llama `ddgs.news(full_query)`, pero el resultado NO
  está restringido al dominio prensa.com — ddgs.news() está ignorando (o el proveedor subyacente
  no soporta) el operador `site:`, devolviendo resultados globales de noticias en inglés que
  contienen la palabra "MIDA" (coincide con acrónimos homónimos: Malaysian Investment Development
  Authority, Utah's Military Installation Development Authority, etc.), y el pipeline los guarda
  todos con `source: "prensa.com"` sin validar el dominio real de la URL devuelta.
  Impacto: el fetch diario (GitHub Actions, corre ~diario según `git log -- sources/`) sigue
  activo, pero la mayoría de los artículos que SÍ trae son ruido de este bug — explica por qué
  la mayoría de corridas reportan "0 artículos nuevos" útiles y por qué no hay avance real del
  backfill 2015→hoy pese a fetches diarios.
  Recomendación (no aplicada en esta sesión — fuera del alcance de la routine, requiere tocar
  scripts/fetch_news.py): (a) validar que el dominio de cada resultado de ddgs.news() coincida
  con `site_cfg["site"]` antes de guardarlo, descartando lo que no coincida; (b) evaluar retirar
  el término ambiguo "MIDA" de la query o añadir contexto ("Panamá") obligatorio en el query string
  en vez de depender solo del filtro de sitio.

## 2026-08-05 08:05
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
