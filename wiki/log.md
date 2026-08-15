---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-15
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

## 2026-08-15 00:00
ROUTINE: Diagnóstico + 16 falsos positivos detectados y documentados

`python wiki_agro.py stats` mostró 16 pendientes de ingesta. `ingest --limit 5`
entregó un lote (`pending_ingest.md`) donde NINGUNO de los 5 artículos era
sobre agro de Panamá. Se inspeccionó `sources/processed.json` directamente y
se confirmó que los 16 pendientes totales son falsos positivos, ninguno
relacionado con Panamá:

FALSOS POSITIVOS (16, ninguno ingestado, 0 páginas de wiki creadas):
  - paultan.org — MITI/MIDA de Malasia (incentivos de inversión industrial)
  - sltrib.com ×3 — MIDA = Military Installation Development Authority (Utah, EE.UU.),
    centros de datos de Kevin O'Leary, orden del gobernador Cox, oposición en Box Elder
  - msn.com — artículo de viajes, menciona la MIDA de Utah de forma tangencial
  - spa.gov.sa — programa "Reef Saudi" de agricultura de secano (Arabia Saudita)
  - nyfb.org — New York Farm Bureau (EE.UU.)
  - whc.unesco.org — Qanats persas (patrimonio UNESCO, Irán)
  - ieeexplore.ieee.org — paper técnico genérico sobre IoT y agricultura de precisión
  - archive.org — catálogo taxonómico de dípteros de América (no es noticia agro-PA)
  - heraldo.es ×3 — Aragón, España (medio ambiente, ganadería porcina, elecciones al campo)
  - agenciabrasil.ebc.com.br — Finep, financiamiento a agricultura familiar (Brasil)

CAUSA RAÍZ IDENTIFICADA Y CORREGIDA:
  `scripts/fetch_news.py::fetch_ddg_search()` (usada por la búsqueda web
  `prensa_agro`, query: "agropecuario OR agricultura OR ganadería OR MIDA OR
  cosecha Panamá") NO aplicaba el filtro `_is_panama_related()` que sí tienen
  las rutas RSS y GDELT. El operador `site:prensa.com` de DuckDuckGo no se
  respeta de forma confiable, y el término "MIDA" es ambiguo (coincide con
  Malasia y con la Military Installation Development Authority de Utah), así
  que la búsqueda devolvía artículos de cualquier sitio/país que mencionaran
  esos términos. Fix aplicado: se agregó el mismo guard de Panamá
  (`_is_panama_related` + `_is_blocked_domain`) que usan RSS y GDELT antes del
  `yield` en `fetch_ddg_search()`.

BUG SECUNDARIO CORREGIDO:
  `scripts/ingest.py::mark_ingested()` iteraba `processed.items()` sin filtrar
  la clave interna `_gdelt_windows` (una lista), causando `AttributeError:
  'list' object has no attribute 'get'` en cada llamada. Se corrigió para usar
  `article_entries(processed)`, igual que `mark_all_ingested()`.

ACCIÓN: los 16 artículos se marcaron como `ingested: true` (revisados y
descartados) vía `mark-ingested` para no bloquear la cola de pendientes.
Pendientes de ingesta: 16 → 0. Páginas de wiki creadas esta sesión: 0
(tasa de falsos positivos = 0% de contenido publicado, como exige CLAUDE.md).

DIAGNÓSTICO ADICIONAL:
  - Último commit con artículos nuevos REALES: 2026-07-30 (16 días atrás)
    — los "artículos nuevos" de las corridas de GitHub Actions entre esa
    fecha y hoy eran, en su totalidad, los falsos positivos aquí descritos.
  - Ventanas GDELT completadas: 67 (supera la estimación original de ~45),
    lo que sugiere que el rango histórico 2015→hoy ya está cubierto o que las
    ventanas se están re-generando sin alinearse a los trimestres calendario
    originales (ver `_gdelt_windows` en `sources/processed.json`, valores no
    alineados a Q1-Q4, p.ej. `20260618_20260708`). Requiere revisión del
    generador de ventanas en `scripts/fetch_historical.py` en una próxima
    sesión — no se modificó en esta sesión por estar fuera de alcance del
    diagnóstico de falsos positivos.
  - Fuentes RSS activas (IICA, La Prensa) no fueron la causa; el problema
    estaba aislado a la búsqueda DDG `prensa_agro`.
