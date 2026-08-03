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

## 2026-08-03 08:04
FALSOS POSITIVOS: 5/5 artículos del lote `ingest --limit 5` rechazados — 0% ingestados al wiki
  Causa raíz: colisión de la sigla "MIDA" — el fetch capturó noticias que mencionan
  "MIDA" pero de organizaciones sin relación con Panamá:
    - MITI/MARii Malasia (Malaysian Investment Development Authority) — mecanismo NCM de incentivos industriales
    - MIDA Utah, EE.UU. (Military Installation Development Authority) — data center de Kevin O'Leary en Box Elder
      County (3 artículos: timeline, oposición vecinal, orden del gobernador Cox sobre calidad del aire/Great Salt Lake)
    - Artículo sobre normas culturales para hospedarse con locales en el extranjero (menciona la demanda contra MIDA Utah)
  Ninguno trata sobre el Ministerio de Desarrollo Agropecuario de Panamá ni sobre agro panameño.
  Artículos (todos etiquetados incorrectamente con fuente "prensa.com" pero de dominios
  paultan.org, sltrib.com y msn.com):
    - 20260708_prensacom_2026-07-07-miti-working-on-simplified-ncm-customised-incenti.json
    - 20260519_prensacom_news-2026-05-19-kevin-oleary-data-center-timeline.json
    - 20260527_prensacom_news-2026-05-27-box-elder-data-center-opponents.json
    - 20260529_prensacom_news-environment-2026-05-29-utah-governor-issues-order-prote.json
    - 20260307_prensacom_en-us-news-other-cultural-rules-for-staying-with-locals-abro.json
  Acción: NO se creó contenido en wiki/summaries|topics|entities para estos artículos.
  Se marcarán como `ingested: true` (revisados y descartados) vía mark-all-ingested para
  liberar la cola sin re-presentarlos, preservando 0% falsos positivos en el wiki.
  Recomendación al usuario: el fetch/scoring debería excluir coincidencias de "MIDA" en
  dominios fuera de Panamá (paultan.org, sltrib.com, msn.com) o exigir co-ocurrencia con
  términos como "Panamá", "agropecuario", "agrícola" para reducir este tipo de colisión.

## 2026-08-03 08:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-03 08:20
BUG DE HERRAMIENTA DETECTADO Y CORREGIDO: `mark-all-ingested --limit N` no respeta el
mismo orden que `ingest --limit N`. `ingest` selecciona por score de prioridad
(scripts/prioritize.py), pero `mark-all-ingested` usa `find_pending()`, que ordena por
nombre de archivo alfabético (`sorted(SOURCES_DIR.glob("*.json"))`). Resultado: el
`mark-all-ingested --limit 5` ejecutado tras el paso de ingesta marcó como `ingested: true`
4 artículos que **nunca fueron revisados** en esta sesión (ninguno estaba en
pending_ingest.md):
  - sltrib.com/.../utah-nuclear-energy-state (energía nuclear Utah — irrelevante)
  - ieeexplore.ieee.org/document/10945742 (IoT y agricultura de precisión — NO Panamá, sin revisar)
  - archive.org/.../Cataloguedipter2SaoP (catálogo de dípteros — irrelevante)
  - heraldo.es/.../aragon-...-cerdo-granjas (ganadería porcina, Aragón/España — NO Panamá, sin revisar)
  Solo 1 de los 5 marcados coincidía con el lote real revisado (Cultural Rules).
  CORRECCIÓN aplicada manualmente en sources/processed.json:
    - Revertidos a `ingested: false` los 4 artículos no revisados (vuelven a la cola).
    - Marcados `ingested: true` los 4 falsos positivos reales del lote (MITI/MARii,
      Kevin O'Leary timeline, Box Elder, Utah Gov Cox) vía edición directa, ya que el
      comando singular `mark-ingested <url>` también falla: itera `processed.items()`
      sin filtrar claves internas (`_gdelt_windows`), y truena con
      `AttributeError: 'list' object has no attribute 'get'`.
  Recomendación al usuario/desarrollador: en `scripts/ingest.py`, (1) hacer que
  `find_pending()` (usado por `mark_all_ingested`) ordene por el mismo criterio de
  prioridad que usa `ingest` (o mejor, que `run_prepare` persista qué URLs exactas
  quedaron en el lote de pending_ingest.md para que mark-all-ingested marque solo esas),
  y (2) hacer que `mark_ingested()` use `article_entries(processed)` en vez de iterar
  `processed.items()` directamente para evitar el crash con claves internas.

## 2026-08-03 08:35
FALSOS POSITIVOS: 5/5 artículos del segundo lote `ingest --limit 5` rechazados — 0%
ingestados al wiki (segundo lote consecutivo 100% falso positivo)
  - heraldo.es: Aragón, sentencia sobre espacio por cerdo en granjas — España, no Panamá
  - sltrib.com: Utah, uranio para energía nuclear (menciona "Military Installation
    Development Authority (MIDA)" — confirma la colisión de sigla documentada arriba)
  - nyfb.org: New York Farm Bureau — EE.UU., no Panamá
  - heraldo.es: Arvensis Agro, nutrición vegetal — Aragón, España, no Panamá
  - spa.gov.sa: Programa "Reef Saudi", agricultura de secano — Arabia Saudita, no Panamá
  Marcados `ingested: true` (revisados y descartados) directamente en processed.json,
  ya que `mark-ingested` (comando singular) también está roto (ver bug arriba).
  Ningún contenido creado en wiki/.

  DIAGNÓSTICO SISTÉMICO: 10/10 artículos revisados en esta sesión fueron falsos
  positivos (0% relacionados con agro panameño). Revisando la cola restante (6
  pendientes) con `queue --top 10`, TODOS sin excepción son también no-Panamá:
  Finep (Brasil), Persian Qanat (Irán, histórico), AEGA/Luis Biendicho (Aragón, España),
  Ambient IoT precision agriculture (genérico, sin país), Catalogue of diptera (taxonomía,
  irrelevante). Esto sugiere que el mecanismo de fetch/scoring (`scripts/prioritize.py` y/o
  las queries GDELT/RSS) está capturando noticias agropecuarias o menciones de "MIDA" a
  nivel global sin filtrar por relevancia geográfica a Panamá. Se detiene la revisión de
  la cola en este punto de la sesión para evitar más falsos positivos; se recomienda
  revisar la lógica de scoring/fetch antes de la próxima sesión (ver recomendación en la
  entrada anterior).
