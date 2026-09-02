---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-09-02
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

## 2026-09-02 00:00
INGEST: 4 artículos procesados (sesión Claude Code — routine programada)
  Artículos:
    - 20241107_prensacom_economia-evaluan-perdidas-en-produccion-de-arroz-maiz-y-gana → summaries/ + topics/arroz.md, topics/maiz.md, topics/cambio_climatico.md actualizados + entities/mida.md actualizado
    - 20220524_prensacom_economia-panama-proyecta-sembrar-cerca-de-90-mil-hectareas-d → summaries/ + topics/arroz.md actualizado + entities/mida.md actualizado
    - 20240607_prensacom_politica-roberto-linares-revisara-los-subsidios-en-el-mida → summaries/ + topics/politicas_agropecuarias.md actualizado + topics/subsidios_programas.md creado + entities/mida.md actualizado
    - 20240613_prensacom_economia-productores-de-arroz-de-panama-este-y-darien-exigen → summaries/ + topics/arroz.md actualizado + topics/subsidios_programas.md actualizado + entities/mida.md actualizado
  Páginas creadas: subsidios_programas.md
  Páginas actualizadas: arroz.md, maiz.md, cambio_climatico.md, politicas_agropecuarias.md, mida.md
  Summaries: 4 nuevos archivos en wiki/summaries/
  Nota: los 4 artículos solo tenían `summary_raw` truncado disponible (sin `full_text`); las páginas
  reflejan únicamente los hechos confirmados en el extracto, sin inventar cifras no presentes en la fuente.

FALSO POSITIVO DETECTADO — NO INGESTADO:
  - Archivo: 20260708_prensacom_2026-07-07-miti-working-on-simplified-ncm-customised-incenti.json
  - Título: "MITI working on simplified NCM customised incentive mechanism to build real
    local industrial capabilities"
  - URL: https://paultan.org/2026/07/07/miti-working-on-simplified-ncm-customised-incentive-mechanism-to-build-real-local-industrial-capabilities/
  - Motivo: el artículo trata sobre política industrial y de inversión de MALASIA. "MITI" es el
    Ministry of Investment, Trade and Industry de Malasia; "MIDA" aquí es la Malaysian Investment
    Development Authority (NO el Ministerio de Desarrollo Agropecuario de Panamá); "MARii" es el
    Malaysia Automotive, Robotics and IoT Institute. La fuente real es paultan.org (medio automotriz
    malasio), aunque el registro de processed.json lo etiqueta como "source: prensa.com" y
    "country: PA". No tiene relación alguna con el agro panameño.
    NO se ingestó. Se deja `ingested: false` en sources/processed.json (no se marca como ingestado)
    para no falsificar el registro, mientras se investiga por qué el pipeline de fetch/scoring de
    GDELT está clasificando erróneamente noticias de MIDA-Malasia como relevantes al agro de Panamá.
  Acción recomendada: revisar el filtro de relevancia en scripts/ (probablemente scripts/prioritize.py
  o el matching de keywords de GDELT) — el acrónimo "MIDA" es ambiguo (Panamá vs. Malasia) y está
  generando una cantidad significativa de falsos positivos en sources/processed.json (ver también
  entradas previas de thestar.com.my, fox13now.com, nyfb.org, etc. — 38 artículos siguen pendientes,
  varios de los cuales probablemente son también falsos positivos por el mismo motivo).

BUGFIX: scripts/ingest.py mark_ingested() iteraba processed.items() sin filtrar la clave interna
  `_gdelt_windows` (una lista), causando `AttributeError: 'list' object has no attribute 'get'`
  al ejecutar `mark-ingested`. Corregido para usar `article_entries(processed)` igual que el resto
  del módulo. Sin este fix, `mark-ingested` fallaba siempre que `_gdelt_windows` precediera a la
  URL objetivo en el diccionario.

