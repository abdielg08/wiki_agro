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

## 2026-07-23 00:00
INGEST: 5 artículos revisados, 0 ingestados — 5/5 FALSOS POSITIVOS (rechazados, no se creó contenido de wiki)
  Todos etiquetados con source=prensa.com, country=PA, language=es, pero NINGUNO trata sobre agro de Panamá:
    - "MITI working on simplified NCM..." (paultan.org) → Malaysian Investment Development Authority (MIDA de Malasia, vía MITI/MARii)
    - "Timeline: Kevin O'Leary data center plan..." (sltrib.com) → Utah Military Installation Development Authority (MIDA de Utah, centro de datos)
    - "Box Elder data center opponents..." (sltrib.com) → misma MIDA de Utah, oposición local a centro de datos
    - "Utah Gov. Cox issues order..." (sltrib.com) → misma MIDA de Utah, calidad del aire/Great Salt Lake
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) → mención tangencial de MIDA de Utah en una demanda legal
  CAUSA RAÍZ identificada: `fetch_ddg_search()` en scripts/fetch_news.py (fuente `web_searches: prensa_agro`,
  query "... OR MIDA OR ..." con `site:prensa.com`) — el operador `site:` de DDGS no restringe realmente los
  resultados, y la función además hardcodea `source=site`, `language="es"`, `country="PA"` para TODO resultado
  sin verificar el dominio real. `is_agro_relevant()` solo exige coincidencia de keyword (sin AND de "Panamá"),
  a diferencia de `fetch_gdelt_batch()` que sí exige `(términos) AND (Panama OR Panamá OR ...)`.
  Esto es la MISMA clase de bug que causó los 7 falsos positivos de MIDA/Malasia documentados el 2026-06-22
  en metrics.md — el fix de GDELT no cubrió el pipeline de búsqueda DDG.
  RECOMENDACIÓN (no aplicada en esta sesión, requiere revisión de código fuera del alcance de la routine):
  1) eliminar "MIDA" como término aislado de `search_terms.primary` o exigir co-ocurrencia con "Panamá"/"Panama"
     en `is_agro_relevant()`, igual que ya hace `fetch_gdelt_batch()`;
  2) en `fetch_ddg_search()`, derivar `source`/`country`/`language` del dominio real de la URL en vez de
     hardcodearlos al del `site:` buscado.
  Artículos marcados `ingested: true` vía `mark-all-ingested` para no re-bloquear la cola de pendientes.

## 2026-07-23 08:10
BUG DETECTADO: `mark-all-ingested --limit 5` marcó como ingestados 3 artículos DISTINTOS a los 5 mostrados en
`pending_ingest.md` (que sí fueron revisados arriba). Causa: `ingest`/`run_prepare` selecciona por score de
prioridad (scripts/prioritize.py), mientras que `mark_all_ingested()` usa `find_pending()` (orden alfabético
por nombre de archivo) — ambos operan sobre el mismo pool de pendientes pero con criterios de orden distintos,
así que "marcar los primeros N pendientes" no corresponde a "los N que Claude acaba de leer".
  Artículos marcados a ciegas (nunca mostrados en pending_ingest.md, revisados retroactivamente en esta sesión):
    - "Utah wants to process uranium..." (sltrib.com) → MISMA MIDA de Utah (Military Installation Development
      Authority), nada de Panamá → FALSO POSITIVO, correctamente rechazado en retrospectiva.
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) → paper académico
      genérico sobre 6G/precision agriculture, sin mención de Panamá → FALSO POSITIVO.
    - "Catalogue of the diptera of the Americas South of United States" (archive.org, catálogo zoológico
      brasileño de 1966/67) → sin relación con Panamá → FALSO POSITIVO.
  Resultado: por suerte los 3 también eran falsos positivos, así que el estado final (ingested=true, sin
  contenido de wiki) es correcto, pero fue por casualidad — este bug PODRÍA marcar un artículo genuino como
  ingerido sin que Claude lo procese jamás, perdiéndolo silenciosamente del pipeline para siempre.
  RECOMENDACIÓN FUERTE: dejar de usar `mark-all-ingested` en las routines; usar únicamente los comandos
  `mark-ingested '<url>'` exactos que `pending_ingest.md` imprime al final, uno por artículo ya revisado.
  FIX APLICADO (menor, aislado): `mark_ingested()` en scripts/ingest.py crasheaba con
  `AttributeError: 'list' object has no attribute 'get'` en TODA invocación porque iteraba
  `processed.items()` sin filtrar la clave interna `_gdelt_windows` (una lista, no un dict) — a diferencia de
  `mark_all_ingested()` que sí usa `article_entries()`. Se corrigió para usar `article_entries(processed)`
  igual que la función plural. Esto bloqueaba por completo el marcado por URL individual.

## 2026-07-23 08:12
INGEST: 6 artículos adicionales revisados, 0 ingestados — 6/6 FALSOS POSITIVOS (marcados vía mark-ingested por URL)
    - "Box Elder data center opponents..." y "Utah Gov. Cox issues order..." → duplicados de MIDA-Utah ya
      documentados arriba, ahora marcados correctamente vía mark-ingested por URL exacta.
    - "MITI working on simplified NCM..." → duplicado de MIDA-Malasia ya documentado, marcado vía mark-ingested.
    - "The Persian Qanat" (whc.unesco.org) → sitio de Patrimonio Mundial UNESCO en Irán, agricultura de riego
      antigua persa — coincide con keyword "riego"/"agricultura" pero cero relación con Panamá.
    - "New York Farm Bureau" (nyfb.org) → organización agrícola del estado de Nueva York, EE.UU.
    - "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa) → programa agrícola de
      Arabia Saudita (trigo y cebada de secano), agencia de noticias oficial saudí — sin relación con Panamá.
  Total de la sesión: 11 artículos revisados, 0 ingestados, 11/11 falsos positivos (0% tasa de acierto del pool).
  Ninguno violó la regla de 0% falsos positivos EN EL WIKI (no se creó ninguna página incorrecta), pero señala
  que la fuente `web_searches.prensa_agro` (DDG) está devolviendo casi exclusivamente ruido — ver diagnóstico
  de causa raíz arriba (08:03).

## 2026-07-23 08:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
