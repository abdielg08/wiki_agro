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

## 2026-08-17 16:15
INGEST: 5 artículos revisados, 5 falsos positivos (0 ingestados) — sesión Claude Code
  Causa raíz: colisión de la sigla "MIDA" — el pipeline de fetch (prensa.com/GDELT)
  está capturando artículos en inglés que mencionan otras entidades llamadas MIDA
  (Malaysian Investment Development Authority en Malasia; Military Installation
  Development Authority en Utah, EE.UU.), no el Ministerio de Desarrollo
  Agropecuario de Panamá. Ninguno trata sobre agro panameño — NO se ingestó ninguno.
  Falsos positivos:
    - "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, 2026-07-08)
      → MIDA = Malaysian Investment Development Authority (agencia de inversión de Malasia)
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19)
      → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    - "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27)
      → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
      → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    - "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07)
      → menciona de pasada la Military Installation Development Authority (Utah)
  Recomendación: el fetch etiqueta estos artículos con country=PA incorrectamente;
  revisar el filtro de país/keyword en el fetch de GDELT/prensa.com para excluir
  resultados donde "MIDA" no vaya acompañado de contexto agropecuario panameño.
  Se marcarán como ingested=true (vía mark-all-ingested) para no re-procesarlos,
  sin crear páginas de wiki asociadas.

## 2026-08-17 16:16
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-17 16:18
INGEST: 7 artículos adicionales revisados, 7 falsos positivos (0 ingestados) — sesión Claude Code
  Todos con source="prensa.com", country="PA" (etiqueta incorrecta). Ninguno menciona
  Panamá en el texto completo. Verificado por grep de "panama"/"panamá" en full_text +
  summary_raw de los 7 archivos.
  Falsos positivos:
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa, 2026-06-24) — Arabia Saudita
    - "New York Farm Bureau" (nyfb.org, 2026-06-17) — EE.UU.
    - "The Persian Qanat" (whc.unesco.org, 2026-07-07) — Irán, patrimonio UNESCO
    - "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es, 2026-05-03) — Aragón, España
    - "AEGA pide elecciones al campo en Aragón..." (heraldo.es, 2026-06-08) — Aragón, España
    - "Finep vai pagar R$ 220 milhões para inovações em agricultura familiar" (agenciabrasil.ebc.com.br, 2026-07-02) — Brasil
    - "Arvensis Agro amplía sus instalaciones..." (heraldo.es, 2026-06-23) — Aragón, España
  Con esto, pendientes = 0 (29/29 artículos marcados). De los 29 descargados,
  solo 6 tienen contenido real sobre agro panameño (los de la semilla manual
  del 2026-05-24); los 23 restantes con source="prensa.com" son, sin excepción,
  falsos positivos.

## 2026-08-17 16:20
FIX: causa raíz de los falsos positivos identificada y corregida
  Diagnóstico: scripts/fetch_news.py::fetch_ddg_search() construye la query
  como "site:prensa.com {query}" para DDGS().news(), pero la librería `ddgs`
  no respeta de forma confiable el operador "site:" — devuelve resultados de
  cualquier dominio mundial que contenga términos agro genéricos. El código
  etiquetaba cada resultado con source="prensa.com" y country="PA" sin
  verificar el dominio real de la URL devuelta (scripts/fetch_news.py, antes
  líneas ~292-299). Esto viene contaminando sources/articles/ desde al menos
  2025-03-31 (23/23 artículos con source="prensa.com" son falsos positivos,
  incluyendo confusiones con "MIDA" = Malaysian Investment Development
  Authority y Utah's Military Installation Development Authority).
  Fix: se agregó verificación de dominio (urlparse(url).netloc vs `site`)
  en fetch_ddg_search() — descarta cualquier resultado cuyo dominio real no
  coincida con el sitio configurado antes de aceptarlo.
  Fix adicional: scripts/ingest.py::mark_ingested() crasheaba con
  AttributeError porque iteraba processed.items() sin excluir la clave
  interna "_gdelt_windows" (una lista, no dict) — ahora usa
  article_entries(processed), igual que mark_all_ingested().
  Bug documentado sin corregir: mark_all_ingested(limit=N) usa find_pending()
  (orden alfabético por archivo) mientras que `ingest` usa prioritize()
  (orden por score) para elegir qué mostrar — los conjuntos de N artículos
  pueden no coincidir. Recomendación: usar `mark-ingested <url>` por artículo
  en vez de `mark-all-ingested` hasta que se unifique el criterio de orden.
  Pendiente: validar en la próxima corrida de GitHub Actions que ya no
  entren artículos no-panameños vía DDG.
