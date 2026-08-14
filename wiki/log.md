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

## 2026-08-14 00:47
ROUTINE: git pull OK. stats → 16 pendientes de ingesta. Se procesó lote de 5 (ingest --limit 5).

FALSOS POSITIVOS (5/5 del lote) — NINGUNO ingestado, NINGUNA página wiki creada/modificada:
  1. "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, MY)
     → Ministerio de Comercio e Industria de Malasia + MIDA = Malaysian Industrial
       Development Authority. No es Panamá.
  2. "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, Utah US)
     → MIDA = Military Installation Development Authority (Utah). No es agro, no es Panamá.
  3. "Box Elder data center opponents..." (sltrib.com, Utah US)
     → Mismo MIDA de Utah (data centers). No es Panamá.
  4. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, Utah US)
     → Mismo MIDA de Utah, calidad de aire/agua. No es agro panameño.
  5. "Cultural Rules For Staying With Locals Abroad" (msn.com, artículo de viajes)
     → Menciona MIDA de Utah de pasada. No tiene relación con agro ni con Panamá.

DIAGNÓSTICO DE CAUSA RAÍZ (falsos positivos sistémicos):
  Se inspeccionaron los 16 artículos pendientes completos (no solo el lote de 5):
  TODOS son falsos positivos. Fuentes reales: Arabia Saudita (spa.gov.sa), Utah US
  (sltrib.com x3), Malasia (paultan.org), New York Farm Bureau (nyfb.org, sin fecha/
  contenido real), UNESCO (whc.unesco.org), IEEE (ieeexplore.ieee.org), archive.org,
  Aragón/España (heraldo.es x3), Brasil (agenciabrasil.ebc.com.br). NINGUNO es de Panamá.

  Causa raíz identificada en scripts/fetch_historical.py:64-67 y scripts/fetch_news.py:
  - La query GDELT usa "MIDA" como término OR suelto (sin comillas ni contexto):
    `"agropecuario OR agricultura OR ganaderia OR MIDA OR IDIAP OR cosecha OR cultivo..."`
    "MIDA" colisiona con: Malaysian Industrial Development Authority, Military
    Installation Development Authority (Utah), y probablemente otros acrónimos.
  - El filtro `sourcecountry:PA` de GDELT no está excluyendo estos resultados
    (India, Malasia, España, Brasil, EEUU pasan el filtro).
  - Además, el pipeline hardcodea `"source": "prensa.com"`, `"language": "es"`,
    `"country": "PA"` en el JSON de CADA artículo GDELT sin verificar el dominio/idioma
    real (ver fetch_historical.py:103, fetch_news.py:235,299,420). Esto oculta el origen
    real y hace que el filtro de fuente en `stats` sea engañoso (23/29 artículos
    descargados aparecen como "prensa.com" sin serlo).

  Impacto: 0 artículos legítimos ingestados en este backfill desde 2026-07-29/30
  (últimos commits con "N artículos nuevos" > 0). Desde entonces (~2 semanas), GitHub
  Actions corre a diario pero solo trae falsos positivos o "0 artículos nuevos".

  Recomendación para el usuario (NO aplicada en esta sesión — requiere revisión):
    a. Quitar "MIDA" como término suelto de _AGRO_QUERY, o exigir coocurrencia con
       "Panamá"/"panameño" en la consulta GDELT.
    b. No confiar en `sourcecountry:PA`; validar el dominio real contra un allowlist
       de fuentes panameñas (prensa.com, panamaamerica.com.pa, tvn-2.com, mida.gob.pa, etc.)
       antes de guardar el artículo.
    c. Dejar de hardcodear source/language/country — extraerlos del artículo real.

  Se recomienda a la routine de mañana: revisar si el usuario aplicó el fix antes de
  seguir ingestando; si no, todo artículo nuevo con fuente etiquetada "prensa.com" debe
  verificarse manualmente contra la URL real antes de ingestar.

Resultado del lote: 0 artículos ingestados, 5 marcados como procesados (mark-all-ingested)
para liberar la cola de pendientes — no vuelven a aparecer en pending_ingest.md.
Pendientes restantes tras este lote: 11 (todos ya inspeccionados arriba y confirmados
como falsos positivos también — quedarán marcados en próximas rutinas).

## 2026-08-14 00:48
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
