---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-16
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

## 2026-08-16 16:17
INGEST: 5 artículos revisados, 5 falsos positivos (0 ingestados al wiki)
  Ninguno de los 5 artículos del batch trata sobre agro panameño. Los 5
  fueron descartados y NO se creó contenido en wiki/summaries, topics/ ni
  entities/. Detalle:
    1. "MITI working on simplified NCM customised incentive mechanism..."
       (paultan.org, Malasia) — MITI/MARii son agencias malasias de
       incentivos industriales, sin relación con Panamá.
    2. "Timeline: How the Kevin O'Leary data center plan came to be..."
       (sltrib.com, Utah/EEUU) — "MIDA" aquí es la Military Installation
       Development Authority de Utah, no el Ministerio de Desarrollo
       Agropecuario de Panamá.
    3. "Box Elder data center opponents hope for a vote..." (sltrib.com,
       Utah/EEUU) — mismo MIDA de Utah (centro de datos, oposición local).
    4. "Utah Gov. Cox issues order to protect Great Salt Lake..."
       (sltrib.com, Utah/EEUU) — mismo MIDA de Utah.
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com) — menciona
       de pasada una demanda contra el MIDA de Utah; sin relación con
       Panamá ni agro.

  DIAGNÓSTICO DE CAUSA RAÍZ (5/5 falsos positivos en este batch):
  Los 5 artículos fueron ingeridos vía `fetch_ddg_search()` en
  `scripts/fetch_news.py` (búsqueda `web_searches: prensa_agro`,
  `config/*.yaml` línea ~159: `site: "prensa.com"`, query incluye el
  término "MIDA"). El operador `site:prensa.com` de DuckDuckGo NO está
  siendo respetado por el motor de búsqueda (los 5 resultados vienen de
  sltrib.com, paultan.org y msn.com — ningún dominio es prensa.com), y el
  código en `fetch_ddg_search()` (scripts/fetch_news.py ~línea 291-297)
  etiqueta cada resultado con `source: site` (hardcodeado a "prensa.com"),
  `country: "PA"` y `language: "es"` SIN verificar el dominio real del URL
  devuelto. El filtro `is_agro_relevant()` tampoco distingue el acrónimo
  "MIDA" panameño de sus homónimos (Utah Military Installation
  Development Authority; posible sigla malasia). Esto ya se había
  detectado una vez (ver wiki/metrics.md, auditoría 2026-06-22, 7 falsos
  positivos) y persiste sin corregirse en el pipeline.
  RECOMENDACIÓN (no aplicada en esta sesión — fuera del dominio wiki/ del
  LLM): en `fetch_ddg_search()`, validar que el dominio del URL devuelto
  coincida con `search_cfg["site"]` antes de aceptar el resultado, y/o
  excluir "MIDA" como término aislado de la query DDG (usar frases como
  "MIDA Panamá" en vez de "MIDA" solo).
  Artículos marcados `ingested=true` (revisados, no publicados) via
  `mark-all-ingested` para no bloquear la cola de pendientes.

