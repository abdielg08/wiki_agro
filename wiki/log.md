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

## 2026-08-13 08:19
FALSOS POSITIVOS: 5/5 artículos de la cola de ingesta descartados (0% falsos positivos ingestados)
  Causa raíz: colisión de la sigla "MIDA" — el fetcher (GDELT/RSS) capturó artículos de
  prensa.com que mencionan "MIDA" pero refiriéndose a entidades homónimas no panameñas,
  no al Ministerio de Desarrollo Agropecuario de Panamá. Ninguno de los 5 textos menciona
  "Panamá" en ningún punto (verificado programáticamente).
  Artículos descartados:
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, Malasia)
      → MIDA = agencia malaya bajo MITI/MARii, no relacionada con agro panameño
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, Utah)
      → MIDA = Military Installation Development Authority (Utah), centros de datos
    - "Box Elder data center opponents hope for a vote..." (sltrib.com, Utah)
      → mismo MIDA de Utah (data centers), no agro
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, Utah)
      → mismo MIDA de Utah, calidad del aire/agua, no agro panameño
    - "Cultural Rules For Staying With Locals Abroad" (msn.com)
      → menciona litigio contra "MIDA" de Utah; artículo de viajes, sin relación agro
  Acción: NO se creó contenido en wiki/. Los 5 artículos se marcaron como ingestados
  (mark-all-ingested) para limpiar la cola sin contaminar el wiki.
  Recomendación: si estos falsos positivos se repiten, considerar afinar el prioritizador/
  fetcher para exigir coincidencia de "Panamá"/"agropecuario" además de la sigla "MIDA".

## 2026-08-13 08:19
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-13 08:35
BUG DETECTADO Y CORREGIDO: `mark-all-ingested` marcaba artículos incorrectos
  Causa: `ingest --limit N` selecciona artículos por score de prioridad
  (`prioritize()`), pero `mark_all_ingested()` usaba `find_pending()` en
  orden alfabético de archivo — un slice completamente distinto. El primer
  `mark-all-ingested --limit 5` de esta sesión marcó 5 artículos que
  Claude NUNCA revisó (en vez de los 5 falsos positivos reales mostrados
  en pending_ingest.md), dejando 4 de los verdaderos falsos positivos
  todavía pendientes (reaparecieron en el siguiente `ingest --limit 5`).
  Artículos marcados por error, verificados ahora como falsos positivos
  también (ninguno menciona Panamá — verificado programáticamente):
    - "Utah wants to process uranium on the Wasatch Front..." (sltrib.com) — MIDA=Military Installation Development Authority (Utah)
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) — paper técnico 6G genérico, sin relación con Panamá
    - "Catalogue of the diptera of the Americas South of United States" (archive.org) — catálogo entomológico histórico, no noticia agro-Panamá
    - "Aragón celebra la sentencia del Supremo que tumba ampliación..." (heraldo.es) — granjas porcinas en Aragón, España, no Panamá
  Corrección aplicada:
    1. Fix en `scripts/ingest.py::mark_ingested()` — crasheaba con
       `AttributeError` al iterar `processed.items()` sin filtrar la
       clave especial `_gdelt_windows` (una lista, no un dict). Ahora usa
       `article_entries()` como el resto del código.
    2. Fix en `scripts/ingest.py::mark_all_ingested()` — ahora usa
       `prioritize()` con la misma estrategia que `run_prepare()`, para
       marcar exactamente los artículos que Claude vio en pending_ingest.md.
    3. Se marcaron manualmente (vía `mark-ingested <url>` ya corregido) los
       4 falsos positivos de la primera tanda que seguían pendientes:
       paultan.org (MITI/Malasia), sltrib.com ×2 (Kevin O'Leary, Box Elder,
       data centers de Utah), sltrib.com (gobernador de Utah, Great Salt Lake).
  Impacto en 0% falsos positivos: NINGUNO llegó al wiki — todos los
  artículos afectados eran, en efecto, falsos positivos (verificado
  individualmente). El bug solo afectaba el orden de marcado en la cola,
  no la calidad del contenido publicado.

