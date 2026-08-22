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

## 2026-08-22 00:00
ROUTINE: Diagnóstico — 17 pendientes de ingesta (30 descargados, 13 ingestados)
INGEST: lote de 5 artículos revisado — 5/5 FALSOS POSITIVOS, 0 ingestados al wiki
  Causa raíz: el fetch (GDELT/RSS) hace matching por keyword "MIDA" sin desambiguar
  entidad, capturando ruido de organizaciones homónimas no panameñas y artículos
  sin relación con agro:
    - MITI/MIDA Malaysia (incentivos industriales, paultan.org) → MIDA = Malaysian
      Investment Development Authority, no MIDA Panamá. NO es agro panameño.
    - Box Elder County data center (sltrib.com) → MIDA = Utah Military Installation
      Development Authority. NO es agro, NO es Panamá.
    - Utah Gov. Cox orden sobre Great Salt Lake / calidad de aire (sltrib.com) →
      mismo MIDA de Utah (data centers). NO es agro panameño.
    - Timeline data center Kevin O'Leary (sltrib.com) → mismo MIDA de Utah.
      NO es agro panameño.
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) → mención de
      Military Installation Development Authority de Utah en contexto de una
      demanda; artículo es sobre viajes, sin relación alguna con agro.
  Ninguno de los 5 artículos creó ni modificó páginas de wiki/. Se marcan como
  ingestados (mark-all-ingested) para sacarlos de la cola de pendientes sin
  contaminar el wiki, conforme a la regla de 0% falsos positivos.
  Acción recomendada para el fetch: filtrar por dominio geográfico (.pa, mida.gob.pa)
  o requerir co-ocurrencia de términos agro (arroz, ganadería, cosecha, MIDA Panamá,
  etc.) antes de descargar artículos que solo contienen la cadena "MIDA".

## 2026-08-22 00:11
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-22 00:30
BUGFIX: `mark-all-ingested` marcaba el conjunto equivocado de artículos.
  `ingest --limit N` selecciona los N artículos por score de relevancia
  (prioritize.py), pero `mark-all-ingested --limit N` marcaba los N primeros
  en orden alfabético de archivo (find_pending() sin ordenar por score) —
  dos conjuntos distintos. El primer `mark-all-ingested --limit 5` de esta
  sesión marcó 5 artículos que NUNCA fueron mostrados en pending_ingest.md ni
  revisados por Claude Code, saltándose el control de 0% falsos positivos.
  Se auditaron los 5 artículos marcados sin revisión — los 5 resultaron ser
  también falsos positivos genuinos (ver detalle abajo), así que no se perdió
  ningún artículo real, pero el riesgo era real: un artículo legítimo de agro
  panameño pudo haberse marcado como ingestado sin nunca llegar al wiki.
  Recomendación: no usar `mark-all-ingested` salvo que su `limit` y `strategy`
  coincidan exactamente con los del `ingest` que generó el lote; preferir
  siempre los comandos `mark-ingested <url>` individuales que genera
  `pending_ingest.md` al final de cada lote.
  Bug separado encontrado y corregido en el mismo commit: `mark-ingested`
  (comando individual) fallaba con AttributeError porque iteraba
  `processed.items()` sin excluir la clave interna `_gdelt_windows` (una
  lista, no un dict) — cualquier llamada a `mark-ingested <url>` crasheaba
  antes de encontrar la URL. Fix en `scripts/ingest.py::mark_ingested()`:
  usar `article_entries(processed)` como ya hacía `mark_all_ingested()`.