## 2026-08-16 16:17
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-16 16:40
BUGFIX + INGEST: 11 falsos positivos adicionales detectados, 2 bugs de
herramientas corregidos, 0 artículos reales ingestados esta sesión.

  BUG 1 — `mark-all-ingested` marcaba los artículos equivocados:
  Se detectó que los 4 primeros falsos positivos documentados arriba
  (MITI, Kevin O'Leary, Box Elder, Utah Gov Cox) NO quedaron marcados
  `ingested=true` a pesar de que el log anterior lo reportaba. Causa:
  `ingest --limit N` selecciona artículos con `prioritize()` (orden por
  score), pero `mark-all-ingested --limit N` (scripts/ingest.py
  `mark_all_ingested`) usa `find_pending()` (orden por nombre de archivo,
  sin score) — ambos "top N" no son el mismo conjunto, así que
  `mark-all-ingested` marcó artículos distintos a los que realmente se
  revisaron. Como resultado, al ejecutar `ingest --limit 5` de nuevo,
  4 de los 5 "nuevos" artículos eran los mismos falsos positivos ya
  descartados. Corrección aplicada en esta sesión: se marcaron
  individualmente con `mark-ingested '<url>'` los 5 artículos
  correctamente revisados. `mark-all-ingested` sigue siendo no confiable
  para lotes — usar `mark-ingested` por URL hasta que se corrija.

  BUG 2 — `mark-ingested` fallaba con AttributeError:
  `scripts/ingest.py::mark_ingested()` iteraba `processed.items()`
  asumiendo que todos los valores son dict, pero `_gdelt_windows` es una
  lista → `'list' object has no attribute 'get'`. CORREGIDO en esta
  sesión: se agregó `if not isinstance(meta, dict): continue` antes de
  usar `meta.get(...)` (scripts/ingest.py, función `mark_ingested`).

  FALSOS POSITIVOS ADICIONALES (11, todos vía `fetch_ddg_search` /
  `web_searches: prensa_agro`, ninguno sobre agro panameño):
    - MITI/NCM (paultan.org, Malasia) — ya documentado arriba, ahora
      correctamente marcado `ingested=true`.
    - Kevin O'Leary data center timeline (sltrib.com, Utah) — ídem.
    - Box Elder data center opponents (sltrib.com, Utah) — ídem.
    - Utah Gov. Cox order (sltrib.com, Utah) — ídem.
    - "Arvensis Agro amplía sus instalaciones..." (heraldo.es, Aragón,
      España) — empresa de nutrición vegetal aragonesa, sin relación con
      Panamá.
    - "Reef Saudi" (spa.gov.sa, Arabia Saudita) — programa de agricultura
      de secano saudí.
    - "Finep vai pagar R$ 220 milhões..." (agenciabrasil.ebc.com.br,
      Brasil) — financiamiento a agricultura familiar brasileña.
    - "The Persian Qanat" (whc.unesco.org, Irán) — sistema de riego
      histórico iraní (patrimonio UNESCO).
    - "AEGA pide elecciones al campo en Aragón..." (heraldo.es, España).
    - "New York Farm Bureau" (nyfb.org, EEUU).
    - "Luis Biendicho asume la consejería de Medio Ambiente..."
      (heraldo.es, Aragón, España).
  Los 11 fueron revisados uno por uno (título, URL, dominio real y
  `summary_raw`), confirmados como no-Panamá, y marcados
  `ingested=true` sin crear contenido en wiki/. **16/16 artículos
  pendientes al inicio de esta sesión eran falsos positivos (100%)** —
  ninguno del backlog de `prensa_agro` era real.

  CAUSA RAÍZ CONFIRMADA Y CORREGIDA: a diferencia de `fetch_rss()`, que
  ya valida `_is_blocked_domain(url)` (scripts/fetch_news.py línea ~220),
  `fetch_ddg_search()` NO verificaba que el dominio del resultado
  coincidiera con `search_cfg["site"]` (p.ej. "prensa.com"), y el
  operador `site:` de DuckDuckGo resultó no ser confiable — devuelve
  resultados de dominios completamente distintos (sltrib.com,
  paultan.org, heraldo.es, spa.gov.sa, agenciabrasil.ebc.com.br,
  whc.unesco.org, nyfb.org) que igual pasaban el filtro de
  `is_agro_relevant()` por mencionar términos genéricos como
  "agricultura"/"agro". CORREGIDO en esta sesión: se agregó verificación
  de dominio (`site not in _url_domain(url)`) y `_is_blocked_domain(url)`
  en `fetch_ddg_search()` (scripts/fetch_news.py), replicando el patrón
  ya usado en `fetch_rss()`. Con este fix, ninguno de los 16 falsos
  positivos de esta sesión habría entrado a la cola de pendientes.

  DIAGNÓSTICO — 0 artículos nuevos reales desde 2026-07-30:
  El último commit con contenido real nuevo en `sources/` fue
  2026-07-30 (3 artículos). Desde entonces, 10+ corridas de GitHub
  Actions consecutivas (2026-08-02 → 2026-08-16) reportan "0 artículos
  nuevos" — muy por encima del umbral de alarma de 3 días de CLAUDE.md.
  GitHub Actions SÍ está corriendo (último commit en sources/: hoy,
  2026-08-16 11:18 UTC). `_gdelt_windows` en processed.json tiene 69
  ventanas completadas (≥45), lo que según CLAUDE.md indica que el rango
  de fechas GDELT está agotado y necesita expansión. Combinado con el fix
  de `fetch_ddg_search()` (que ahora rechazará los falsos positivos que
  antes sí entraban), es probable que el conteo de "artículos nuevos"
  baje aún más hasta que se expanda el rango de fechas GDELT o se
  agreguen fuentes nuevas. RECOMENDACIÓN: expandir `_gdelt_windows` /
  rango histórico en `scripts/fetch_historical.py`, y revisar si RSS de
  IICA/La Prensa sigue activo.
