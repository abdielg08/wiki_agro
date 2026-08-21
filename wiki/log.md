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

## 2026-08-21 00:00
ROUTINE: Diagnóstico — 17 artículos pendientes de ingesta detectados

FALSOS POSITIVOS (5/5 del lote — 0 ingestados, tasa falsos positivos del lote: 100%):
Todos coinciden en falso positivo por colisión de la sigla "MIDA" (no es
Ministerio de Desarrollo Agropecuario de Panamá en ninguno de los 5 casos):
  1. "MITI working on simplified NCM..." (paultan.org, 2026-07-08)
     → MIDA = Malaysian Investment Development Authority (Malasia), no Panamá.
  2. "Box Elder data center opponents..." (sltrib.com, 2026-05-27)
     → MIDA = Military Installation Development Authority (Utah, EE.UU.).
  3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
     → Mismo MIDA de Utah (data centers), sin relación con agro panameño.
  4. "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com, 2026-05-19)
     → Mismo MIDA de Utah.
  5. "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07)
     → Artículo de viajes/cultura sin relación con agro; mención tangencial
       al mismo caso MIDA de Utah en contexto de otro artículo relacionado.
  Ninguno de los 5 fue ingestado al wiki (0 páginas creadas/actualizadas).
  Marcados como procesados vía `mark-all-ingested --limit 5` para no
  reaparecer en pending_ingest.md.
  NOTA para el pipeline de fetch: el matching por palabra clave "MIDA" sin
  contexto de país/idioma sigue generando falsos positivos recurrentes
  (ver también auditoría de 2026-06-22 en wiki/metrics.md, 7 falsos previos).
  Recomendación: filtrar por country=PA + idioma español + dominio de fuente
  confiable antes de incluir en pending_ingest.md.

## 2026-08-21 16:16
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-21 16:35 (continuación de la entrada 16:16)
BUG DETECTADO — `mark-all-ingested` NO marca los mismos artículos que muestra `ingest`:

`python wiki_agro.py ingest --limit 5` selecciona el lote usando
`prioritize()` (estrategia `score`, en `scripts/prioritize.py`), pero
`mark-all-ingested --limit N` marca artículos usando `find_pending(limit=N)`
directamente (orden alfabético por nombre de archivo, sin scoring). Como
resultado, la llamada `mark-all-ingested --limit 5` de esta sesión NO marcó
los 5 artículos del lote 1 (MITI/MIDA Malasia, Box Elder, Great Salt Lake,
Kevin O'Leary), sino 5 artículos completamente distintos que nunca fueron
revisados:
  - Utah nuclear energy (sltrib.com) — no relacionado con Panamá
  - "Ambient IoT: Communications Enabling Precision Agriculture" (IEEE,
    paper genérico 6G, sin mención de Panamá)
  - "Cultural Rules For Staying With Locals Abroad" (msn.com) — sí
    coincide con el lote 1, revisado y confirmado falso positivo
  - "Catalogue of the diptera of the Americas South of United States"
    (archive.org) — catálogo zoológico brasileño de 1966/1967, sin relación
    con Panamá
  - Aragón (España) — sentencia sobre espacio por cerdo en granjas
Se verificó manualmente el contenido completo de los 4 artículos no
revisados: los 4 son falsos positivos igual (0% pérdida de contenido real
esta vez), pero el bug es grave: en una sesión futura `mark-all-ingested`
podría marcar como "ingestado" un artículo real de agro panameño sin que
Claude Code lo haya visto ni creado su página de wiki — pérdida silenciosa
de cobertura, violando la regla de "Pendientes > 0 = falla del sistema"
(el artículo desaparecería de pendientes sin haber sido procesado).

RECOMENDACIÓN: eliminar `mark-all-ingested` del flujo de la routine, o
hacer que use la misma función `prioritize()` que `ingest`. Mientras tanto,
esta sesión usa `mark-ingested '<url>'` (marcado explícito por URL) para
cada artículo que sí fue revisado.

BUG ADICIONAL — `mark-ingested <url>` crashea con `AttributeError`:
`scripts/ingest.py::mark_ingested()` itera `processed.items()` sin filtrar
las claves internas (p. ej. `_gdelt_windows`, que es una `list`, no un
`dict`), y falla en `meta.get("path", "")` para CUALQUIER url. A diferencia
de `mark_all_ingested()`, que sí usa `article_entries(processed)` para
excluir esas claves. Se marcaron los artículos de esta sesión editando
`sources/processed.json` directamente (mismo efecto que `mark-ingested`
habría tenido) como workaround. RECOMENDACIÓN: aplicar el mismo filtro
`article_entries()` dentro de `mark_ingested()`.

## 2026-08-21 16:45
ROUTINE: Continuación de ingesta — lotes 2, 3 y 4 (12 artículos restantes)

FALSOS POSITIVOS (12/12 — 0 ingestados al wiki):
  Lote 2 (5): MITI/MIDA Malasia (paultan.org), Box Elder data center
    (sltrib.com), Great Salt Lake / calidad del aire (sltrib.com), timeline
    Kevin O'Leary data center (sltrib.com), Agricultural Resource
    Development Division — Maine (maine.gov). Ninguno menciona Panamá;
    los 4 primeros son la misma colisión de sigla "MIDA" (Utah), el quinto
    es agricultura del estado de Maine, EE.UU.
  Lote 3 (5): Finep / agricultura familiar (Brasil, agenciabrasil.ebc.com.br,
    en portugués pese a `language: es` en los metadatos), "The Persian
    Qanat" (UNESCO, sistema de riego histórico de Irán), AEGA elecciones al
    campo en Aragón (heraldo.es, España), New York Farm Bureau (nyfb.org,
    EE.UU.), Arvensis Agro amplía instalaciones (heraldo.es, España).
  Lote 4 (2): "Reef Saudi" agricultura de secano (spa.gov.sa, Arabia
    Saudita), nombramiento de consejería de Medio Ambiente en Aragón
    (heraldo.es, España, caso Forestalia).
  Todos marcados como procesados en `sources/processed.json` (workaround
  manual por el bug de `mark-ingested` arriba descrito). 0 páginas de wiki
  creadas o actualizadas para estos 12 artículos.

DIAGNÓSTICO DE CAUSA RAÍZ — fuente "prensa.com" (DDG web search) rota:
De los 17 artículos pendientes al inicio de la sesión, **17/17 (100%)**
resultaron ser falsos positivos, todos etiquetados `source: prensa.com`,
`country: PA`, `language: es` pese a venir de dominios completamente
ajenos (heraldo.es, sltrib.com, ieeexplore.ieee.org, agenciabrasil.ebc.com.br,
archive.org, whc.unesco.org, paultan.org, maine.gov, nyfb.org, spa.gov.sa,
msn.com) y sin ninguna mención real de Panamá. Causa raíz identificada en
`scripts/fetch_news.py::fetch_ddg_search()` + `config/sources.yaml`:
  1. La búsqueda DDG usa `site:prensa.com` (`config/sources.yaml`, bloque
     `web_searches: prensa_agro`), pero `ddgs.news()` NO respeta ese filtro
     de forma confiable — devuelve resultados de dominios arbitrarios.
  2. El query configurado es
     `"agropecuario OR agricultura OR ganadería OR MIDA OR cosecha Panamá"`
     — todo unido con OR, por lo que "Panamá" es solo una alternativa más,
     no un requisito. Cualquier resultado que mencione "agricultura" o
     "MIDA" (sigla ambigua, ver bug de colisión documentado a las 00:00 de
     hoy) pasa el filtro sin mencionar Panamá en absoluto.
  3. `fetch_ddg_search()` (scripts/fetch_news.py líneas ~292-302) asigna
     `source`, `country: "PA"` y `language: "es"` de forma fija, ignorando
     el dominio y el idioma reales del resultado devuelto por DDG (ej.
     el artículo de Finep está en portugués pero quedó marcado `language: es`).
  4. `is_agro_relevant()` (scripts/fetch_news.py línea 123), usado como
     filtro de relevancia, solo verifica términos agropecuarios genéricos
     (`config/sources.yaml: search_terms`) y tampoco exige "Panamá"/"Panama".
  Esto explica también los 7 falsos positivos previos documentados en la
  auditoría de 2026-06-22 (wiki/metrics.md) — es un problema recurrente y
  sistémico, no un caso aislado.

RECOMENDACIÓN (para el usuario, no aplicada en esta sesión — cambio de
código fuera del alcance de la routine automática):
  - Cambiar el query DDG a exigir Panamá explícitamente, p. ej.
    `(agropecuario OR agricultura OR ganadería OR cosecha) AND (Panamá OR Panama)`
  - Validar que el dominio del resultado (`urlparse(url).netloc`) coincida
    con `site` antes de aceptarlo.
  - Exigir "panamá"/"panama" como término obligatorio (no solo uno más de
    la lista) en `is_agro_relevant()`.
  - Derivar `source`/`country`/`language` del resultado real, no hardcodear.
  - Ver también bugs de `mark-ingested`/`mark-all-ingested` documentados
    arriba (00:00 y 16:35 de hoy).

RESULTADO DE LA SESIÓN: 17 pendientes evaluados, 0 ingestados al wiki
(17/17 falsos positivos, documentados), 0 páginas de wiki nuevas o
modificadas. `python wiki_agro.py stats` → Pendientes de ingesta: 0.
