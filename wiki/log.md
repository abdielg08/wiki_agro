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

## 2026-08-04 00:00
ROUTINE: Diagnóstico + ingesta (sesión programada)
  `stats` inicial: 29 descargados, 13 ingestados, 16 pendientes, 20 páginas wiki
  `ingest --limit 5` → 5 artículos en pending_ingest.md, TODOS falsos positivos:
    1. "MITI working on simplified NCM..." (paultan.org) — MITI/MIDA de Malasia
       (Ministry of Investment, Trade & Industry), no agro panameño. country=PA
       en metadata pero contenido 100% sobre Malasia; sin mención de Panamá.
    2. "Timeline: Kevin O'Leary data center plan" (sltrib.com) — MIDA = Military
       Installation Development Authority de Utah, EE.UU. Centro de datos, no agro.
    3. "Box Elder data center opponents" (sltrib.com) — mismo MIDA de Utah, disputa
       por centro de datos hyperscale. No agro panameño.
    4. "Utah Gov. Cox issues order to protect Great Salt Lake" (sltrib.com) — mismo
       MIDA de Utah, calidad del aire/agua ligada a centros de datos. No agro panameño.
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com) — artículo de viajes
       que menciona de pasada la demanda contra MIDA (Utah). Sin relación con Panamá.
  Causa raíz: colisión de keyword "MIDA" — el fetch RSS/GDELT indexa cualquier
  artículo que mencione la sigla "MIDA", sin distinguir el Ministerio de Desarrollo
  Agropecuario de Panamá de otras entidades homónimas (Malasia, Utah).
  Verificación: se leyó full_text/summary_raw de los 5 JSON en sources/articles/ —
  ninguno contiene "panama"/"panamá". 0 páginas de wiki creadas o modificadas.
  Acción: NO ingestados. `mark-all-ingested --limit 5` ejecutado para sacarlos de
  la cola de pendientes (ya fueron revisados y descartados, no deben re-procesarse).
  Recomendación: agregar filtro de país/contexto en el fetcher para reducir esta
  clase de falso positivo (ver sugerencia en wiki/metrics.md).

## 2026-08-04 00:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-04 00:20
BUG DETECTADO Y CORREGIDO: `mark-all-ingested` no respeta la selección de `ingest`
  Causa: `ingest --limit 5` (scripts/ingest.py:run_prepare) selecciona los 5
  artículos de pending_ingest.md vía `prioritize(..., strategy="score")`, pero
  `mark-all-ingested` (scripts/ingest.py:mark_all_ingested → find_pending) usa
  `sorted(SOURCES_DIR.glob("*.json"))`, es decir orden alfabético de archivo —
  un criterio de selección totalmente distinto. Resultado: al ejecutar
  `mark-all-ingested --limit 5` tras revisar los 5 artículos de pending_ingest.md,
  la herramienta marcó como ingestados 4 artículos DIFERENTES que nunca fueron
  leídos ni verificados ("Utah wants to process uranium...", "Ambient IoT:
  Communications Enabling Precision Agriculture", "Catalogue of the diptera of
  the Americas South of United States", "Aragón celebra la sentencia... espacio
  por cerdo en las granjas"). Solo 1 de los 5 marcados ("Cultural Rules For
  Staying With Locals Abroad") coincidía con el artículo realmente revisado.
  Corrección aplicada en esta sesión: se revirtieron manualmente (editando
  sources/processed.json) los 4 artículos marcados por error a `ingested: false`,
  y se marcaron correctamente (uno por uno, por URL) los 4 artículos que sí
  fueron revisados y confirmados como falsos positivos "MIDA": paultan.org
  (MITI/MIDA Malasia), sltrib.com Kevin O'Leary timeline, sltrib.com Box Elder
  data center, sltrib.com Utah Gov. Cox order. Nota adicional: el comando
  individual `mark-ingested <url>` también falla con
  `AttributeError: 'list' object has no attribute 'get'` porque
  `processed.json` contiene la clave `_gdelt_windows` (una lista) y
  `mark_ingested()` en scripts/ingest.py:141-152 asume que todo valor en
  `processed.items()` es un dict — no filtra la clave `_gdelt_windows`.
  RECOMENDACIÓN PARA PRÓXIMA SESIÓN DE DESARROLLO: (1) hacer que
  `mark_all_ingested` reciba explícitamente la lista de URLs a marcar (o
  reutilice la misma función `prioritize()` que usó `run_prepare`) en vez de
  re-derivar su propia selección; (2) hacer que `mark_ingested`/`mark_all_ingested`
  ignoren claves que no sean dict (como `_gdelt_windows`) al iterar
  `processed.items()`. Hasta que se corrija, NO usar `mark-all-ingested` a
  ciegas después de `ingest --limit N` — verificar el diff de
  `sources/processed.json` antes de commitear, o marcar cada URL
  individualmente (con la corrección manual del bug de `_gdelt_windows`).
