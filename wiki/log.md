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

## 2026-08-16 00:00
FALSOS POSITIVOS: 5/5 artículos del batch `ingest --limit 5` NO son sobre agro
de Panamá. Ninguno fue ingestado al wiki (0% falsos positivos — regla
innegociable). Detalle:
  1. "MITI working on simplified NCM..." (paultan.org) — MIDA = Malaysian
     Investment Development Authority (Malasia), no Panamá.
  2. "Timeline: Kevin O'Leary data center..." (sltrib.com) — MIDA = Military
     Installation Development Authority (Utah, EE.UU.).
  3. "Box Elder data center opponents..." (sltrib.com) — mismo MIDA de Utah.
  4. "Utah Gov. Cox issues order..." (sltrib.com) — mismo MIDA de Utah.
  5. "Cultural Rules For Staying With Locals Abroad" (msn.com) — artículo de
     viajes, menciona de pasada el litigio del MIDA de Utah.
  Marcados como `ingested: true` vía `mark-all-ingested --limit 5` (procesados
  y descartados, no reintentarán) — no se creó contenido en wiki/.

DIAGNÓSTICO — causa raíz identificada:
  Los 16 artículos pendientes (100% de la cola) son ruido global, no solo
  este batch de 5 — ver `queue --top 20`: Aragón (España), Utah, Arabia
  Saudita, Brasil, Nueva York, etc. Ninguno es de Panamá.
  Causa: en `scripts/fetch_news.py::fetch_ddg_search()`, la búsqueda DDG
  construye `site:prensa.com <query>` pero la librería `ddgs` (vertical
  `.news()`) no respeta de forma confiable el operador `site:`, devolviendo
  resultados de cualquier dominio. Combinado con `is_agro_relevant()` — que
  solo exige que aparezca UNA keyword genérica como "MIDA", "agricultura" o
  "cosecha" en cualquier parte del texto, sin exigir relación con Panamá —
  esto deja pasar cualquier artículo mundial que mencione esas palabras.
  Confirmado con `sources/processed.json`: los 7 falsos positivos marcados
  en la auditoría previa (2026-06-22, ver metrics.md) tienen el mismo
  patrón de dominios ajenos a prensa.com.
  Adicional: 0 artículos reales han entrado al wiki vía el pipeline
  automático (RSS+DDG+GDELT) desde el inicio del proyecto — los 6 artículos
  "reales" en wiki/ son semilla manual del 2026-05-24. Los feeds RSS
  (La Prensa, IICA) no están aportando contenido; el único canal activo es
  DDG search, y sale 100% contaminado.
  GitHub Actions sí corre a diario y termina en `success` (verificado runs
  2026-08-08 → 2026-08-15), por lo que el fallo NO es de infraestructura de
  CI sino de calidad del filtro de relevancia.

FIX APLICADO: `scripts/fetch_news.py::fetch_ddg_search()` ahora filtra
  explícitamente por dominio (`site.lower() in urlparse(url).netloc.lower()`)
  después de recibir resultados de `ddgs.news()`, en vez de confiar en que
  el operador `site:` de la query sea respetado. Esto debería eliminar la
  mayoría de los falsos positivos de dominios globales en la próxima corrida
  de GitHub Actions. Pendiente validar con la corrida del 2026-08-17.
  No se modificó `is_agro_relevant()` en esta sesión — si tras el fix de
  dominio siguen llegando falsos positivos (p.ej. de prensa.com pero sobre
  temas no agropecuarios), la siguiente routine debe además exigir mención
  de "Panamá"/"Panama" en el texto.

## 2026-08-16 08:17
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
