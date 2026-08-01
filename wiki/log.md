---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-01
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

## 2026-08-01 00:00
ROUTINE: 16 pendientes revisados — 0 ingestados (16/16 falsos positivos)
  `stats` mostraba 16 pendientes. Se leyó `pending_ingest.md` (5) y se inspeccionó
  el resto directamente en `sources/articles/`. Los 16 artículos tienen 0 menciones
  de "Panamá"/"Panama" en su texto completo y NO son sobre agro panameño:
    - https://www.spa.gov.sa/en/N2096157 — programa agrícola de Arabia Saudita ("Reef Saudi")
    - https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/ — centro de datos en Utah, EE.UU.
    - https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/ — Utah, EE.UU.
    - https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/ — Utah, EE.UU.
    - https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/ — Utah, EE.UU.
    - https://www.nyfb.org/ — New York Farm Bureau, EE.UU.
    - https://whc.unesco.org/en/list/1506 — Qanat persa (Irán), patrimonio UNESCO
    - https://paultan.org/2026/07/07/miti-...-incentive-mechanism.../ — MITI/MIDA de Malasia (agencia de inversión, no Panamá)
    - https://ieeexplore.ieee.org/document/10945742 — paper IEEE sobre IoT y agricultura de precisión (genérico, sin país)
    - https://www.msn.com/en-us/news/other/cultural-rules-for-staying-with-locals-abroad/... — artículo de viajes, sin relación agro
    - https://archive.org/details/Cataloguedipter2SaoP — catálogo zoológico histórico (Brasil, 1966)
    - https://www.heraldo.es/.../luis-biendicho-vox-... — política ambiental de Aragón, España
    - https://www.heraldo.es/.../aragon-celebra-sentencia-supremo-... — normativa porcina de Aragón, España
    - https://www.heraldo.es/.../aega-pide-elecciones-campo-aragon-... — gremio agrario de Aragón, España
    - https://agenciabrasil.ebc.com.br/.../finep-vai-pagar-... — financiamiento agrícola de Brasil
    - https://www.heraldo.es/.../arvensis-agro-amplia-... — empresa agro de Aragón, España
  Ninguno fue ingestado al wiki. Los 16 se marcaron `ingested: true` en `processed.json`
  (vía `mark-ingested`) para despejar la cola de pendientes sin contaminar el wiki —
  mismo criterio usado el 2026-06-22 con los 7 falsos positivos previos.

  DIAGNÓSTICO DE CAUSA RAÍZ (falsos positivos):
  La búsqueda web `prensa_agro` en `config/sources.yaml` usa DDG (`ddgs.news`) con
  `site:prensa.com agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá`.
  El operador `site:` de DDG NO estaba siendo verificado — el código aceptaba
  cualquier resultado devuelto y lo etiquetaba como fuente "prensa.com" sin
  comprobar el dominio real de la URL. Además, el filtro `is_agro_relevant()`
  solo exige coincidencia de UN término genérico (p.ej. "MIDA", "agricultura"),
  sin requerir contexto de Panamá, por lo que términos ambiguos como "MIDA"
  (que en EE.UU./Utah es "Military Installation Development Authority" y en
  Malasia es una agencia de MITI) generan falsos positivos sistemáticos.

  FIX APLICADO: `scripts/fetch_news.py::fetch_ddg_search` ahora descarta
  cualquier resultado cuyo dominio (`urlparse(url).netloc`) no contenga el
  `site` configurado, antes de aceptar el artículo. Esto habría filtrado
  los 16 falsos positivos de esta sesión (ninguno pertenece a prensa.com).

  BUG ADICIONAL CORREGIDO: `scripts/ingest.py::mark_ingested` iteraba
  `processed.items()` sin excluir la clave interna `_gdelt_windows` (una
  lista, no un dict), causando `AttributeError` en cada llamada y bloqueando
  el marcado de artículos. Ahora usa `article_entries()` como el resto del
  código.

  Resultado: `python wiki_agro.py stats` → Pendientes de ingesta: 0 (antes 16).
  Artículos reales ingestados al wiki en esta sesión: 0 (todos falsos positivos).
