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
INGEST: Routine automática — 5 artículos revisados, 5 FALSOS POSITIVOS (0 ingestados)
  Causa raíz: coincidencia de sigla "MIDA" — el pipeline de fetch (probablemente
  búsqueda por keyword "MIDA") capturó artículos en inglés sobre Utah (EE.UU.)
  y Malasia que no tienen relación con Panamá ni con el agro panameño:
    - 20260708_prensacom_...miti-working-on-simplified-ncm... → "MIDA" = agencia de
      Malaysian Investment Development Authority (Malasia), no Panamá. RECHAZADO.
    - 20260519_prensacom_...kevin-oleary-data-center-timeline... → "MIDA" = Utah's
      Military Installation Development Authority (data center Stratos, Utah, EE.UU.).
      RECHAZADO.
    - 20260527_prensacom_...box-elder-data-center-opponents... → mismo caso, oposición
      a centro de datos de Kevin O'Leary en Utah. RECHAZADO.
    - 20260529_prensacom_...utah-governor-issues-order-prote... → orden del gobernador
      de Utah sobre calidad de aire/agua vs. centros de datos; "MIDA" = agencia de Utah.
      RECHAZADO.
    - 20260307_prensacom_...cultural-rules-for-staying-with-locals-abro... → artículo de
      viajes/cultura sin relación con agro; mención tangencial a la demanda contra la
      "MIDA" de Utah. RECHAZADO.
  Nota: estos artículos tenían `country: PA` en su metadata pese a ser 100% sobre EE.UU.
  y Malasia — el tag de país del fetch no es confiable como filtro por sí solo.
  Los 5 fueron marcados como ingestados vía `mark-all-ingested` para limpiar la cola de
  pendientes; ninguna página de wiki fue creada ni modificada por estos artículos.
  Acción recomendada: revisar el filtro de fuente `prensa.com`/keyword "MIDA" en el
  fetcher — está trayendo ruido internacional no panameño.

## 2026-08-04 08:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-04 08:20
BUG ENCONTRADO: `mark-all-ingested --limit N` NO marca los mismos artículos que muestra
`ingest --limit N`.
  Causa: `ingest` (run_prepare) selecciona pendientes vía `prioritize()` (orden por score),
  mientras que `mark-all-ingested` llama a `find_pending(limit=N)` directamente, que usa
  orden alfabético/cronológico de archivo (`sorted(SOURCES_DIR.glob("*.json"))`). Ambas
  funciones recorren la misma cola de pendientes pero con criterios de orden distintos,
  por lo que "los primeros N" de una no son "los primeros N" de la otra.
  Efecto real esta sesión: de los 5 artículos revisados y documentados como falsos
  positivos en la entrada 2026-08-04 00:00 (paultan.org MITI, 3× sltrib.com Utah/MIDA,
  msn.com cultural-rules), `mark-all-ingested --limit 5` solo marcó 1 de ellos
  (msn.com) como ingestado. Los otros 4 marcados fueron artículos DISTINTOS que nunca
  habían sido revisados:
    - archive.org/details/Cataloguedipter2SaoP → catálogo de zoología de 1966/67
      (Secretaria da Agricultura, Brasil). Sin relación con Panamá. FALSO POSITIVO.
    - ieeexplore.ieee.org/document/10945742 → paper académico "Ambient IoT: Communications
      Enabling Precision Agriculture" (6G, agricultura de precisión, genérico/global, sin
      mención de Panamá). FALSO POSITIVO.
    - sltrib.com/.../utah-nuclear-energy-state → energía nuclear en Utah, EE.UU.;
      menciona "MIDA" = Military Installation Development Authority (Utah). FALSO POSITIVO.
    - heraldo.es/.../aragon-celebra-sentencia-supremo...cerdo-granjas → fallo judicial
      español sobre espacio mínimo por cerdo en granjas de Aragón, España (Consejería de
      Agricultura de Aragón, no Panamá). FALSO POSITIVO.
  Por suerte los 4 resultaron ser también falsos positivos, así que no se violó la regla
  de 0% falsos positivos ingestados al wiki — pero el hallazgo expone un riesgo real: este
  desajuste pudo haber marcado como "ingested" un artículo verdaderamente sobre agro
  panameño sin que ningún LLM lo revisara ni creara página de wiki para él, perdiéndolo
  silenciosamente para siempre (el artículo nunca reaparece en pendientes).
  Mitigación aplicada esta sesión: se dejó de usar `mark-all-ingested` para el resto de
  la cola; se revisó cada uno de los 11 artículos pendientes restantes individualmente y
  se marcaron con una llamada directa a `save_processed()` (equivalente a `mark-ingested`
  por URL), ya que `mark-ingested` individual también tiene un bug — itera
  `processed.items()` sin excluir la clave interna `_gdelt_windows` (una lista), y falla
  con `AttributeError: 'list' object has no attribute 'get'` en la primera URL.
  Acción recomendada para próxima sesión: corregir `scripts/ingest.py`:
    1. `mark_all_ingested()` debe usar el mismo `prioritize()`/orden que `run_prepare()`,
       o mejor, `ingest` debería persistir la lista exacta de URLs seleccionadas (p. ej.
       en un archivo de estado) y `mark-all-ingested` debería marcar exactamente esas
       URLs, no recalcular la cola.
    2. `mark_ingested()` (singular) debe usar `article_entries(processed)` en vez de
       iterar `processed.items()` directamente, para excluir `_gdelt_windows`.

