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

## 2026-08-06 00:00
INGEST: 0/5 artículos ingestados — 5 falsos positivos detectados, 0% ingestados al wiki
  Causa raíz: coincidencia de la sigla "MIDA" con entidades homónimas no panameñas.
  Ninguno de los 5 artículos trata sobre agro de Panamá. NO se creó ninguna página de wiki.
  Falsos positivos (marcados como procesados para no reaparecer en la cola):
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org) →
      Ministerio malasio de Comercio e Industria (MITI) y MARii (Malaysia Automotive,
      Robotics and IoT Institute). No relacionado con Panamá.
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com) →
      MIDA = Military Installation Development Authority de Utah, EE.UU. Centro de datos,
      no agricultura.
    - "Box Elder data center opponents hope for a vote..." (sltrib.com) →
      Mismo MIDA de Utah (autoridad de desarrollo militar/data centers), sin relación agro.
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) →
      Mismo MIDA de Utah; artículo sobre calidad del aire y centros de datos.
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) →
      Artículo de viajes/cultura sin relación con agro; mención tangencial de MIDA (Utah).
  Acción: python wiki_agro.py mark-ingested para las 5 URLs (evita reprocesamiento;
  ninguna generó contenido en wiki/).

## 2026-08-06 16:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-06 16:10
BUGFIX: `mark_ingested()` en scripts/ingest.py fallaba con AttributeError al
  iterar `processed.items()` sin filtrar la clave interna `_gdelt_windows`
  (una lista, no un dict). Se corrigió para usar `article_entries(processed)`,
  igual que `mark_all_ingested()`. También se detectó que `mark-all-ingested`
  usa un orden distinto (por nombre de archivo) al de `ingest` (por score de
  prioridad) — por eso solo marcó 1 de los 5 artículos mostrados en el lote
  anterior. Los 4 restantes se marcaron manualmente con `mark-ingested <url>`.
  Recomendación: preferir siempre los comandos `mark-ingested` explícitos por
  URL que genera `pending_ingest.md`, no `mark-all-ingested`.

## 2026-08-06 16:12
INGEST: 0/1 artículos ingestados — 1 falso positivo detectado (lote 2)
  - "New York Farm Bureau" (nyfb.org) → organización agrícola de Nueva York,
    EE.UU. Sin relación con Panamá. NO se creó página de wiki.

## 2026-08-06 16:20
INGEST: 0/5 artículos ingestados — 5 falsos positivos detectados (lote 3)
  Todos son noticias agrícolas legítimas pero de OTROS países, no Panamá:
    - "Arvensis Agro amplía sus instalaciones..." (heraldo.es) → España/Aragón.
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa) → Arabia Saudita.
    - "Finep vai pagar R$ 220 milhões..." (agenciabrasil.ebc.com.br) → Brasil.
    - "The Persian Qanat" (whc.unesco.org) → sitio patrimonio UNESCO, Irán.
    - "AEGA pide elecciones al campo en Aragón..." (heraldo.es) → España/Aragón.
  NO se creó ninguna página de wiki. Marcados como procesados con mark-ingested
  por URL para no reaparecer en la cola.

## 2026-08-06 16:25
INGEST: 0/1 artículos ingestados — 1 falso positivo detectado (lote 4, último pendiente)
  - "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es) →
    Política regional de Aragón, España (consejería de Medio Ambiente/Agricultura,
    caso Forestalia). Sin relación con Panamá. NO se creó página de wiki.

## 2026-08-06 16:40
DIAGNÓSTICO AVANZADO (pendientes = 0 tras procesar 16/16 falsos positivos):

Resumen de la sesión: los 16 artículos pendientes eran 100% falsos positivos
(0 páginas de wiki nuevas). Tasa de falsos positivos de la sesión: 100% de lo
descargado, 0% de lo ingestado al wiki — la regla "0% falsos positivos en el
wiki" se mantuvo, pero el pipeline de fetch está desperdiciando casi toda su
capacidad en contenido irrelevante.

