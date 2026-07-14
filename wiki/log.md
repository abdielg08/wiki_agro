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

## 2026-07-14 00:20
INGEST: 0 artículos reales ingeridos — 7 falsos positivos detectados y descartados
  Pendientes al inicio de sesión: 7
  Falsos positivos (NO ingestados al wiki; marcados `ingested: true` en processed.json solo para
  sacarlos de la cola de pendientes — no generan summaries/topics/entities):
    - "Box Elder data center opponents..." (sltrib.com) — MIDA = Military Installation Development
      Authority de Utah, EE.UU., NO el Ministerio de Desarrollo Agropecuario de Panamá
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) — mismo MIDA de Utah
    - "Timeline: Kevin O'Leary data center..." (sltrib.com) — mismo MIDA de Utah
    - "Utah wants to process uranium..." (sltrib.com) — Military Installation Development Authority (Utah)
    - "The Persian Qanat" (whc.unesco.org) — sistema de riego histórico de Irán, sin relación con Panamá
    - "New York Farm Bureau" (nyfb.org) — organización agrícola de EE.UU.
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa) — programa
      agrícola de Arabia Saudita
  Causa raíz identificada: ninguna de las 7 URLs pertenece al dominio prensa.com. La búsqueda DDG
  "site:prensa.com agropecuario OR ... OR MIDA OR ..." (config/sources.yaml → web_searches.prensa_agro)
  no está siendo honrada por `ddgs.news()` — el operador `site:` no filtra el dominio real de los
  resultados. Sumado a que `is_agro_relevant()` en scripts/fetch_news.py solo revisa palabras clave
  genéricas (incluida la sigla ambigua "MIDA") sin exigir mención de Panamá ni validar el dominio,
  cualquier noticia agrícola mundial que contenga esos términos se cuela como si fuera de prensa.com.
  Las 14 entradas con fuente "prensa.com" en sources/ (7 de la auditoría 2026-06-22 + 7 de hoy) son
  100% falsos positivos — ninguna es de prensa.com real.
  FIX aplicado (scripts/fetch_news.py, fetch_ddg_search): ahora descarta cualquier resultado cuyo
  dominio (urlparse(url).netloc) no contenga el `site` solicitado, antes de aceptar el artículo.
  Esto debería eliminar esta clase de falso positivo en la próxima corrida de GitHub Actions.
  FIX adicional (scripts/ingest.py, mark_ingested): bug preexistente — iteraba `processed.items()`
  sin excluir la clave interna `_gdelt_windows` (una lista), causando `AttributeError` en toda
  ejecución de `mark-ingested`. Corregido para usar `article_entries()`, igual que el resto del código.

## 2026-07-14 00:25
DIAGNÓSTICO: 4 días consecutivos sin artículos nuevos reales en sources/articles — ALERTA (supera el
máximo de 3 días definido en CLAUDE.md)
  Último archivo nuevo en sources/articles: 2026-07-10 (y resultó ser el falso positivo del Qanat).
  GitHub Actions (wiki_daily.yml) corrió: 07-11 (success, 0 artículos), 07-12 (success, 0 artículos),
  07-13 (failure — falla de infraestructura del runner en el paso "Set up job", ~4 min, no relacionada
  con el código del proyecto). La corrida de hoy 07-14 está programada para las 11:00 UTC y aún no corre.
  Causa de "0 artículos" en 07-11 y 07-12: TODAS las ventanas GDELT intentadas fallaron con
  "GET blocked (403/429)" o "Read timed out" / "Max retries exceeded" — incluye 9 ventanas históricas
  (2015-01-01 → 2017-03-29) que nunca se completaron y siguen reintentándose cada corrida, más la
  ventana más reciente (2026-06-18 → 2026-07-11). Ventanas GDELT ya completadas y en caché: 48
  (cobertura histórica 2017-03 → 2026-06). No es agotamiento de rango — GDELT está bloqueando o
  dando timeout a las IPs de GitHub Actions en cada corrida reciente.
  RSS: IICA (https://www.iica.int/es/rss/noticias) y LaPrensaGeneral (https://www.prensa.com/feed/)
  devolvieron 0 entradas en ambas corridas — feeds posiblemente vacíos, movidos o desactualizados.
  DDG búsquedas dirigidas por sitio oficial (oirsa.org, mida.gob.pa, idiap.gob.pa, bda.gob.pa,
  fao.org, bancomundial.org, iica.int) devolvieron "No results found" en las 7 — ddgs no encuentra
  nada al restringir a estos dominios institucionales.
  Acción tomada: fix de validación de dominio en fetch_ddg_search() (ver entrada INGEST arriba)
  para detener los falsos positivos de "prensa.com". El bloqueo/timeout de GDELT queda fuera del
  control del proyecto — si persiste 3+ corridas más, evaluar en próxima sesión: reducir frecuencia
  de requests a GDELT, aumentar el timeout, o rotar a un user-agent/IP diferente.
  RSS de IICA/La Prensa requieren revisión de URL en próxima sesión de mantenimiento.