INGEST: 1 artículo adicional procesado (batch 2, misma sesión)
  Al preparar un segundo lote con `ingest --limit 3` se detectaron 3 candidatos, 2 de ellos NUEVOS
  falsos positivos por la misma ambigüedad de "MIDA":
    - www.sltrib.com (Salt Lake Tribune, Utah): "Kevin O'Leary data center timeline" y "Box Elder
      data center opponents" — aquí "MIDA" = Military Installation Development Authority de Utah,
      una junta estatal que aprueba centros de datos. NO ingestados; ver Acción recomendada arriba.
    - paultan.org (MITI/Malasia) — mismo falso positivo ya documentado arriba, reaparece en la cola.
  Se identificó manualmente en sources/processed.json una veta de artículos legítimos de prensa.com
  (Panamá) aún pendientes que el orden de prioridad por score no había priorizado (ej. brote de
  influenza aviar, importación de cebolla, crédito agropecuario BNP, cooperación IICA-Argentina,
  vicem inisterio del MIDA, presupuesto MIDA/IMA 2023). Se procesó uno de ellos para completar la
  meta de la sesión:
    - 20221022_prensacom_economia-mida-refuerza-controles-por-brote-de-influenza-avia → summaries/ + topics/plagas_enfermedades.md actualizado + entities/mida.md actualizado
  Total de la sesión: **5 artículos reales ingestados** (0 falsos positivos ingestados; 3 falsos
  positivos detectados y documentados, no ingestados).

## 2026-09-02 (continuación)
DIAGNÓSTICO AVANZADO: 6 días sin artículos nuevos en sources/ (desde 2026-08-27) — supera el
  máximo de 3 días definido en CLAUDE.md como señal de falla. Se investigó con las herramientas MCP
  de GitHub (actions_list + get_job_logs) leyendo el log real de la corrida de Actions de hoy
  (run #99, id 33644553540) y la lista de las últimas ~30 corridas. Hallazgos:

  1. RSS roto: feed de IICA devuelve 403/429 (bloqueado); feed de La Prensa devuelve 0 entradas.
  2. Búsqueda web DuckDuckGo (ddgs): las 7 queries configuradas devolvieron "No results found" en
     la corrida de hoy — sospechoso de bloqueo/rate-limit hacia la IP de GitHub Actions.
  3. GDELT — BUG DE RAÍZ IDENTIFICADO en `fetch_gdelt_historical()` (scripts/fetch_news.py):
     - Las 8 ventanas trimestrales de 2015-2016 llevan fallando con timeout de conexión en TODAS
       las corridas desde el inicio del proyecto (0/8 completadas en ~99 corridas) — nunca se ha
       descargado nada de ese rango.
     - Las 36 ventanas trimestrales de 2017-2025 y la ventana 2026-Q1/Q2 (20260319_20260617) están
       correctamente completadas.
     - La ventana "viva" (más reciente, inicio fijo 2026-06-18, fin = "ayer" recalculado cada
       corrida) es un BUG DE DISEÑO: como el fin crece un día por corrida y la clave de la ventana
       incluye el fin, cada corrida exitosa genera una clave NUEVA en vez de avanzar el inicio —
       resultado: 40 claves distintas con inicio "20260618" y fines desde 20260623 hasta 20260831
       en `sources/processed.json["_gdelt_windows"]" (casi una por día de fin de junio a fines de
       agosto 2026), cada una re-descargando por completo un rango que en su mayoría ya se había
       descargado el día anterior. El rango nunca se "cierra" como un trimestre normal, sigue
       creciendo sin límite, y en algún momento entre 2026-08-31 y 2026-09-02 empezó a fallar por
       timeout (rango ya de 76+ días) y quedó atascado — explica el corte total de artículos nuevos.
     - Los timeouts de hoy afectaron TANTO las ventanas antiguas (2015-2016) COMO la ventana viva
       reciente, lo que indica un problema de conectividad/rate-limit hacia `api.gdeltproject.org`
       en el momento de la corrida, no una falta de cobertura de GDELT para fechas antiguas.
  4. Corridas #94-#97 (2026-08-28 a 2026-08-31) fallaron en ~4 segundos, antes del checkout —
     consistente con una falla transitoria de infraestructura de GitHub Actions, sin logs
     disponibles (HTTP 404 al pedirlos) para confirmar la causa raíz.

  Diagnóstico completo, recomendaciones de fix y desglose exacto documentados en `wiki/metrics.md`
  (sección "Estado del Fetch" y "Progreso del Backfill GDELT"). No se aplicó ningún cambio a
  scripts/fetch_news.py en esta sesión: el entorno de esta sesión de Claude Code tiene el egress a
  `api.gdeltproject.org` bloqueado por política de la organización (confirmado con un curl directo,
  `CONNECT tunnel failed, response 403`), por lo que cualquier fix al fetch de GDELT no podría
  probarse aquí contra la red real y debe hacerse en una sesión con acceso, o confiarse a que
  GitHub Actions lo valide.

## 2026-09-02 16:27
LINT: 26 páginas revisadas, 60 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:38, stale:20, no_index:1

## 2026-09-02 16:27
LINT: 26 páginas revisadas, 60 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:38, stale:20, no_index:1
