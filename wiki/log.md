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

## 2026-08-20 00:00
ROUTINE: 5 artículos pendientes revisados — 5 falsos positivos (0 ingestados)
  Causa raíz: colisión de sigla "MIDA" — el filtro de fetch capturó artículos de
  prensa.com que mencionan "MIDA" pero refiriéndose a organizaciones homónimas
  no panameñas, ninguno menciona Panamá:
    1. "MITI working on simplified NCM customised incentive mechanism..." (paultan.org, 2026-07-08)
       → MIDA = Malaysian Investment Development Authority (Malasia)
    2. "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    4. "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07)
       → menciona demanda contra MIDA (Utah), sin relación con agro panameño
  Acción: NO se creó contenido en wiki/. Los 5 marcados como ingestados vía
  `mark-all-ingested` para sacarlos de la cola (no reaparecerán como pendientes).
  Recomendación: el fetch (RSS/GDELT) debería excluir dominios no relacionados con
  Panamá (paultan.org, sltrib.com, msn.com) o exigir coincidencia con "Panamá"/"Panama"
  además de "MIDA" para reducir este tipo de falso positivo en fuentes prensa.com.

## 2026-08-20 08:12
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-20 08:20
BUGFIX: `mark_ingested()` en `scripts/ingest.py` fallaba con `AttributeError:
'list' object has no attribute 'get'` al iterar `processed.items()` sin
excluir la clave interna `_gdelt_windows` (una lista, no un dict). Esto
rompía el comando `python wiki_agro.py mark-ingested <url>` — exactamente el
comando que `pending_ingest.md` indica ejecutar tras procesar cada artículo —
y dejaba artículos ya evaluados reapareciendo como pendientes en la siguiente
ronda de ingesta. Fix: usar `article_entries(processed)` (ya usado por
`mark_all_ingested`) para excluir claves `_meta` antes de iterar.

HALLAZGO ADICIONAL (riesgo de proceso): `python wiki_agro.py mark-all-ingested
--limit 5` NO selecciona el mismo lote que `python wiki_agro.py ingest --limit 5`
mostró en `pending_ingest.md` — `ingest` ordena por score de relevancia
(`run_prepare`), mientras `mark-all-ingested` usa `find_pending()` (orden por
nombre de archivo). Al ejecutar `mark-all-ingested --limit 5` a las 00:00 se
marcaron como ingestados 5 artículos, pero SOLO 1 (msn.com) coincidía con los
5 revisados en `pending_ingest.md`; los otros 4 (archive.org catálogo de
dípteros, paper IEEE de IoT en agricultura de precisión, sltrib.com sobre
uranio en Utah, heraldo.es sobre sentencia porcina en Aragón) nunca fueron
mostrados para revisión. Se verificaron manualmente después: los 4 son
también falsos positivos (ninguno menciona Panamá), así que no hubo pérdida
de contenido real esta vez — pero el riesgo es real: `mark-all-ingested`
podría marcar como "ingestado" (y sacar de la cola para siempre) un artículo
genuino de Panamá sin que el LLM lo haya visto ni creado la página
correspondiente. Recomendación: no usar `mark-all-ingested` como paso
genérico de la routine; usar `mark-ingested <url>` por artículo, solo
después de revisar el texto real mostrado en `pending_ingest.md` (como se
hizo para el resto de esta sesión), o corregir `mark-all-ingested` para que
use el mismo orden por score que `ingest`.

## 2026-08-20 08:35
ROUTINE: 12 artículos pendientes adicionales revisados — 12 falsos positivos (0 ingestados)
  Continuación de la ronda 00:00 (bug de marcado corregido). Ninguno menciona Panamá:
    - paultan.org (MITI/MIDA Malasia) — reaparecido por el bug, remarcado ahora
    - sltrib.com × 3 (MIDA = Military Installation Development Authority, Utah) — remarcados
    - maine.gov/dacf/ard — Agricultural Resource Development Division (Maine, EE.UU.)
    - agenciabrasil.ebc.com.br — Finep financia innovación agrícola (Brasil)
    - whc.unesco.org — "The Persian Qanat" (Irán, patrimonio UNESCO)
    - heraldo.es × 2 — AEGA / consejería de Agricultura de Aragón (España)
    - nyfb.org — New York Farm Bureau (EE.UU.)
    - spa.gov.sa — Programa "Reef Saudi" de agricultura de secano (Arabia Saudita)
    - heraldo.es — nombramiento de consejero de Medio Ambiente de Aragón (España)
  Acción: NO se creó contenido en wiki/. Los 12 marcados como ingestados
  individualmente vía `mark-ingested <url>` para sacarlos de la cola.

  Más los 3 marcados a las 00:00 vía `mark-all-ingested` sin revisión previa
  (ver hallazgo 08:20) y verificados retroactivamente como falsos positivos:
    - archive.org — catálogo de dípteros de Sudamérica (Brasil, 1966/67)
    - ieeexplore.ieee.org — paper "Ambient IoT: Communications Enabling
      Precision Agriculture" (académico, genérico, sin mención geográfica)
    - heraldo.es — sentencia del Supremo sobre espacio porcino en Aragón (España)

  Total sesión: 18/18 artículos pendientes eran falsos positivos (0 ingestados
  al wiki). `Pendientes de ingesta` = 0 tras esta sesión.

DIAGNÓSTICO: la fuente "prensa.com" (24/30 artículos descargados, el 80% del
total) resultó ser 100% falsos positivos en esta sesión — ninguno de sus
artículos pendientes mencionaba Panamá. Los 6 artículos "reales" ya en el
wiki provienen todos de fuentes semilla no-prensa.com (MIDA, IDIAP, BDA,
IICA, TVNNoticias, LaPrensaEco). Esto sugiere que el fetch bajo la etiqueta
"prensa.com" no está filtrando por relevancia geográfica a Panamá — probable
causa: búsqueda GDELT/RSS por palabras clave genéricas de agro (o por la
sigla "MIDA") sin restringir dominio o mención explícita de "Panamá"/"Panama".
Recomendación para el pipeline de fetch: (1) exigir coincidencia de
"Panamá"/"Panama" en título o texto además de las palabras clave de agro,
(2) restringir o excluir dominios de noticias no panameños que hayan
producido falsos positivos repetidos (paultan.org, sltrib.com, heraldo.es,
maine.gov, whc.unesco.org, spa.gov.sa, agenciabrasil.ebc.com.br, nyfb.org,
msn.com), (3) revisar por qué la fuente se etiqueta genéricamente
"prensa.com" cuando el contenido real proviene de otros dominios.

## 2026-08-20 08:16
LINT: 20 páginas revisadas, 55 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:12, no_index:1
