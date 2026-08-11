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

## 2026-08-11 00:00
INGEST: lote de 5 artículos revisado — 0 ingestados, 5 falsos positivos (tasa FP: 100%)
  Causa raíz: colisión de palabra clave "MIDA" — el acrónimo panameño (Ministerio
  de Desarrollo Agropecuario) coincide con acrónimos homónimos de otras
  jurisdicciones sin relación con Panamá ni con agropecuaria:
    - "MIDA" (Utah, EE.UU.) = Military Installation Development Authority,
      entidad de desarrollo económico/urbanístico involucrada en un proyecto
      de centro de datos de Kevin O'Leary
    - "MIDA" también aparece en contexto de MITI/MARii (Malasia), agencias de
      inversión e industria — no agropecuarias
  Artículos rechazados (NO ingestados, sin páginas de wiki creadas/modificadas):
    1. "MITI working on simplified NCM..." (paultan.org, 2026-07-08) — industria/inversión Malasia, MIDA=agencia malaya no relacionada
    2. "Timeline: Kevin O'Leary data center plan..." (sltrib.com, 2026-05-19) — centro de datos en Utah, MIDA=Military Installation Development Authority
    3. "Box Elder data center opponents..." (sltrib.com, 2026-05-27) — mismo caso Utah MIDA
    4. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29) — mismo caso Utah MIDA
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07) — artículo de viajes, mención tangencial a demanda contra Utah MIDA
  Acción: marcados como ingestados vía `mark-all-ingested` para limpiarlos de la
  cola de pendientes (ya fueron revisados y descartados, no requieren reproceso).
  Recomendación: el fetch debería filtrar por dominio/país o exigir coincidencia
  adicional con términos agropecuarios además de "MIDA" para reducir falsos
  positivos futuros de esta fuente (prensa.com / agregador).

## 2026-08-11 16:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-11 16:10
DIAGNÓSTICO: revisados los 11 artículos pendientes restantes vía sources/processed.json
  — 11/11 son falsos positivos (tasa FP de la cola completa: 16/16 = 100%)
  Ninguno trata sobre agropecuaria de Panamá. Todos etiquetados con
  `"source": "prensa.com"` en processed.json, pero esa etiqueta es genérica del
  fetch, no refleja el dominio real del artículo (ver URLs abajo).
  Artículos rechazados (NO ingestados):
    1. "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa, 2026-06-24) — agricultura de secano en Arabia Saudita
    2. "Timeline: Kevin O'Leary data center plan..." (sltrib.com, 2026-05-19) — MIDA=Utah Military Installation Development Authority
    3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29) — mismo caso Utah MIDA
    4. "Box Elder data center opponents..." (sltrib.com, 2026-05-27) — mismo caso Utah MIDA
    5. "New York Farm Bureau" (nyfb.org, 2026-06-17) — gremio agrícola de Nueva York, EE.UU.
    6. "The Persian Qanat" (whc.unesco.org, 2026-07-07) — patrimonio UNESCO, sistema de riego histórico de Irán
    7. "MITI working on simplified NCM..." (paultan.org, 2026-07-08) — industria/inversión Malasia, MIDA=agencia malaya
    8. "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es, 2026-05-03) — Aragón, España, caso Forestalia/Inaga
    9. "AEGA pide elecciones al campo en Aragón..." (heraldo.es, 2026-06-08) — Aragón, España
    10. "Finep vai pagar R$ 220 milhões para inovações em agricultura familiar" (agenciabrasil.ebc.com.br, 2026-07-02) — Brasil
    11. "Arvensis Agro amplía sus instalaciones..." (heraldo.es, 2026-06-23) — Aragón, España
  Acción: marcados como ingestados vía `mark-all-ingested --limit 0` para vaciar
  la cola de pendientes (todos ya revisados y descartados).
  CAUSA RAÍZ CONFIRMADA (afecta las 16 revisiones de esta sesión, 100% FP):
  el mecanismo de fetch no filtra por relevancia geográfica a Panamá — solo hace
  match por palabras clave genéricas (p.ej. "MIDA", "agricultura", "agro") sin
  exigir contexto panameño (dominio .pa, mención de Panamá/provincias, o fuentes
  de la lista de Nivel 1-4 de CLAUDE.md). Resultado: recoge acrónimos homónimos
  de otras jurisdicciones (MIDA-Utah, MIDA-Malasia) y noticias agrícolas de
  España, Brasil, Arabia Saudita, EE.UU. e Irán/UNESCO sin relación con Panamá.
  ACCIÓN REQUERIDA (fuera del alcance de esta sesión de ingesta): revisar y
  corregir el script de fetch (GDELT/RSS) para exigir coincidencia adicional con
  "Panamá" / dominios .pa / fuentes de confianza listadas en CLAUDE.md antes de
  guardar un artículo en sources/articles/. Hasta que se corrija, se espera que
  la mayoría de los artículos nuevos descargados sean falsos positivos.

