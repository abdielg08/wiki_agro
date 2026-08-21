---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-21
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

## 2026-08-21 00:00
FALSOS POSITIVOS: 5/5 artículos del lote pendiente rechazados — 0% ingestados
  Ninguno de los 5 artículos trata sobre agro panameño. Todos coinciden por la
  palabra clave "MIDA", pero se refieren a entidades homónimas no relacionadas:
    1. paultan.org — MITI/MIDA de Malasia (Malaysian Investment Development Authority),
       incentivos industriales.
    2. sltrib.com — "Box Elder data center opponents" — MIDA = Military Installation
       Development Authority (Utah, EE.UU.), oposición a centro de datos.
    3. sltrib.com — Orden del gobernador de Utah sobre calidad de aire/Great Salt Lake
       y centros de datos, menciona MIDA de Utah.
    4. sltrib.com — Cronología del plan de centro de datos de Kevin O'Leary, MIDA
       = junta de desarrollo de instalaciones militares de Utah.
    5. msn.com — "Cultural Rules For Staying With Locals Abroad", menciona demanda
       contra MIDA de Utah de forma incidental.
  (Nota: el campo `full_text` de estos JSON está vacío, pero `summary_raw` sí
  tiene contenido — de ahí se confirmó el tema de cada uno.)
  DIAGNÓSTICO DE CAUSA RAÍZ: los 5 artículos están etiquetados con fuente
  "prensa.com" en processed.json pero sus URLs reales no pertenecen a prensa.com
  (paultan.org, sltrib.com, msn.com). En scripts/fetch_news.py, la búsqueda DDG
  usa `site:{site} {query}` (línea ~257) pero la API de noticias de DDG no
  respeta estrictamente el filtro `site:`, devolviendo resultados globales que
  matchean la palabra clave "MIDA" sin filtro geográfico.
  ACCIÓN: los 5 se marcan como `ingested: true` (procesados/evaluados), pero
  NO se creó ninguna página de wiki ni resumen para ellos.

## 2026-08-21 00:16
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-21 00:30
BUGFIX: `mark-all-ingested` marcaba artículos incorrectos (no revisados)
  Al ejecutar `mark-all-ingested --limit 5` para cerrar el lote de falsos
  positivos de arriba, se detectó que el comando marcó como `ingested: true`
  5 artículos DISTINTOS a los 5 que Claude Code había revisado. Causa: el
  comando `ingest` (scripts/ingest.py `run_prepare`) selecciona artículos por
  score de relevancia vía `prioritize()`, pero `mark_all_ingested` llamaba a
  `find_pending(limit=N)` directamente, que ordena por nombre de archivo
  (orden alfabético del glob) — un orden completamente distinto. Resultado:
  se marcaron como "procesados" 4 artículos que Claude Code NUNCA evaluó
  (uranio/nuclear en Utah, un paper de IEEE sobre IoT agrícola, un catálogo
  de dípteros de 1966 en archive.org, y una nota de Aragón sobre cuotas de
  espacio porcino) — ninguno relacionado con Panamá, pero marcados sin
  revisión, lo cual habría ocultado esa cola para siempre sin dejar rastro
  en el log.
  CORRECCIÓN APLICADA:
    1. Se revirtió `ingested: false` en processed.json para esos 4 artículos
       no revisados (quedó como `ingested: true` únicamente el de msn.com,
       que sí fue revisado y coincide con el lote de arriba).
    2. Se corrigió `scripts/ingest.py`:
       - `mark_all_ingested()` ahora usa `prioritize(strategy="score")`
         sobre el pool completo de pendientes antes de recortar por
         `limit`, igual que `run_prepare()` — así marca exactamente los
         artículos que se mostraron en `pending_ingest.md`.
       - `mark_ingested()` (marcado individual por URL) iteraba sobre
         `processed.items()` crudo, incluyendo la clave interna
         `_gdelt_windows` (una lista, no un dict de artículo), lo cual
         causaba un `AttributeError: 'list' object has no attribute 'get'`
         y hacía que el comando `python wiki_agro.py mark-ingested <url>`
         — el que `pending_ingest.md` recomienda usar al pie de cada
         lote — fallara siempre. Se cambió a iterar sobre
         `article_entries(processed)`, que ya filtra las claves `_meta`.
  IMPACTO: antes de este fix, cualquier sesión que usara
  `mark-all-ingested --limit N` corría el riesgo de marcar como
  "procesados" artículos nunca vistos por Claude Code, dejándolos fuera
  de la cola sin que constara en el log ni en el wiki. Con el fix, ambos
  comandos quedan alineados con el orden de `ingest`.

