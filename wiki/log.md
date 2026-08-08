---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-08
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

## 2026-08-08 08:05
INGEST: 16 artículos marcados como ingestados por sesión Claude Code
  (nota: el mensaje automático de arriba dice "ingestados" pero ver el
  diagnóstico completo abajo — los 16 son FALSOS POSITIVOS, no se creó
  contenido de wiki para ninguno)

## 2026-08-08 08:10
ROUTINE: Sesión programada — diagnóstico de falsos positivos y fix de bug

**Paso 1-2**: `git pull origin main` (branch ya actualizado, sin cambios) →
`python wiki_agro.py stats` mostró 16 artículos pendientes de ingesta.

**Paso 3 — Verificación de los 5 artículos del batch (`ingest --limit 5`)**:
Los 5 artículos NO son sobre agro de Panamá (0% relevancia):
  - "MITI working on simplified NCM..." (paultan.org) — Malasia, MITI/MIDA
    de Malasia, no tiene relación con Panamá.
  - "Kevin O'Leary data center timeline" (sltrib.com) — Utah, EE.UU.,
    "MIDA" = Military Installation Development Authority (Utah), no
    Ministerio de Desarrollo Agropecuario de Panamá.
  - "Box Elder data center opponents" (sltrib.com) — Utah, EE.UU.
  - "Utah Gov. Cox... data centers" (sltrib.com) — Utah, EE.UU.
  - "Cultural Rules For Staying With Locals Abroad" (msn.com) — artículo
    de viajes genérico, menciona MIDA de Utah de pasada.
  Ninguno menciona "Panamá" ni una sola vez en título o texto. NO se
  ingestaron — no se creó ningún summary ni se tocó ningún topic/entity.

**Diagnóstico ampliado**: se revisaron los 16 artículos pendientes (no solo
los 5 del batch) porque el patrón de falsos positivos era sistemático.
Resultado: **16/16 son falsos positivos**, 0 menciones de "Panamá"/"Panama"
en título o cuerpo de texto en ninguno. Fuentes reales (mal etiquetadas
todas como "prensa.com" en processed.json):
  spa.gov.sa (Arabia Saudita), sltrib.com ×3 (Utah, EE.UU.), nyfb.org
  (New York Farm Bureau), whc.unesco.org (Qanat persa, Irán), paultan.org
  (Malasia), ieeexplore.ieee.org (paper IoT genérico), msn.com (viajes),
  archive.org (catálogo de dípteros), heraldo.es ×3 (Aragón, España),
  agenciabrasil.ebc.com.br (Brasil).

**Causa raíz identificada**: `scripts/fetch_news.py::fetch_ddg_search()`
(usado por la búsqueda web `prensa_agro` con `site:prensa.com`) NO aplicaba
los mismos filtros que sí tienen los fetchers de RSS y GDELT:
  1. No verificaba que el dominio de la URL devuelta por DDG realmente
     coincidiera con el `site:` pedido — DDG no respeta ese operador de
     forma confiable en su endpoint de noticias, así que devolvía
     resultados de dominios completamente ajenos (sltrib.com, paultan.org,
     etc.) y el código los etiquetaba igual como fuente "prensa.com".
  2. No llamaba a `_is_panama_related()` — solo `is_agro_relevant()`, que
     hace match contra términos genéricos como "MIDA", "agricultura",
     "cosecha" sin exigir ningún término geográfico panameño. "MIDA"
     colisiona con la Malaysian Investment Development Authority y con la
     Utah Military Installation Development Authority.

**Fix aplicado**: `fetch_ddg_search()` ahora rechaza resultados cuyo
dominio no termine en el `site` solicitado, aplica `_is_blocked_domain()`,
y exige `_is_panama_related()` (término geográfico panameño explícito en
título/URL) — igual que ya hacían `fetch_rss()` y `fetch_gdelt_batch()`.
Commit incluido en esta sesión.

**Paso 4**: los 16 artículos se marcaron como `ingested: true` en
`processed.json` vía `mark-all-ingested --limit 0` (procesados/rechazados,
no ingestados al wiki) para desbloquear la cola de pendientes — quedaban
ahí desde corridas previas de Actions y ningún fetch futuro los va a
reintentar.

**Diagnóstico avanzado (Paso 5, pendientes=0 tras el fix)**:
  - Últimos commits de `sources/`: 2026-08-07 (0 nuevos), 2026-08-04 (0),
    2026-08-02 (0), 2026-07-31 (0), 2026-07-30 (3 nuevos — los que
    resultaron ser estos falsos positivos). **4 corridas consecutivas de
    Actions sin artículos reales nuevos** — señal de alarma según CLAUDE.md.
  - Ventanas GDELT completadas: 63 (antes 0 según metrics.md de 2026-06-22).
    Con 45+ ventanas completadas, el rango histórico configurado
    (2015-01-01 → 2027-12-31) está prácticamente agotado para GDELT; el
    fetch ya no está trayendo artículos reales porque no queda mucho rango
    nuevo por explorar y la única fuente activa devolviendo resultados era
    la búsqueda DDG rota (`prensa_agro`), ahora corregida.
  - Acción sugerida para próxima sesión: validar que con el fix de
    `fetch_ddg_search()` la corrida de GitHub Actions vuelva a traer
    artículos reales sobre agro panameño; si sigue en 0, revisar si RSS de
    IICA/La Prensa siguen activos y considerar sumar más `web_searches`
    dirigidas a dominios .gob.pa.
