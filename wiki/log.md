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

## 2026-08-10 16:10
ROUTINE: Sesión de mantenimiento (backfill histórico + diagnóstico)

**FALSOS POSITIVOS — 16 artículos revisados, 0 ingestados (0 sobre agro de Panamá)**

Los 16 artículos pendientes (los únicos 16 restantes en cola) resultaron ser
100% falsos positivos, todos etiquetados con fuente "prensa.com":
  - MITI/MIDA (Malasia) — incentivos industriales (paultan.org)
  - MIDA de Utah (Military Installation Development Authority) — data center
    de Kevin O'Leary, 3 artículos (sltrib.com)
  - New York Farm Bureau (nyfb.org)
  - Arvensis Agro, AEGA, Luis Biendicho/Inaga — agricultura de Aragón,
    España, 3 artículos (heraldo.es)
  - "Reef Saudi" — agricultura de secano en Arabia Saudita (spa.gov.sa)
  - Finep — innovación agrícola en Brasil (agenciabrasil.ebc.com.br)
  - "The Persian Qanat" — sistema de riego histórico en Irán (unesco.org)
  - AEGA Aragón (elecciones al campo) y consejería de Medio Ambiente de
    Aragón — 2 artículos adicionales (heraldo.es)

Ninguno menciona Panamá, sus provincias o el canal. Ninguno se creó en
wiki/summaries/ ni se referenció en topics/ o entities/. Marcados
`ingested: true` en processed.json vía `mark-all-ingested` para sacarlos de
la cola (no se reintentarán), pero NO representan cobertura real del wiki.

**DIAGNÓSTICO — causa raíz identificada**

La fuente `web_searches.prensa_agro` (búsqueda DuckDuckGo, `config/sources.yaml`)
es responsable del 100% de los falsos positivos acumulados a la fecha
(23/23 artículos de "prensa.com" en `sources/processed.json` son falsos
positivos — ver también los 7 documentados el 2026-06-22). Dos bugs
combinados en `scripts/fetch_news.py`:

  1. `fetch_ddg_search()` nunca aplicaba el filtro `_is_panama_related()`
     que sí usan `fetch_rss()` y `fetch_gdelt_batch()` — solo verificaba
     relevancia agro genérica (`is_agro_relevant`), que hace match con
     acrónimos ambiguos como "MIDA" sin importar el país.
  2. La query en config (`site:prensa.com agropecuario OR agricultura OR
     ... OR MIDA OR cosecha Panamá`) no tenía paréntesis alrededor de los
     términos con OR, por lo que la restricción `site:prensa.com` solo
     aplicaba a la primera cláusula — DDG devolvía resultados de cualquier
     dominio que matcheara cualquiera de los términos sueltos (ej. "MIDA").

**FIX aplicado** (scripts/fetch_news.py, config/sources.yaml):
  - `fetch_ddg_search()` ahora aplica `_is_blocked_domain()` y
    `_is_panama_related()` (título+cuerpo+URL) antes de aceptar un
    resultado, igual que RSS y GDELT.
  - Query de `prensa_agro` reescrita con paréntesis:
    `site:prensa.com (agropecuario OR agricultura OR ... OR MIDA OR cosecha Panamá)`.
  - Pendiente de validar en la próxima corrida de GitHub Actions (no se
    pudo probar en vivo en esta sesión — sin acceso de red a DDG).

**DIAGNÓSTICO — ventanas GDELT infladas artificialmente**

`sources/processed.json._gdelt_windows` reporta 64 ventanas completadas
(por encima del umbral de 45 que CLAUDE.md interpreta como "rango agotado"),
pero 27 de esas 64 son la MISMA ventana final parcial (`20260618_*`)
re-fetcheada cada día con una fecha de fin distinta (crece 1 día por
corrida de Actions), porque la clave de ventana incluye la fecha de fin.
Solo 37 son ventanas trimestrales reales, cubriendo 2017-03-30 → 2026-06-17.
**El backfill de 2015-01-01 a 2017-03-29 (~9 trimestres) nunca se ha
fetcheado.** No se modificó `fetch_gdelt_historical()` en esta sesión — el
fix requiere cambiar la lógica de qué ventana final se marca "completa" y
merece su propia sesión con pruebas de red. Ver wiki/metrics.md.

**Días sin artículos nuevos**: el último commit con artículos nuevos fue
2026-07-30 (3 artículos). Han pasado 11 días hábiles sin ingesta real —
supera el umbral de fallo de 3 días definido en CLAUDE.md. GitHub Actions
SÍ está corriendo a diario (commits "0 artículos nuevos" cada 2-3 días
hasta hoy 2026-08-10), así que la causa no es que el fetch esté caído, sino
los dos bugs de arriba: DDG solo devuelve ruido y GDELT está reciclando la
misma ventana en vez de avanzar en el historial 2015-2017.

Pendientes tras esta sesión: 0. Páginas wiki sin cambios (20). Próxima
sesión debería: (a) verificar que el fix de DDG produzca resultados reales
tras la próxima corrida de Actions, (b) si sigue en 0, considerar
desactivar temporalmente `prensa_agro` o acotar su query, y (c) planear el
fix de la ventana GDELT final para desbloquear el backfill 2015-2017.

## 2026-08-10 16:09
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-10 16:09
INGEST: 11 artículos marcados como ingestados por sesión Claude Code
