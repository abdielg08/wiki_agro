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

## 2026-08-22 00:00
INGEST: 0 artículos reales ingestados — 5/5 falsos positivos detectados y rechazados
  Lote (`ingest --limit 5`, etiquetado erróneamente como fuente "prensa.com"):
    - paultan.org "MITI working on simplified NCM..." → MIDA = Malaysian Industrial Development Authority. No relacionado a Panamá.
    - sltrib.com "Box Elder data center opponents..." → MIDA = Military Installation Development Authority (Utah, EE.UU.). No agro.
    - sltrib.com "Utah Gov. Cox issues order to protect Great Salt Lake..." → MIDA = Utah MIDA. No agro, no Panamá.
    - sltrib.com "Timeline: How the Kevin O'Leary data center plan..." → MIDA = Utah MIDA. No agro, no Panamá.
    - msn.com "Cultural Rules For Staying With Locals Abroad" → artículo de viajes, mención tangencial a demanda contra MIDA (Utah). No agro.
  Ninguno ingestado al wiki (0% falsos positivos — regla innegociable). Marcados `ingested: true` en processed.json vía mark-all-ingested para sacarlos de la cola sin crear páginas.

DIAGNÓSTICO — causa raíz identificada y corregida:
  Los 5 artículos venían de la búsqueda DDG "prensa_agro" (`site:prensa.com` + término "MIDA"),
  pero sus URLs reales pertenecían a dominios totalmente ajenos (paultan.org, sltrib.com, msn.com).
  Dos bugs compuestos en `scripts/fetch_news.py`:
    1. `fetch_ddg_search()` no verificaba que la URL del resultado perteneciera al dominio
       consultado con `site:` — el backend de DDGS news no siempre respeta ese filtro.
    2. `is_agro_relevant()` hace match de substring simple contra `search_terms.primary/secondary`
       sin exigir contexto de Panamá; "MIDA" es un acrónimo ambiguo (coincide con Malaysia,
       con la "Military Installation Development Authority" de Utah, etc.) — mismo patrón que
       causó los 7 falsos positivos corregidos el 2026-06-22.
  Fix aplicado: `fetch_ddg_search()` ahora descarta resultados cuyo dominio (`urlparse(url).netloc`)
  no contenga el `site` consultado, antes de aplicar `is_agro_relevant()`. Esto habría bloqueado
  los 5 artículos de este lote.
  Pendiente de validar en la próxima corrida de `fetch --mode web` / GitHub Actions.

## 2026-08-22 08:11
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-22 08:30
BUGFIX — corrupción de datos detectada y revertida en processed.json:
  El comando `mark-all-ingested --limit 5` NO usa el mismo orden que `ingest --limit 5`
  (uno ordena por score de prioridad vía `prioritize()`, el otro por orden alfabético
  de archivo vía `find_pending()`). Al ejecutarlo tras el primer lote de falsos positivos,
  marcó `ingested: true` en 5 artículos completamente distintos a los 5 que realmente
  revisé — 4 de ellos NUNCA fueron leídos ni evaluados, y ninguno recibió página de wiki:
    - sltrib.com "Utah nuclear energy state" (no revisado)
    - ieeexplore.ieee.org/document/10945742 (no revisado)
    - archive.org "Catalogue dipter 2 Sao P" (no revisado)
    - heraldo.es "Aragón sentencia Supremo cerdo granjas" (no revisado)
  Revertidos a `ingested: false` en processed.json para que vuelvan a la cola y se
  revisen correctamente. (msn.com "Cultural Rules..." sí fue revisado como FP, se dejó igual).
  Fix aplicado en `scripts/ingest.py`: `mark_all_ingested()` ahora usa `prioritize(strategy="score")`,
  el mismo orden que `run_prepare()`, para garantizar que marque exactamente el lote mostrado
  en el último `pending_ingest.md`. Recomendación: preferir los comandos `mark-ingested <url>`
  exactos listados al final de `pending_ingest.md` sobre `mark-all-ingested --limit N`.

  Bug adicional encontrado y corregido en el mismo archivo: `mark_ingested(url_or_slug)`
  iteraba `processed.items()` sin filtrar las claves internas (`_gdelt_windows`, etc., que
  son listas, no dicts), causando `AttributeError: 'list' object has no attribute 'get'`
  en cualquier llamada. Ahora usa `article_entries()` como el resto del código.

## 2026-08-22 08:35
INGEST: 0 artículos reales ingestados — 5/5 falsos positivos (lote 2, `ingest --limit 5` reejecutado tras el bugfix)
  - paultan.org, sltrib.com ×3 → mismo homónimo MIDA (Malasia/Utah), ya documentado arriba.
  - heraldo.es "Aragón celebra sentencia Supremo... espacio cerdo granjas" → artículo real de
    porcicultura, pero sobre **España** (Aragón), no Panamá. Fuera de alcance del wiki
    (agro panameño únicamente). No ingestado.
  Los 5 marcados `ingested: true` individualmente vía `mark-ingested <url>` (no mark-all-ingested).
  Total falsos positivos de la sesión: 10/10 artículos revisados. 0 páginas de wiki creadas.

## 2026-08-22 08:14
INGEST: 11 artículos marcados como ingestados por sesión Claude Code

## 2026-08-22 08:40
INGEST: 0 artículos reales ingestados — 11/11 falsos positivos (resto de la cola, verificados por dominio y por ausencia de mención a "Panamá"/"Panama" en título y texto completo)
  - archive.org "Catalogue of the diptera of the Americas South of United States" (entomología, sin relación)
  - ieeexplore.ieee.org "Ambient IoT: Communications Enabling Precision Agriculture" (paper genérico IoT, sin país)
  - sltrib.com "Utah wants to process uranium..." (Utah, minería nuclear)
  - heraldo.es ×3: "Luis Biendicho asume consejería Medio Ambiente" / "AEGA pide elecciones al campo en Aragón" / "Arvensis Agro amplía instalaciones" (Aragón, España)
  - nyfb.org "New York Farm Bureau" (EE.UU., Nueva York)
  - spa.gov.sa "Reef Saudi... Rain-Fed Agriculture" (Arabia Saudita)
  - agenciabrasil.ebc.com.br "Finep vai pagar R$220 milhões... agricultura familiar" (Brasil)
  - whc.unesco.org "The Persian Qanat" (Irán, patrimonio UNESCO)
  - maine.gov "Agricultural Resource Development Division" (Maine, EE.UU.)
  Ninguno ingestado al wiki. Marcados `ingested: true` vía `mark-all-ingested` (ya corregido, orden
  irrelevante con --limit 0 = todos los pendientes) para vaciar la cola contaminada por el mismo bug
  de `fetch_ddg_search()` corregido arriba (búsqueda "prensa_agro" trayendo resultados de dominios
  ajenos a prensa.com en todo el mundo).

  **Cola de ingesta en 0 tras esta sesión.** Total falsos positivos detectados: 21/21 artículos
  revisados (10 del lote MIDA + 11 de este lote). 0 artículos reales ingestados, 0 páginas nuevas
  de wiki. Tasa de falsos positivos del lote: 100% — confirma que el bug de dominio en
  `fetch_ddg_search()` (ya corregido en este commit) era la causa raíz de que TODA la cola pendiente
  estuviera contaminada. El fix solo aplica a futuras corridas de `fetch --mode web`; no limpia
  retroactivamente `sources/articles/` (que permanecen inmutables por regla del proyecto).

## 2026-08-22 08:17
LINT: 20 páginas revisadas, 55 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:12, no_index:1
