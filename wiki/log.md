---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-20
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

## 2026-07-20 00:00
INGEST: 5 artículos revisados, 5 falsos positivos — 0 ingestados
  Causa raíz: el fetch por palabra clave "MIDA" captura ruido de otras
  entidades homónimas no relacionadas con Panamá:
    - Malaysia: MIDA = Malaysian Investment Development Authority (agencia de MITI)
    - Utah (EE.UU.): MIDA = Military Institutional Development Authority
  Artículos descartados (NO ingestados, NO reflejados en wiki/topics ni wiki/entities):
    - 20260708_prensacom_...miti-working-on-simplified-ncm... → Malasia, MITI/MIDA/MARii, incentivos industriales. Sin relación con Panamá.
    - 20260527_prensacom_...box-elder-data-center-opponents... → Utah, MIDA (autoridad de desarrollo de instalaciones militares) vs. centro de datos. Sin relación con Panamá.
    - 20260529_prensacom_...utah-governor-issues-order-prote... → Utah, orden del gobernador sobre calidad de aire/Gran Lago Salado y centros de datos; MIDA sin autoridad ambiental. Sin relación con Panamá.
    - 20260519_prensacom_...kevin-oleary-data-center-timeline... → Utah, cronología del plan de centro de datos de Kevin O'Leary aprobado por la junta de MIDA. Sin relación con Panamá.
    - 20250613_prensacom_...utah-nuclear-energy-state... → Utah, procesamiento de uranio, acuerdo entre Guardia Nacional de Utah y MIDA. Sin relación con Panamá.
  Acción: marcados como ingestados vía `mark-all-ingested` para vaciar la cola de pendientes
  (no se crearon ni modificaron páginas de wiki/summaries, wiki/topics ni wiki/entities)
  Recomendación: el filtro de fetch/keyword debería excluir dominios de noticias de EE.UU./Malasia
  o requerir co-ocurrencia con términos como "Panamá"/"panameño" para reducir este tipo de falso positivo.

## 2026-07-20 08:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-20 08:15
BUGFIX: `mark_all_ingested()` en `scripts/ingest.py` usa `find_pending()`
  (orden alfabético por nombre de archivo), mientras que `ingest --limit N`
  usa `prioritize()` (orden por score). Como resultado, la llamada anterior
  a `mark-all-ingested --limit 5` marcó como ingestado un artículo NO
  revisado en esta sesión (ver abajo) en vez de uno de los 5 sí revisados.
  Revisión de ese artículo:
    - 20250331_prensacom_document-10945742.json (IEEE, "Ambient IoT:
      Communications Enabling Precision Agriculture") → paper académico
      genérico sobre 6G/IoT, sin ninguna mención a Panamá. FALSO POSITIVO
      confirmado igualmente — no se creó ni modificó ninguna página de wiki.
  Fix aplicado: `mark_ingested()` en scripts/ingest.py ahora usa
  `article_entries(processed)` (como el resto del módulo) en vez de iterar
  `processed.items()` crudo, lo que además corregía un crash
  (`AttributeError: 'list' object has no attribute 'get'`) al toparse con
  la clave interna `_gdelt_windows`.
  Acción correctiva: se marcó manualmente vía `mark-ingested <url>` el
  artículo pendiente que sí correspondía (paultan.org MITI/Malasia,
  repetido de la ronda anterior porque no había sido marcado).

## 2026-07-20 08:16
INGEST: 4 artículos revisados, 4 falsos positivos — 0 ingestados
  Artículos descartados (NO ingestados, NO reflejados en wiki/topics ni wiki/entities):
    - paultan.org/.../miti-working-on-simplified-ncm... → Malasia (repetido, ver entrada 08:00). Sin relación con Panamá.
    - whc.unesco.org/en/list/1506 ("The Persian Qanat") → sistema de riego histórico de Irán, sitio UNESCO. Sin relación con Panamá.
    - nyfb.org ("New York Farm Bureau") → gremio agrícola de Nueva York, EE.UU. Sin relación con Panamá.
    - spa.gov.sa/en/N2096157 ("Reef Saudi") → programa de agricultura de secano en Arabia Saudita. Sin relación con Panamá.
  Marcados como ingestados individualmente vía `mark-ingested <url>` tras el fix del bug anterior.

## 2026-07-20 08:17
DIAGNÓSTICO: 0/22 artículos descargados corresponden a agro de Panamá en esta
  sesión de ingesta (9 pendientes revisados en total = 9 falsos positivos,
  100% de la cola). El fetch automático (GDELT/RSS por palabra clave) está
  trayendo ruido de homónimos internacionales (MIDA-Malasia, MIDA-Utah) y
  artículos genéricos de agricultura sin relación con Panamá. Ningún
  artículo nuevo se agregó a wiki/ en esta sesión — tasa de falsos
  positivos de la routine se mantiene en 0% (ninguno fue ingestado
  incorrectamente), pero la tasa de falsos positivos EN LA COLA DE FETCH es
  altísima. Ver wiki/metrics.md para recomendaciones de fix al fetch.