## 2026-08-13 08:36
FALSOS POSITIVOS: 1/1 artículo adicional descartado (tanda 2 de ingest --limit 5)
  - "Arvensis Agro amplía sus instalaciones..." (heraldo.es) — empresa
    aragonesa (España) de nutrición vegetal; no relacionada con Panamá.
    Los otros 4 artículos de esta tanda eran duplicados de los falsos
    positivos de MIDA/Utah ya documentados arriba.
  Acción: marcado como ingestado sin crear contenido en wiki/.

## 2026-08-13 08:45
CAUSA RAÍZ ENCONTRADA Y CORREGIDA: fetcher de búsqueda web (`prensa_agro`)
  no filtraba por dominio ni por mención de Panamá
  Tanda 3 de `ingest --limit 5` trajo 5/5 falsos positivos más, ninguno
  relacionado con Panamá: "Reef Saudi" (spa.gov.sa, Arabia Saudita),
  Finep/agricultura familiar (agenciabrasil.ebc.com.br, Brasil), "The
  Persian Qanat" (whc.unesco.org, Irán/UNESCO), AEGA Aragón
  (heraldo.es, España), New York Farm Bureau (nyfb.org, EE.UU.).
  Total: 16/16 artículos de la cola de ingesta de esta sesión eran
  falsos positivos (0 ingestados al wiki, 0% falsos positivos publicados).
  Investigación de causa raíz (`config/sources.yaml` + `scripts/fetch_news.py`):
    - La búsqueda web `prensa_agro` usa DuckDuckGo (`ddgs.news()`) con
      `site:prensa.com agropecuario OR agricultura OR ganadería OR MIDA
      OR cosecha Panamá`, pero el operador `site:` NO es respetado por el
      endpoint de noticias de `ddgs` — llegaron resultados de dominios
      completamente ajenos (paultan.org, sltrib.com, msn.com, archive.org,
      ieeexplore.ieee.org, spa.gov.sa, ebc.com.br, unesco.org, heraldo.es,
      nyfb.org), todos etiquetados incorrectamente con `source: prensa.com`.
    - `is_agro_relevant()` solo exige que aparezca UN término genérico
      (p.ej. "MIDA", "agricultura", "sequía", "riego") en cualquier parte
      del título/cuerpo — sin exigir mención de Panamá. Como "MIDA" es
      también la sigla de "Military Installation Development Authority"
      (Utah) y de una agencia malaya, y "agricultura"/"sequía" son
      términos genéricos usados en noticias de cualquier país, la
      búsqueda global sin restricción de dominio real capturó ruido de
      todo el mundo.
  Corrección aplicada en `scripts/fetch_news.py::fetch_ddg_search()`:
    1. Verificar que el dominio real de la URL del resultado contenga el
       `site` solicitado (`urlparse(url).netloc`) — descarta resultados
       fuera de dominio en vez de confiar en el operador `site:` de DDG.
    2. Exigir mención explícita de "panama"/"panamá" en título+cuerpo
       además de un término agro — cierra el hueco de colisión de siglas
       (MIDA) y de relevancia genérica sin especificidad panameña.
  Con este fix, futuros `fetch` deberían dejar de encolar estos falsos
  positivos. Se recomienda observar la próxima corrida de GitHub Actions
  para confirmar que `prensa_agro` deja de aportar ruido.

## 2026-08-13 08:50
FALSOS POSITIVOS: 1/1 artículo final descartado — cola de ingesta vaciada
  - "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es,
    Aragón, España) — nombramiento político regional español, sin relación
    con Panamá ni con el sector agropecuario panameño.
  Resultado de la sesión: 17/17 artículos de la cola eran falsos positivos
  (0 ingestados al wiki — 0% falsos positivos publicados, cumpliendo la
  métrica innegociable). Pendientes de ingesta = 0.