## 2026-08-04 08:25
INGEST: Routine automática — 11 artículos pendientes restantes revisados, 11 FALSOS
POSITIVOS (0 ingestados al wiki). Con esto, pendientes de ingesta = 0.
  Ruido internacional confirmado por país/tema (ninguno sobre agro de Panamá):
    - 3× heraldo.es (Aragón, España): consejería de Agricultura de Aragón (caso Forestalia),
      AEGA pide elecciones al campo, Arvensis Agro amplía instalaciones. Todos sobre
      agricultura española, no panameña.
    - 3× sltrib.com (Utah, EE.UU.): timeline centro de datos Kevin O'Leary, oposición en
      Box Elder, orden del gobernador Cox — coincidencia de sigla "MIDA" (Utah Military
      Installation Development Authority).
    - nyfb.org → New York Farm Bureau (EE.UU.).
    - spa.gov.sa → "Reef Saudi", programa de agricultura de secano en Arabia Saudita.
    - agenciabrasil.ebc.com.br → Finep financia innovación en agricultura familiar,
      Brasil.
    - whc.unesco.org → "The Persian Qanat", sistema de riego histórico de Irán.
    - paultan.org → MITI/MIDA de Malasia (Malaysian Investment Development Authority),
      mecanismo de incentivos industriales. Ya visto en la entrada 08:20.
  Todos los artículos tenían `country: PA` en su metadata pese a no tener relación con
  Panamá — confirma que el tag de país del fetch no filtra correctamente y que la fuente
  `prensa.com` está agregando ruido global (probablemente vía búsqueda de keyword
  "agro"/"agricultura"/"MIDA" sin filtro geográfico).
  Estado del wiki: sin cambios de contenido esta sesión (0 páginas nuevas) — los 16
  artículos pendientes al inicio de la sesión (5 + 11) resultaron ser 100% ruido
  internacional. Cobertura de fuentes 100% panameñas (MIDA, IDIAP, BDA, IICA, La Prensa,
  TVN) sigue en 6 artículos, sin cambios desde 2025-05-24.
  Acción recomendada: ajustar `config/sources.yaml` / lógica de fetch para excluir
  dominios claramente no panameños (heraldo.es, sltrib.com, spa.gov.sa,
  agenciabrasil.ebc.com.br, whc.unesco.org, paultan.org, nyfb.org, thestar.com.my) o
  exigir mención explícita de Panamá en el texto antes de aceptar un artículo como
  candidato a ingesta.
