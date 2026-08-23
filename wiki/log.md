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

## 2026-08-23 00:00
ROUTINE: Sesión de mantenimiento — 17 pendientes revisados, 0 ingestados al wiki (todos falsos positivos)

  **FALSOS POSITIVOS (12, revisados en esta sesión, NO ingestados al wiki)**:
    - paultan.org/...miti-working-on-simplified-ncm... (MITI Malasia, ministerio de industria/comercio malayo — colisión "MIDA")
    - sltrib.com/.../box-elder-data-center-opponents (MIDA = Military Installation Development Authority, Utah)
    - sltrib.com/.../utah-governor-issues-order-protect (ídem, MIDA de Utah)
    - sltrib.com/.../kevin-oleary-data-center-timeline (ídem, MIDA de Utah)
    - msn.com/.../cultural-rules-for-staying-with-locals-abroad (artículo de viajes, menciona MIDA de Utah de paso)
    - maine.gov/dacf/ard (agricultura de Maine, EE.UU. — sin relación con Panamá)
    - agenciabrasil.ebc.com.br/.../finep-agricultura-familiar (agricultura de Brasil)
    - whc.unesco.org/en/list/1506 (sistema de qanats de Irán)
    - heraldo.es/.../aega-pide-elecciones-campo-aragon (agricultura de Aragón, España)
    - nyfb.org (New York Farm Bureau, EE.UU.)
    - heraldo.es/.../arvensis-agro-amplia-sus-instalaciones (empresa aragonesa, España)
    - spa.gov.sa/en/N2096157 (programa "Reef Saudi", Arabia Saudita)
    - heraldo.es/.../luis-biendicho-consejeria-medio-ambiente (política ambiental de Aragón, España)

  Ninguno trata sobre el sector agropecuario de Panamá. Todos marcados `ingested: true`
  vía `mark-all-ingested` para despejar la cola, sin crear páginas de wiki ni resúmenes.

  **DIAGNÓSTICO — causa raíz (auditoría completa de processed.json)**:
    De 30 artículos descargados acumulados, solo 6 son reales (datos semilla). Los otros
    24 (80%) son falsos positivos — 12 ya estaban marcados de sesiones previas, 12 se
    procesaron en esta sesión. Causa raíz identificada en `scripts/fetch_news.py`:
      1. `fetch_ddg_search()` construye la consulta como `site:{site} {query}`, pero
         `ddgs.news()` NO respeta de forma confiable el filtro `site:` — devuelve
         resultados de dominios completamente ajenos (thestar.com.my, sltrib.com,
         heraldo.es, nyfb.org, spa.gov.sa, etc.) y el código los etiquetaba igual
         como fuente "prensa.com" sin verificar el dominio real.
      2. `is_agro_relevant()` hace match de CUALQUIER término de `search_terms` (ej.
         "MIDA", "agricultura", "riego") sin exigir ningún contexto de Panamá, así que
         "MIDA" (Malasia/Utah) o "agricultura" (cualquier país) pasan el filtro.
    **Fix aplicado** (`scripts/fetch_news.py`): se agregó verificación de que el dominio
    real del resultado (`urlparse(url).netloc`) contenga el `site` configurado antes de
    aceptar un resultado de búsqueda web — descarta en origen los casos vistos arriba.
    También se corrigió un bug en `scripts/ingest.py::mark_ingested()` que crasheaba con
    `AttributeError` al iterar sobre la clave `_gdelt_windows` (lista, no dict) de
    `processed.json`.
    **Bug adicional corregido**: `mark_all_ingested()` usaba el orden crudo de
    `find_pending()` (por nombre de archivo) mientras que `ingest` (`run_prepare`) usa
    `prioritize(strategy="score")` — dos órdenes distintos. Esto causaba que
    `mark-all-ingested --limit N` marcara artículos DISTINTOS a los que realmente se
    mostraron en `pending_ingest.md` y fueron revisados por Claude Code, arriesgando que
    artículos reales de Panamá quedaran marcados `ingested: true` sin nunca generar
    contenido en el wiki. Se corrigió para que `mark_all_ingested()` use la misma
    `prioritize()` que `run_prepare()`, con `--strategy/--year/--source` opcionales que
    deben coincidir con los usados en `ingest`.

  **Señal de alarma activada**: 3 días consecutivos sin artículos nuevos reales
    (commits automáticos 2026-08-20, 08-21, 08-22 con "0 artículos nuevos"; el único
    artículo nuevo reciente, 2026-08-19, resultó ser otro falso positivo del mismo tipo).
    Ventanas GDELT completadas: 73 (ya superó el estimado de ~45-46 para 2015→hoy sin
    producir contenido real adicional) — indica que el backfill GDELT tampoco está
    aportando artículos genuinos de Panamá, o los está aportando pero luego se pierden
    entre el ruido de falsos positivos del mismo `is_agro_relevant()` sin filtro de país.
    Sin capacidad de ejecutar el fetch en esta sesión (routine de mantenimiento del
    wiki, no de fetch) — el fix de dominio debería reducir drásticamente el ruido en la
    próxima corrida de GitHub Actions; requiere validación en la próxima sesión.

  Cobertura post-sesión: 30 descargados, 30 ingestados (6 reales + 24 falsos positivos
  documentados), 0 pendientes. Páginas de wiki: sin cambios (20).

## 2026-08-23 16:11
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-23 16:13
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-23 16:13
INGEST: 7 artículos marcados como ingestados por sesión Claude Code
