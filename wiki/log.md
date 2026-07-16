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

## 2026-07-16 00:00
INGEST: 5 artículos pendientes revisados — 5/5 FALSOS POSITIVOS, 0 ingestados
  Ninguno trata sobre agro panameño; ningún summary ni página de topics/entities creada:
    - "MITI working on simplified NCM..." (paultan.org) → MIDA de Malasia (Malaysian Investment Development Authority), no Panamá
    - "Box Elder data center opponents..." (sltrib.com) → MIDA de Utah (Military Installation Development Authority)
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) → misma MIDA de Utah
    - "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com) → misma MIDA de Utah
    - "Utah wants to process uranium..." (sltrib.com) → mención incidental de MIDA de Utah
  Causa raíz diagnosticada: scripts/fetch_news.py::fetch_ddg_search() (búsqueda DDG "prensa_agro",
    config/sources.yaml site: prensa.com) no aplicaba los filtros _is_blocked_domain() /
    _is_panama_related() que sí usan los fetchers de RSS y GDELT — el término "MIDA" en
    search_terms coincide con homónimos internacionales. Además el campo "source" se
    hardcodeaba al nombre de la búsqueda ("prensa.com") en vez del dominio real de la URL
    devuelta, ocultando que los artículos no venían de prensa.com.
  Corrección aplicada: fetch_ddg_search() ahora exige _is_panama_related(title, url),
    descarta _is_blocked_domain(url), y usa _url_domain(url) como "source" real.
  Artículos marcados como procesados (mark-ingested) para no re-encolarlos; pendientes: 4
  Tasa de falsos positivos de esta sesión: 5/5 (100%) — todos detectados y rechazados,
    0 incorporados al wiki. Cumple regla de 0% falsos positivos en el wiki.
  BUG adicional encontrado y corregido en scripts/ingest.py::mark_ingested(): iteraba
    processed.items() asumiendo que todo valor es dict, pero la clave de metadatos
    "_gdelt_windows" es una lista → AttributeError. Se agregó guard `isinstance(meta, dict)`.

## 2026-07-16 00:05
INGEST: 4 artículos pendientes revisados — 4/4 FALSOS POSITIVOS, 0 ingestados
  Mismo patrón de causa raíz (coincidencia genérica en "agricultura"/"agriculture" sin
    ningún término de Panamá):
    - "The Persian Qanat" (whc.unesco.org) → sistema de riego histórico de Irán
    - "New York Farm Bureau" (nyfb.org) → gremio agrícola de Nueva York, EE.UU.
    - "'Reef Saudi'..." (spa.gov.sa) → programa de agricultura de secano en Arabia Saudita
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org)
      → paper técnico IEEE sobre 6G/IoT, sin mención de Panamá
  Ninguno mencionaba Panamá, Chiriquí, Azuero ni ningún término de _PANAMA_TERMS —
    confirma que el fix en fetch_ddg_search() (commit de esta sesión) habría evitado
    que estos 4 entraran a la cola en primer lugar.
  0 summaries/topics/entities creados. Marcados como procesados (mark-ingested).
  Pendientes tras esta sesión: 0. Tasa de falsos positivos: 9/9 (100%) detectados,
    0% incorporados al wiki — regla de 0% falsos positivos cumplida.
