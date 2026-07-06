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

## 2026-07-06 00:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-06 (sesión routine)
INGEST: 6 pendientes revisados — 0 reales, 6 falsos positivos (0 páginas nuevas)
  FALSOS POSITIVOS detectados (NO ingestados al wiki):
    - sltrib.com "Timeline: How the Kevin O'Leary data center plan..." (20260519) —
      "MIDA" = Military Installation Development Authority de Utah, no el MIDA de Panamá
    - sltrib.com "Box Elder data center opponents..." (20260527) — mismo MIDA de Utah
    - sltrib.com "Utah Gov. Cox issues order to protect Great Salt Lake..." (20260529) — mismo MIDA de Utah
    - sltrib.com "Utah wants to process uranium on the Wasatch Front..." (20250613) — mismo MIDA de Utah
    - spa.gov.sa "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (20260624) —
      agricultura real pero de Arabia Saudita, no de Panamá
    - nyfb.org "New York Farm Bureau" (20260617) — gremio agrícola de Nueva York, EE.UU.,
      no de Panamá. NOTA: no apareció en la vista previa de `pending_ingest.md` (limitada
      a 5 de los 6 pendientes) — se detectó al auditar `sources/processed.json` después de
      `mark-all-ingested --limit 5`, que sí lo marcó `ingested: true` al ser parte del cupo
      de 5 pendientes según el orden interno de `find_pending()`. Se verificó su texto
      completo (no menciona Panamá) antes de dejarlo documentado aquí — no se creó
      contenido de wiki para él en ningún momento.
  Ninguno de los 6 textos completos menciona "Panamá"/"Panama" (verificado programáticamente).
  Los 6 quedaron marcados `ingested: true` en processed.json (cola despejada) pero SIN
  página de wiki asociada, siguiendo la convención ya usada para los falsos positivos previos.

DIAGNÓSTICO — causa raíz encontrada y corregida:
  Los 6 artículos (y 7 falsos positivos previos: 3x thestar.com.my "MIDA"/Malasia,
  1x thestar.com.my "I-Bhd" sin relación, fox13now.com, worldbank.org genérico,
  ieeexplore.org — total acumulado ahora: 13) comparten el mismo origen:
  `fetch_ddg_search()` en scripts/fetch_news.py.
  Bug 1: la búsqueda `site:{site}` de DuckDuckGo (ddgs.news) no siempre respeta el
    filtro de sitio, y el código etiquetaba `source` con el sitio consultado
    ("prensa.com") sin verificar que la URL devuelta perteneciera realmente a ese dominio.
  Bug 2: `fetch_ddg_search()` y `fetch_world_bank()` solo llamaban a `is_agro_relevant()`
    (términos genéricos como "MIDA", "agricultura") y nunca a `_is_panama_related()` /
    `_is_blocked_domain()`, chequeos que `fetch_rss()` y `fetch_gdelt_batch()` ya
    aplicaban. Por eso coincidencias de sigla (MIDA de Utah/Malasia) o agricultura de
    otros países colaban sin el requisito de mención explícita a Panamá.
  FIX aplicado en scripts/fetch_news.py:
    - `fetch_ddg_search()`: ahora descarta resultados cuyo dominio no contenga el
      `site` consultado, aplica `_is_blocked_domain()`, y exige `_is_panama_related()`
      sobre título+cuerpo+URL antes de aceptar el artículo.
    - `fetch_world_bank()`: ahora también exige `_is_panama_related()`.
  Bug adicional (no relacionado a falsos positivos) corregido en scripts/ingest.py:
    `mark_ingested()` iteraba `processed.items()` sin filtrar la clave interna
    `_gdelt_windows` (una lista, no un dict de artículo), causando
    `AttributeError: 'list' object has no attribute 'get'` al marcar un artículo
    puntual. Ahora usa `article_entries()` como el resto del código.
  Pendientes de ingesta tras esta sesión: 0.

## 2026-07-06 00:07
LINT: 20 páginas revisadas, 55 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:12, no_index:1