## 2026-08-11 16:05
INGEST: 11 artículos marcados como ingestados por sesión Claude Code

## 2026-08-11 16:20
DIAGNÓSTICO AVANZADO: causa raíz localizada en código (Pendientes=0 tras limpieza)
  Cola vacía: 29/29 artículos descargados ya revisados, 0 pendientes.
  Días sin artículos nuevos: el último fetch que trajo artículos fue el commit
  3af3406 (2026-07-30, 3 artículos). Desde entonces, 6 corridas de GitHub Actions
  consecutivas (2026-07-31, 08-02, 08-04, 08-07, 08-10) reportaron "0 artículos
  nuevos descargados" — 12 días sin ingreso real, supera largamente el umbral de
  alarma de 3 días de CLAUDE.md.
  Ventanas GDELT completadas: 64 (`_gdelt_windows` en processed.json) — ya supera
  el umbral de 45, pero el backfill real no ha avanzado porque casi todo lo que
  llega no es de Panamá (ver abajo), no porque falten ventanas por recorrer.
  CAUSA RAÍZ EXACTA (código): `scripts/fetch_news.py::fetch_ddg_search()`
  (líneas ~244-303), usada para la fuente `prensa_agro` de
  `config/sources.yaml:157-161` (query: `site:prensa.com agropecuario OR
  agricultura OR ganadería OR MIDA OR cosecha Panamá`):
    1. El operador `site:prensa.com` no está siendo respetado por
       `DDGS().news()` (vertical de noticias) — los resultados vienen de
       dominios completamente ajenos (sltrib.com, thestar.com.my, heraldo.es,
       agenciabrasil.ebc.com.br, spa.gov.sa, nyfb.org, whc.unesco.org, etc.)
    2. La query usa `OR` entre términos amplios y globales ("agricultura",
       "MIDA") sin agrupación — cualquier resultado que matchee UNO solo de
       esos términos globales pasa el filtro, sin importar el país.
    3. `fetch_ddg_search()` solo llama a `is_agro_relevant()` (línea 290) antes
       de aceptar un resultado. Las funciones `_is_panama_related()` (línea 78)
       y `_is_blocked_domain()` (línea 72) YA EXISTEN en el mismo archivo pero
       NUNCA se invocan dentro de `fetch_ddg_search()` — están implementadas y
       sin usar. Por eso "MIDA" solo (sin contexto panameño) es suficiente para
       que pase el filtro.
    4. Además, la línea 296 asigna `"source": site or name`, es decir escribe
       `"prensa.com"` como fuente para TODO resultado de esta búsqueda sin
       verificar el dominio real — de ahí que processed.json muestre
       `"source": "prensa.com"` en artículos de sltrib.com, heraldo.es, etc.
  FIX RECOMENDADO (no aplicado en esta sesión — requiere revisión de código,
  fuera del alcance de una sesión de ingesta según CLAUDE.md, que solo permite
  tocar wiki/ y sources/processed.json vía mark-all-ingested):
    En `fetch_ddg_search()`, después de armar `title`/`url`/`body`, agregar:
      `if not _is_panama_related(title, url) or _is_blocked_domain(url): continue`
    junto al `is_agro_relevant(...)` existente, y fijar `"source"` al dominio
    real (`_url_domain(url)`) en vez de al nombre de la búsqueda configurada.
  Hasta que se aplique este fix, se espera que el fetch DDG siga produciendo
  ~100% falsos positivos y el backfill 2015→hoy no avance vía esta fuente.
  Fuentes RSS (IICA, La Prensa) y GDELT (con `sourcecountry:PA` ya en la query)
  no muestran este problema — el bug es específico de `fetch_ddg_search`.
