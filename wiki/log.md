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

## 2026-07-29 00:04
FALSOS POSITIVOS: 5/5 artículos del lote de ingesta (`ingest --limit 5`) rechazados — 0% ingestados, 100% falsos positivos
  - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, 2026-07-08) → MIDA = Malaysian Investment Development Authority
  - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19) → MIDA = Military Installation Development Authority (Utah)
  - "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27) → MIDA = Military Installation Development Authority (Utah)
  - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29) → MIDA = Military Installation Development Authority (Utah)
  - "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07) → menciona MIDA de Utah de pasada, sin relación con Panamá
  Ninguno trata sobre agro panameño. No se creó ningún summary/topic/entity para estos artículos.
  CAUSA RAÍZ (diagnosticada y corregida en este mismo commit):
    `scripts/fetch_news.py::fetch_ddg_search()` (fuente DDG "prensa.com", usada por `wiki_agro.py ingest`)
    no aplicaba los guards `_is_blocked_domain()` / `_is_panama_related()` que sí usan `fetch_rss()`
    y el path histórico de GDELT. Como "MIDA" está en `search_terms.primary` (config/sources.yaml)
    y `is_agro_relevant()` es un simple OR de substring, cualquier noticia global que mencione
    "MIDA" (Malasia, Utah) pasaba el filtro sin verificar mención de Panamá. Además el operador
    `site:prensa.com` de la búsqueda DDG no restringía de forma confiable el dominio — los 5
    resultados vinieron de paultan.org, sltrib.com y msn.com, no de prensa.com.
  FIX: se agregó `_is_blocked_domain(url)` + `_is_panama_related(title, url)` a `fetch_ddg_search()`,
    igual que en `fetch_rss()`. Los 5 artículos se marcan como ingested=true (procesados/descartados)
    para no bloquear la cola de pendientes ni disparar la alerta de "pendiente >1 día sin procesar".
  RECOMENDACIÓN: revisar `fetch_world_bank()` (mismo módulo) — usa `is_agro_relevant()` sin los
    mismos guards; no se modificó en esta sesión por falta de evidencia de falsos positivos ahí.

## 2026-07-29 00:20
FALSOS POSITIVOS: 6/6 artículos del segundo lote (`ingest --limit 6`) rechazados — 0% ingestados
  - "Utah wants to process uranium..." (sltrib.com, 2025-06-13) → MIDA = Military Installation Development Authority (Utah), otra vez
  - "New York Farm Bureau" (nyfb.org, 2026-06-17) → agricultura de EE.UU., sin relación con Panamá
  - "'Reef Saudi'..." (spa.gov.sa, 2026-06-24) → programa agrícola de Arabia Saudita
  - "The Persian Qanat" (whc.unesco.org, 2026-07-07) → sitio patrimonio UNESCO de Irán
  - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org, 2025-03-31) →
    paper técnico genérico sobre agricultura de precisión 6G, sin mención de Panamá
  - "Catalogue of the diptera of the Americas..." (archive.org, 2016-05-13) → catálogo entomológico
    de Brasil (Secretaria da Agricultura), sin relación con Panamá
  Ninguno trata sobre agro panameño. No se creó ningún summary/topic/entity. Confirma el diagnóstico
  anterior: la fuente DDG "prensa.com" (18/24 artículos descargados hasta ahora) no restringe por
  dominio ni por Panamá — devuelve contenido agrícola genérico en inglés de cualquier país. Con el
  fix de esta sesión (`_is_blocked_domain` + `_is_panama_related` en `fetch_ddg_search()`), este tipo
  de resultado debería dejar de descargarse en fetches futuros. Se marcan como ingested=true (procesados
  y descartados) para despejar la cola de pendientes.
  TOTAL DE LA SESIÓN: 11/11 artículos pendientes eran falsos positivos (0 ingestados al wiki).
    0% falsos positivos incorporados al wiki (regla innegociable respetada) — pero 0 artículos
    nuevos de contenido real esta sesión. Ver diagnóstico avanzado más abajo.

## 2026-07-29 00:35
DIAGNÓSTICO AVANZADO: pendientes=0 tras esta sesión → se investigó por qué no llega contenido real
  1. GitHub Actions corrió: sí, commits diarios `chore(sources): N artículos...` hasta 2026-07-28
     (cron 6am hora Panamá). Aún no hay commit para 2026-07-29 al momento de esta sesión.
  2. Ventanas GDELT completadas (`_gdelt_windows` en sources/processed.json): 57.
     Según el umbral de CLAUDE.md (45+), el rango configurado (2015-01-01 → hoy, clamp a ayer)
     está agotado — el backfill histórico vía GDELT ya cubrió todo el rango disponible.
     A partir de ahora solo se abre ~1 ventana nueva cada ~90 días conforme avanza la fecha real;
     0 artículos nuevos de GDELT es el comportamiento ESPERADO en el día a día, no una falla.
  3. Auditoría completa de origen de los 18 artículos con `source=prensa.com` (todos los
     descargados desde la semilla del 2026-05-24, ver `git log -- sources/`):
     TODOS los 18 —sin excepción— vinieron de `fetch_ddg_search()` (búsqueda DuckDuckGo
     configurada como "prensa.com" en config/sources.yaml) y TODOS resultaron ser falsos
     positivos (7 documentados en auditoría previa del 2026-06-22 + 11 en esta sesión).
     Es decir: en más de 2 meses de corridas diarias de GitHub Actions (2026-05-26 → 2026-07-28),
     CERO artículos reales sobre agro panameño han entrado al pipeline — el 100% del volumen
     "nuevo" era ruido de la fuente DDG rota.
  CAUSA RAÍZ CONFIRMADA Y CORREGIDA (ver commit de esta sesión): `fetch_ddg_search()` no
     aplicaba los guards de dominio/Panamá que sí tienen `fetch_rss()` y GDELT. Fix aplicado.
  IMPACTO ESPERADO DEL FIX: las próximas corridas de Actions deberían mostrar 0 (o muy pocos)
     "artículos nuevos" del origen DDG, ya que el filtro ahora exige mención de Panamá — esto es
     una MEJORA (menos ruido), no una regresión, aunque el conteo bruto de "artículos nuevos/día"
     baje. Si tras 3-5 días el conteo de DDG sigue en 0, revisar si `ddgs.news()` realmente honra
     `site:prensa.com` o si conviene reemplazar esa fuente por el RSS directo de prensa.com
     (`config/sources.yaml` ya tiene `rss: "https://www.prensa.com/feed/"` configurado aparte).
  4. RSS (IICA, La Prensa): esta sesión de Claude Code no tiene acceso de red saliente a esos
     dominios (política de red del entorno) — no se pudo verificar en vivo. Solo GitHub Actions
     (IPs no bloqueadas) puede confirmar si los feeds responden. Pendiente de verificar en la
     próxima corrida de Actions si `rss` de La Prensa/IICA está aportando artículos reales.
  RECOMENDACIÓN PRIORITARIA: ejecutar manualmente `wiki_historical.yml` (crawl histórico GDELT
     con `--years` ampliado o `--mode rss/sitemap`) para reactivar ingesta real, ya que el fetch
     diario normal ha estado efectivamente vacío desde la semilla inicial.
