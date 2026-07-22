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

## 2026-07-22 (routine automática)
INGEST: lote de 5 artículos pendientes revisado — 5/5 FALSOS POSITIVOS, 0 ingestados
  Causa raíz: colisión de la sigla "MIDA" — el fetch capta artículos que mencionan
  "MIDA" pero no se refieren al Ministerio de Desarrollo Agropecuario de Panamá.
  Artículos rechazados (no se creó contenido wiki para ninguno):
    1. "MITI working on simplified NCM..." (paultan.org) — MIDA = Malaysian
       Investment Development Authority (Malasia), no Panamá.
       https://paultan.org/2026/07/07/miti-working-on-simplified-ncm-customised-incentive-mechanism-to-build-real-local-industrial-capabilities/
    2. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) —
       MIDA = Military Installation Development Authority (Utah, EE.UU.).
       https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/
    3. "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com) —
       mismo MIDA de Utah (data centers), no agro panameño.
       https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/
    4. "Box Elder data center opponents..." (sltrib.com) — mismo MIDA de Utah.
       https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com) — menciona de
       pasada el MIDA de Utah; sin relación con agro panameño.
       https://www.msn.com/en-us/news/other/cultural-rules-for-staying-with-locals-abroad/ss-AA1QWARj?ocid=BingNewsVerp
  Acción: marcados como ingested=true (procesados/revisados) vía mark-ingested
  para que no queden pendientes indefinidamente; NINGUNO generó página de wiki.
  Recomendación: si el fetch usa "MIDA" como término de búsqueda genérico, agregar
  filtro de país (country=PA) o desambiguación por contexto ("Panamá", "agropecuario")
  para reducir la tasa de falsos positivos en próximas corridas.
  Pendientes tras esta corrida: 6 (de 24 descargados, 13 ingestados reales antes de
  esta sesión + 5 revisados como falsos positivos en esta sesión = 18 procesados).

## 2026-07-22 00:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-22 (continuación — routine automática)
BUGFIX: `mark_ingested()` en scripts/ingest.py fallaba con AttributeError al
  iterar `processed.items()`, porque `sources/processed.json` contiene claves
  internas no-artículo (p.ej. `_gdelt_windows`) cuyo valor es una lista, no un
  dict, y el código llamaba `meta.get("path", "")` sin filtrarlas. Corregido
  para iterar sobre `article_entries(processed)` (ya excluye claves `_meta`),
  igual que ya hacía `mark_all_ingested`. Sin este fix, `mark-ingested` era
  inutilizable para cualquier processed.json con claves internas.

HALLAZGO ADICIONAL: `mark-all-ingested --limit 5` no marca necesariamente los
  mismos artículos que mostró la última corrida de `ingest --limit 5` — vuelve
  a calcular "pendientes" en el momento de la llamada, ordenados por nombre de
  archivo. Como el fetch automático (GitHub Actions) agregó artículos nuevos
  de backfill histórico (fechas 2016 y 2025) a mitad de esta sesión, la
  primera llamada a `mark-all-ingested` marcó 3 artículos NO revisados en vez
  de 3 de los 5 revisados en el lote original. Se identificaron y revisaron
  esos 3 artículos a posteriori (ver abajo) — también resultaron ser falsos
  positivos, así que no hubo impacto en la tasa de falsos positivos, pero es
  un riesgo real: si hubieran sido artículos legítimos de agro panameño,
  habrían quedado marcados `ingested=true` SIN contenido en el wiki. Recomendación:
  usar `mark-ingested <url>` por artículo (ya corregido arriba) en vez de
  `mark-all-ingested` cuando pueda haber fetches concurrentes.

INGEST: revisión completa de los 11 artículos que estaban pendientes al inicio
  de esta sesión (incluyendo los que aparecieron por el hallazgo anterior).
  RESULTADO: 11/11 FALSOS POSITIVOS — 0 páginas de wiki creadas o actualizadas
  esta sesión. Todos marcados `ingested=true` (revisados) tras confirmar que
  ninguno trata sobre agro panameño:
    6. "Catalogue of the diptera of the Americas South of United States" (archive.org,
       1966/67, Secretaria da Agricultura de Brasil) — catálogo taxonómico histórico,
       no noticia de agro panameño. https://archive.org/details/Cataloguedipter2SaoP
    7. "Ambient IoT: Communications Enabling Precision Agriculture" (IEEE, paper
       técnico 6G/IoT genérico) — no menciona Panamá. https://ieeexplore.ieee.org/document/10945742
    8. "Utah wants to process uranium... nuclear energy" (sltrib.com) — mismo
       MIDA de Utah (Military Installation Development Authority), no agro.
       https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/
    9. "New York Farm Bureau" (nyfb.org) — gremio agrícola de EE.UU., no Panamá.
       https://www.nyfb.org/
    10. "The Persian Qanat" (whc.unesco.org) — patrimonio UNESCO de Irán, no Panamá.
        https://whc.unesco.org/en/list/1506
    11. "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture" (spa.gov.sa) —
        programa agrícola de Arabia Saudita, no Panamá.
        https://www.spa.gov.sa/en/N2096157
  (Los otros 5 falsos positivos de este lote — MITI/Malasia, Utah Gov Cox,
  Kevin O'Leary timeline, Box Elder, Cultural Rules Abroad — ya están
  documentados en la entrada anterior de este mismo día.)
  Pendientes tras esta corrida: 0 (24 descargados, 24 ingestados/revisados).
  Falsos positivos acumulados en esta sesión: 11 — ninguno se reflejó como
  contenido en el wiki (tasa de falsos positivos publicados = 0%, cumpliendo
  la regla no-negociable de CLAUDE.md).
  DIAGNÓSTICO GENERAL: la fuente `prensa.com` (RSS/búsqueda genérica) está
  produciendo casi exclusivamente falsos positivos por colisión de palabras
  clave ("MIDA", "agriculture") sin filtro geográfico. De 18 artículos con
  fuente="prensa.com" en sources/, la gran mayoría revisados hasta ahora no
  son sobre Panamá. Recomendación para el fetch: restringir o ponderar más
  bajo la fuente prensa.com, o agregar verificación de país/contexto Panamá
  antes de guardar el artículo en sources/articles/.
