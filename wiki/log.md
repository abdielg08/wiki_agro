---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-27
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

## 2026-07-27 00:05
ROUTINE: Diagnóstico + 5 falsos positivos detectados (0 ingestados al wiki)
  `python wiki_agro.py stats` → 11 pendientes al inicio de la sesión.
  `python wiki_agro.py ingest --limit 5` entregó 5 artículos — **ninguno es sobre
  agro panameño**. NO se ingestaron al wiki (regla 9 de CLAUDE.md). Se marcaron
  como procesados (`mark-ingested`) para sacarlos de la cola:

  1. "MITI working on simplified NCM..." (paultan.org) — MITI/MIDA de **Malasia**
     (Malaysian Investment Development Authority), sin relación con Panamá.
  2. "Timeline: Kevin O'Leary data center plan..." (sltrib.com) — MIDA = **Military
     Installation Development Authority de Utah** (data centers), no agro.
  3. "Box Elder data center opponents..." (sltrib.com) — mismo MIDA de Utah.
  4. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) —
     mismo MIDA de Utah, calidad del aire, nada agropecuario.
  5. "Cultural Rules For Staying With Locals Abroad" (msn.com) — artículo de
     viajes que solo menciona MIDA de Utah de pasada.

  CAUSA RAÍZ (falso positivo sistémico): la fuente "prensa.com" en el pipeline
  de fetch NO está trayendo contenido de La Prensa Panamá — está haciendo una
  búsqueda genérica por la palabra clave "MIDA" sin filtro geográfico/contexto,
  y "MIDA" colisiona con dos siglas no panameñas (Malaysia Investment
  Development Authority, Utah Military Installation Development Authority).

  Se revisaron también los 6 artículos pendientes restantes (no ingestados en
  este batch por límite de 5/sesión) — **los 6 son igualmente falsos
  positivos**, ninguno sobre agro de Panamá:
  - archive.org — catálogo de dípteros (entomología, no agro-Panamá)
  - ieeexplore.org/document/10945742 — paper IoT/agricultura de precisión (genérico, no Panamá)
  - sltrib.com — "Utah nuclear energy state" (MIDA de Utah otra vez)
  - whc.unesco.org/en/list/1506 — "The Persian Qanat" (patrimonio, Irán)
  - spa.gov.sa/en/N2096157 — "Reef Saudi" agricultura de secano (Arabia Saudita, no Panamá)
  - nyfb.org — New York Farm Bureau (agro de EE.UU., no Panamá)

  Se corrigió un bug en `scripts/ingest.py::mark_ingested()` que crasheaba al
  iterar `processed.json` porque no excluía la clave interna `_gdelt_windows`
  (lista, no dict) — ahora usa `article_entries()` como el resto de funciones.

  **ALERTA — recomendación para el usuario**: el fetcher de la fuente
  "prensa.com" necesita ajustarse (query más específica, ej. `"MIDA" AND
  "Panamá"`, o restringir dominio a prensa.com real) para dejar de traer
  ruido de Malasia/Utah/Arabia Saudita. Esto ya había ocurrido antes
  (ver entrada 2026-06-22 en metrics.md: "fix de 7 falsos positivos") — el
  problema es recurrente, no se resolvió de raíz.

  **Días sin artículos reales nuevos**: el último artículo genuinamente nuevo
  llegó el 2026-07-20 (y de los 2 "nuevos" de ese día, ambos resultaron ser
  falsos positivos de Utah). Han pasado 7 días corridos sin ingesta real
  nueva — supera el umbral de 3 días de CLAUDE.md. GitHub Actions sí corrió
  diariamente (commits `chore(sources)` hasta 2026-07-26) pero devolvió 0 o
  solo ruido.

  Ventanas GDELT completadas: 56 (supera el estimado de ~45) → el rango
  histórico 2015-hoy probablemente ya está agotado; el avance futuro depende
  de que las fuentes RSS (IICA, La Prensa) u otra fuente de calidad traigan
  contenido nuevo, no de GDELT.

  Estado tras esta sesión: 6 pendientes (todos sospechosos de ser falsos
  positivos, ver arriba), 18 ingestados, 0 páginas nuevas de wiki (no había
  contenido legítimo que ingestar).
  Fuentes con cobertura: MIDA (2), TVNNoticias (1), LaPrensaEco (1), BDA (1), IICA (1)