1. ¿GitHub Actions corrió hoy? SÍ. Workflow "Wiki Agropecuario — Fetch Diario"
   corre diariamente y termina en success (última corrida: 2026-08-06 12:51 UTC).
   Sin embargo el último artículo REAL (no falso positivo) guardado en
   sources/ tiene saved_at 2026-07-30 — 7 días sin contenido nuevo aprovechable,
   por encima del umbral de 3 días de la métrica de éxito.

2. Ventanas GDELT: 62 completadas (por encima del umbral de 45), pero el
   conteo está inflado por un artefacto: la ventana final (iniciada en
   2026-06-18) genera una window_key nueva cada día porque su fecha de fin
   (`end = utcnow - 1 día`) avanza diariamente y el key incluye esa fecha
   (ver `fetch_gdelt_historical()` en scripts/fetch_news.py). Esto NO es
   agotamiento real del rango 2015→hoy (backfill histórico va llegando bien,
   ventanas trimestrales completas desde 2017-03 hasta 2026-06-17); es una
   ventana final que se re-consulta y re-registra cada día sin cerrar hasta
   cumplir 90 días. No requiere expansión de rango, pero sí sería más
   eficiente deduplicar por fecha de inicio de ventana en vez de por el
   par (inicio,fin) completo — queda como mejora futura, no urgente.

3. RSS/búsqueda web: causa raíz real identificada. La fuente `prensa_agro`
   (búsqueda DuckDuckGo con `site:prensa.com`) en `fetch_ddg_search()`
   (scripts/fetch_news.py) NO aplicaba el filtro `_is_panama_related()` que sí
   tienen el fetcher de RSS y el de GDELT. Como el filtro `site:` de DDGS no
   se respeta de forma confiable en el endpoint de noticias, la búsqueda
   devolvía artículos de agricultura de cualquier país (España/Aragón,
   Arabia Saudita, Brasil, Irán, Malasia, EE.UU.) etiquetados con
   `source: "prensa.com"`, muchos de ellos coincidiendo solo por la sigla
   "MIDA" (que también es una autoridad de Utah, EE.UU., y aparece en el
   ministerio malasio MITI/MARii). Esto explica el 100% de los falsos
   positivos de hoy y probablemente los 7 falsos positivos previos
   registrados en metrics.md.

FIX APLICADO: se agregó a `fetch_ddg_search()` el mismo filtro que ya usan
  RSS y GDELT — `_is_blocked_domain(url)` y `_is_panama_related(title, url)` —
  antes de aceptar un resultado. Archivo: scripts/fetch_news.py.
  Efecto esperado: la próxima corrida de GitHub Actions debería dejar de
  traer artículos no panameños desde la fuente `prensa_agro`.

BUGFIX ADICIONAL (ver entrada 16:10 arriba): `mark_ingested()` corregido para
  no romperse con la clave interna `_gdelt_windows`.

## 2026-08-06 16:55
DIAGNÓSTICO CONFIRMADO (logs reales de Actions run 31103200058, corrida de hoy):
  - GDELT: las 8 ventanas de 2015-2016 fallan con HTTP 403/429 (bloqueo real,
    no falta de datos) en cada corrida; también falló la ventana final
    (2026-06-18→2026-08-05) por acumulación de rate-limit en la misma corrida.
    ~5 de los ~6 minutos del step de fetch se gastan reintentando 2015-2016
    sin éxito antes de llegar a la ventana actual.
  - RSS: IICA y La Prensa devolvieron 0 entradas en el feed hoy.
  - DDG: 7 de 8 búsquedas configuradas (oirsa_alertas, mida_noticias,
    idiap_investigacion, bda_credito, fao_panama, banco_mundial_pa,
    iica_panama) devuelven "No results found" — nunca han aportado artículos.
    Solo `prensa_agro` devolvía resultados, y eran los falsos positivos ya
    corregidos hoy (fix en fetch_ddg_search(), ver entrada anterior).
  Ver wiki/metrics.md → "Progreso del Backfill GDELT" para el detalle completo
  y una recomendación de mejora futura (backoff más largo entre ventanas GDELT).
  No se aplicaron más cambios de código en esta sesión — queda como diagnóstico
  para una futura sesión de mantenimiento.
