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

## 2026-07-27 (routine)
INGEST: 11 artículos revisados — 11/11 falsos positivos (0 páginas nuevas, 0% falsos positivos ingestados al wiki)
  Todos los pendientes acumulados resultaron ser falsos positivos del fetcher DDG:
    - paultan.org — "MITI working on... NCM..." (incentivos industriales de Malasia, MIDA=Malaysian Investment Development Authority)
    - sltrib.com — "Kevin O'Leary data center timeline" (Utah, MIDA=Utah Military Installation Development Authority)
    - sltrib.com — "Box Elder data center opponents" (Utah, ídem)
    - sltrib.com — "Utah Gov. Cox issues order..." (Utah, ídem)
    - sltrib.com — "Utah wants to process uranium..." (Utah, ídem)
    - msn.com — "Cultural Rules For Staying With Locals Abroad" (genérico, sin mención de Panamá)
    - ieeexplore.ieee.org — "Ambient IoT: Precision Agriculture" (paper técnico 6G global, sin Panamá)
    - archive.org — "Catalogue of the diptera..." (catálogo zoológico histórico, Secretaria da Agricultura de Brasil)
    - nyfb.org — "New York Farm Bureau" (EE.UU.)
    - spa.gov.sa — "'Reef Saudi' rain-fed agriculture" (Arabia Saudita)
    - whc.unesco.org — "The Persian Qanat" (Irán)
  Ninguno menciona Panamá. Ninguno se ingestó al wiki (sin summaries/topics/entities creados).
  Notificado al usuario: 11/11 artículos pendientes eran falsos positivos.

FIX (código) scripts/fetch_news.py: fetch_ddg_search() no aplicaba los filtros
  _is_blocked_domain()/_is_panama_related() que sí usan fetch_rss() y las
  funciones GDELT — por eso el término genérico "MIDA" (parte de search_terms.primary)
  colaba resultados de Malasia/Utah bajo la etiqueta "prensa.com" pese a que DDG
  no siempre respeta el operador "site:". Agregados ambos filtros; "source" ahora
  usa el dominio real de la URL en vez del label de config de búsqueda.

FIX (código) scripts/ingest.py: mark_ingested(url) crasheaba con
  `AttributeError: 'list' object has no attribute 'get'` al iterar processed.json
  porque no excluía la clave interna "_gdelt_windows" (es una lista, no un dict de
  metadata). Ahora usa article_entries() igual que mark_all_ingested().

INCIDENTE DE PROCESO: `mark-all-ingested --limit 5` selecciona por orden de archivo
  (sorted glob), mientras que `ingest --limit 5` selecciona por score de relevancia
  (prioritize.py) — no es garantizado que sea el mismo lote de 5. En esta sesión
  eso marcó como ingestados 3 artículos que no habían sido revisados en el momento
  (Utah nuclear energy, IEEE Ambient IoT, catálogo diptera de archive.org); se
  verificaron a posteriori y también resultaron ser falsos positivos, así que no
  hubo pérdida de artículos legítimos, pero fue por suerte, no por diseño.
  Recomendación: usar siempre `mark-ingested <url>` por artículo (como indican los
  comandos al final de pending_ingest.md) en vez de `mark-all-ingested --limit N`.

DIAGNÓSTICO AVANZADO (Paso 4, con logs reales de GitHub Actions — run 30201051693, 2026-07-26):
  - RSS IICA y LaPrensaGeneral: "0 entradas en el feed" — feeds vacíos o rotos.
  - DDG: 7 de 8 búsquedas configuradas devuelven "No results found"
    (oirsa_alertas, mida_noticias, idiap_investigacion, bda_credito, fao_panama,
    banco_mundial_pa, iica_panama). Solo "prensa_agro" devuelve resultados, y
    hasta hoy eran 100% falsos positivos (ver arriba y fix aplicado).
  - GDELT: las 9 ventanas históricas más antiguas (2015-01-01 → 2017-03-29) reciben
    "GET blocked (403/429)" en cada corrida — confirmado bloqueo real de GDELT,
    no es un problema de rango de fechas como se sospechaba en la nota de
    2026-06-22 de metrics.md.
  - GDELT ventana "actual" (ej. 2026-06-18 → 2026-07-25 en la corrida del 26): responde
    200 OK pero 0 artículos.
  - BUG (código, sin corregir aún): en fetch_gdelt_historical() (scripts/fetch_news.py),
    `end = min(config_end, utcnow()-1día)` se usa tanto para acotar el rango como
    para la CLAVE de la ventana "actual" → la clave cambia cada día
    (20260618_20260623, 20260618_20260624, 20260618_20260627, ...) y esa ventana
    nunca se marca "completa" de forma estable: se re-escanea casi el mismo rango
    cada día sin avanzar. 19 de las 56 "ventanas completadas" registradas son
    variantes redundantes de este patrón. Recomendación: usar límites de trimestre
    fijos (independientes de "hoy") para la clave, como ya hace
    scripts/fetch_historical.py, y sólo acotar el RANGO de fetch por "ayer".
  - Últimos 7 días consecutivos (2026-07-21 → 2026-07-27): 0 artículos nuevos reales
    en sources/ — supera el umbral de 3 días de falla definido en CLAUDE.md.
  - Backfill histórico 2015–2017 Q1 (9 trimestres) sigue sin completar por el
    bloqueo de GDELT.
  Acción tomada: 2 bugs de código corregidos (ddg filters, mark_ingested). El
  bloqueo de GDELT y las búsquedas DDG rotas para dominios .gob.pa requieren
  investigación adicional (posible rate-limit por IP compartida de GitHub Actions,
  o cambio en la API de GDELT/DDG) — no se intentó arreglar en esta sesión por no
  poder reproducir contra las APIs reales desde este entorno (proxy de red bloqueado).

## 2026-07-27 08:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