## 2026-08-21 00:45
FALSOS POSITIVOS: 12/12 artículos pendientes rechazados — cola de
"prensa.com" completamente vaciada, 0% ingestados como contenido real
  Tras el fix de `mark-all-ingested`, se procesaron los 12 artículos
  pendientes restantes (todos etiquetados fuente "prensa.com"). Ninguno
  trata sobre agro panameño:
    1. heraldo.es (Aragón, España) — sentencia sobre espacio por cerdo en granjas
    2. sltrib.com (Utah, EE.UU.) — procesamiento de uranio, menciona MIDA de Utah
    3. maine.gov (EE.UU.) — División de Desarrollo de Recursos Agrícolas de Maine
    4. agenciabrasil.ebc.com.br (Brasil) — financiamiento Finep para agricultura familiar
    5. whc.unesco.org (Irán) — sistema de riego Qanat persa (patrimonio UNESCO)
    6. heraldo.es (Aragón, España) — AEGA pide elecciones al campo
    7. nyfb.org (Nueva York, EE.UU.) — New York Farm Bureau (página institucional)
    8. heraldo.es (Aragón, España) — Arvensis Agro amplía instalaciones
    9. spa.gov.sa (Arabia Saudita) — programa "Reef Saudi" de agricultura de secano
    10. heraldo.es (Aragón, España) — cambio de consejería de Medio Ambiente
    11. ieeexplore.ieee.org — paper académico sobre IoT y agricultura de precisión
    12. archive.org — catálogo de dípteros de Sudamérica (1966)
  HALLAZGO SISTÉMICO: de las 24 descargas acumuladas bajo la fuente
  "prensa.com" (ver `stats`), NINGUNA ha producido jamás un resumen en
  `wiki/summaries/` (0 archivos con prefijo `*_prensacom_*`). Los 6
  artículos semilla originales del wiki usaron otras fuentes (MIDA,
  LaPrensaEco, TVNNoticias, IICA, BDA). Esto sugiere que la fuente DDG
  "prensa.com" (scripts/fetch_news.py, búsqueda `site:prensa.com {query}`)
  nunca ha traído contenido real de prensa.com — el filtro `site:` no
  funciona con `ddgs.news()` y devuelve ruido global que matchea palabras
  clave genéricas de agricultura o "MIDA" sin ningún filtro geográfico.
  ACCIÓN: los 12 se marcan como `ingested: true` (revisados y rechazados)
  para no seguir bloqueando la cola; no se creó ninguna página de wiki.
  RECOMENDACIÓN PARA EL USUARIO (requiere intervención humana, fuera del
  alcance de esta sesión de rutina): revisar/reescribir la búsqueda DDG en
  `scripts/fetch_news.py` para la fuente "prensa.com" — considerar buscar
  sin `site:` y filtrar el dominio del resultado en Python, o cambiar a un
  método de descubrimiento distinto (RSS de prensa.com si existe, o
  restringir a los dominios de fuentes de Nivel 1-3 de CLAUDE.md). Mientras
  no se corrija, cada sesión de rutina seguirá descargando ruido bajo la
  etiqueta "prensa.com" que debe rechazarse manualmente.

## 2026-08-21 00:19
INGEST: 4 artículos marcados como ingestados por sesión Claude Code

## 2026-08-21 00:20
INGEST: 12 artículos marcados como ingestados por sesión Claude Code
