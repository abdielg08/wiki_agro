---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-21
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

## 2026-08-21 (routine)
DIAGNÓSTICO: `stats` reportó 30 descargados / 13 ingestados / 17 pendientes.
INGEST: `ingest --limit 5` entregó 5 artículos en `pending_ingest.md`. Los 5 son
**falsos positivos** — NO se ingestaron al wiki (regla 9 de CLAUDE.md):
  - `paultan.org/.../miti-working-on-simplified-ncm-...` — MITI/MARii de Malasia;
    "MIDA" = Malaysian Investment Development Authority, no el MIDA panameño.
  - `sltrib.com/.../box-elder-data-center-opponents` — oposición ciudadana a un
    data center en Utah, EE.UU.; "MIDA" = Military Installation Development
    Authority (autoridad estatal de Utah), sin relación agropecuaria.
  - `sltrib.com/.../utah-governor-issues-order-protect` — orden del gobernador
    de Utah sobre calidad de aire/Great Salt Lake; mismo MIDA de Utah.
  - `sltrib.com/.../kevin-oleary-data-center-timeline` — cronología del proyecto
    de data center de Kevin O'Leary en Utah; mismo MIDA de Utah.
  - `msn.com/.../cultural-rules-for-staying-with-locals-abroad` — artículo de
    viajes/cultura sin relación con el tema; capturado solo por mención lateral
    del mismo MIDA de Utah en una demanda legal.
  Marcados como ingestados (`mark-all-ingested --limit 5`) para vaciar la cola,
  sin crear páginas de wiki. Ningún contenido de wiki fue creado a partir de
  estos 5 artículos.

DIAGNÓSTICO DE CAUSA RAÍZ (falsos positivos sistémicos, fuente `prensa.com`):
  Se revisó `sources/processed.json` completo: de 24 artículos con
  `source: prensa.com`, **0 corresponden a La Prensa de Panamá**. Todos
  provienen de sitios ajenos (paultan.org, sltrib.com, thestar.com.my,
  heraldo.es, worldbank.org, ieeexplore.ieee.org, msn.com, whc.unesco.org,
  maine.gov, nyfb.org, spa.gov.sa, archive.org, agenciabrasil.ebc.com.br).
  Causa: la búsqueda web `prensa_agro` en `config/sources.yaml` usa
  `site:prensa.com` combinado con `query: "... OR MIDA OR ..."` vía DuckDuckGo
  (ddgs) — el operador `site:` no está siendo respetado por el wrapper de
  búsqueda, y el término suelto "MIDA" hace match con acrónimos homónimos no
  panameños en cualquier sitio (Malaysian Investment Development Authority,
  Military Installation Development Authority de Utah, etc.), además de
  términos genéricos como "agricultura"/"agropecuario" que existen en
  cualquier país hispanohablante (p.ej. Aragón, España vía heraldo.es).
  De los 24 artículos `prensa.com`: 7 ya estaban marcados `ingested: true`
  como falsos positivos previamente (sesión 2026-06-22, ver metrics.md),
  ninguno tiene contenido en wiki/. Los 5 de esta sesión suman 12 falsos
  positivos confirmados de esta fuente sobre 24 intentos (0% de rendimiento
  real). Los 12 pendientes restantes de `prensa.com` en la cola tienen el
  mismo patrón (Utah/Malasia/Aragón) y muy probablemente también son falsos
  positivos — pendiente de revisión en próxima sesión.
  RECOMENDACIÓN (no aplicada en esta sesión — requiere decisión del usuario):
  desactivar o corregir la búsqueda `prensa_agro` en `config/sources.yaml`
  (quitar el término suelto "MIDA", exigir "Panamá"/"Panama" en la consulta,
  o verificar que `site:prensa.com` se aplique realmente en el wrapper ddgs).
  Mientras no se corrija, esta fuente seguirá generando falsos positivos y
  consumiendo ciclos de ingesta sin avanzar el backfill real.

Fetch automático (GitHub Actions): corrió normalmente los últimos días
  (commits `chore(sources): N artículos nuevos descargados` diarios), última
  corrida con contenido nuevo: 2026-08-19 (1 artículo). 2026-08-20 y
  2026-08-21 sin artículos nuevos — 2 días consecutivos, por debajo del
  umbral de alarma (3 días).

## 2026-08-21 08:16
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