## 2026-08-22 00:45
ROUTINE: Sesión completa — cola de pendientes vaciada (17 → 0)
  Se revisaron 3 lotes adicionales (5+5+3+4 auditados retroactivamente = 17
  artículos) tras el primer lote de 5. **Los 17 fueron falsos positivos.**
  0 páginas nuevas creadas en wiki/, 0 summaries nuevos — ningún artículo
  real de agro panameño en este lote.
  Lista completa de falsos positivos de la sesión (todos fuente "prensa.com"):
    1. paultan.org — MITI/MIDA Malasia (incentivos industriales)
    2-4. sltrib.com ×3 — MIDA = Utah Military Installation Development
         Authority (data centers, calidad de aire, energía nuclear)
    5. msn.com — "Cultural Rules For Staying With Locals Abroad" (menciona
       MIDA de Utah de pasada; artículo es sobre viajes)
    6. ieeexplore.ieee.org — paper académico "Ambient IoT: Precision
       Agriculture" (6G, genérico, sin mención de Panamá)
    7. archive.org — catálogo de dípteros de Brasil (Secretaria da
       Agricultura, São Paulo, 1966/67)
    8. heraldo.es — Aragón (España), sentencia sobre espacio por cerdo en
       granjas
    9. maine.gov — Division of Agricultural Resource Development (Maine, EE.UU.)
    10. agenciabrasil.ebc.com.br — Finep financia agricultura familiar (Brasil)
    11. whc.unesco.org — "The Persian Qanat" (sistema de riego histórico, Irán)
    12. heraldo.es — AEGA pide elecciones al campo en Aragón (España)
    13. nyfb.org — New York Farm Bureau (EE.UU.)
    14. heraldo.es — Arvensis Agro amplía instalaciones (Aragón, España)
    15. spa.gov.sa — "Reef Saudi", programa de agricultura de secano (Arabia Saudita)
    16. heraldo.es — Luis Biendicho asume consejería de Medio Ambiente (Aragón, España)
    17. (uno más del primer lote de 5, ver entrada 00:00 arriba)
  **DIAGNÓSTICO CRÍTICO — Paso 4**: `python wiki_agro.py stats` ahora muestra
  Pendientes = 0, así que no hay problema de fetch detenido. El problema real
  es de PRECISIÓN: los 24 artículos acumulados bajo fuente "prensa.com" son
  el 100% falsos positivos hasta ahora (0/24 son de agro panameño real) —
  ninguno viene siquiera del dominio prensa.com; el label "prensa.com" está
  mal asignado a resultados de GDELT/búsqueda genérica por palabra clave
  ("MIDA", "agriculture") sin filtro geográfico de Panamá. Dominios reales
  vistos bajo esa fuente: sltrib.com, heraldo.es (España), spa.gov.sa,
  maine.gov, agenciabrasil.com.br, whc.unesco.org, ieeexplore.ieee.org,
  archive.org, paultan.org, msn.com, nyfb.org — ninguno panameño.
  Ventanas GDELT completadas: 72 (`_gdelt_windows` en processed.json), por
  encima del estimado de 45 — el backfill temporal ya corrió extensamente
  pero sin filtro geográfico, así que sigue trayendo ruido global.
  Último commit de GitHub Actions en sources/: 2026-08-21 11:24 UTC
  ("0 artículos nuevos") — el fetch SÍ está corriendo diariamente, no está
  caído; el problema es de calidad/precisión, no de disponibilidad.
  **Recomendación para corregir el fetch** (para revisar en scripts/):
    1. Restringir la búsqueda a dominios .pa o medios listados en CLAUDE.md
       (mida.gob.pa, prensa.com real, panamaamerica.com.pa, tvn-2.com, etc.)
    2. Si se usa GDELT por palabra clave "MIDA", exigir co-ocurrencia con
       "Panamá"/"Panama" o excluir explícitamente dominios ya identificados
       como ruido recurrente (sltrib.com, heraldo.es, spa.gov.sa, etc.)
    3. Revisar por qué el "source" se etiqueta "prensa.com" para artículos
       que no son de ese dominio — posible bug de atribución en el fetcher.
  Total falsos positivos acumulados (histórico): 24 (7 previos + 17 de hoy).
  Total artículos reales ingestados al wiki: 6 (sin cambio — lote semilla
  del 2026-05-24).
