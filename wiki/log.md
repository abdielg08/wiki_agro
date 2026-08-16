---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-16
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

## 2026-08-16 00:00
ROUTINE: `python wiki_agro.py stats` → 16 pendientes de ingesta.
`python wiki_agro.py ingest --limit 5` entregó 5 artículos, los 5 son
**falsos positivos** (0% ingestados al wiki, 0 páginas creadas/actualizadas):
  1. "MITI working on simplified NCM customised incentive mechanism..."
     (paultan.org, 2026-07-08) — sobre Malasia: MITI/MIDA = Malaysian
     Investment Development Authority y MARii, nada que ver con Panamá
     ni con el MIDA panameño (Ministerio de Desarrollo Agropecuario).
  2. "Timeline: How the Kevin O'Leary data center plan came to be..."
     (sltrib.com, 2026-05-19) — sobre un data center en Utah, EE.UU.
     "MIDA" = Military Installation Development Authority (Utah), no
     agro panameño.
  3. "Box Elder data center opponents hope for a vote..."
     (sltrib.com, 2026-05-27) — mismo caso: MIDA de Utah (data centers),
     no agro panameño.
  4. "Utah Gov. Cox issues order to protect Great Salt Lake..."
     (sltrib.com, 2026-05-29) — mismo caso: MIDA de Utah, calidad del
     aire y agua, no agro panameño.
  5. "Cultural Rules For Staying With Locals Abroad"
     (msn.com, 2026-03-07) — artículo de viajes que solo menciona de
     paso una demanda contra el MIDA de Utah; no agro panameño.
  Causa raíz: el fetch/keyword-match de la fuente `prensa.com` está
  capturando artículos por la coincidencia de la sigla "MIDA" en inglés
  (Malaysia / Utah) en vez de filtrar por el MIDA panameño o por
  contenido agropecuario de Panamá. Recomendación: ajustar el filtro de
  ingesta para exigir contexto Panamá (dominio .pa, mención explícita de
  "Panamá"/"Panama", o co-ocurrencia con otras entidades panameñas) antes
  de aceptar coincidencias de "MIDA" como agro-relevantes.
  Acción: los 5 artículos se marcan como ingestados (procesados) via
  `mark-all-ingested --limit 5` para no bloquear la cola de pendientes,
  pero NO se creó ni modificó ninguna página de wiki/. Pendientes bajan
  de 16 a 11; ninguna página nueva agregada al índice.

## 2026-08-16 00:15
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-16 00:30
BUG DETECTADO: `mark-all-ingested --limit N` ordena por nombre de archivo
(`find_pending`), mientras que `ingest --limit N` ordena por score de
relevancia (`prioritize`). Al ejecutar `mark-all-ingested --limit 5`
justo después de revisar el lote de `ingest --limit 5`, se marcaron
como ingestados 5 artículos DISTINTOS a los revisados (solo 1/5 coincidió
por azar), sin que la routine los evaluara. Corregido manualmente en esta
sesión: se revirtió `ingested=false` en los 4 artículos marcados por error
sin revisión ("Utah wants to process uranium...", "Ambient IoT: Communications
Enabling Precision Agriculture", "Catalogue of the diptera...", "Aragón
celebra la sentencia... espacio por cerdo") y se marcó correctamente
`ingested=true` en los 4 artículos del lote 1 que sí fueron revisados como
falsos positivos ese lote (MITI Malasia, Kevin O'Leary timeline, Box Elder
data center, Utah Gov Cox order). Recomendación: usar siempre
`mark-ingested '<url>'` (por URL) en vez de `mark-all-ingested --limit N`
hasta que el ordenamiento de ambos comandos se unifique.

## 2026-08-16 00:45
ROUTINE (continuación): con la cola corregida, se generó un segundo lote
de 5 pendientes y luego se revisó la cola completa restante (11 artículos
en total). Los 11 son **falsos positivos** — ninguno trata sobre agro de
Panamá, a pesar de estar etiquetados con `fuente: prensa.com`:
  1. "Aragón celebra la sentencia del Supremo... espacio por cerdo en las
     granjas" (heraldo.es, 2025-11-25) — porcicultura de Aragón, España.
  2. "Utah wants to process uranium on the Wasatch Front..." (sltrib.com,
     2025-06-13) — coincidencia por sigla "MIDA" (Military Installation
     Development Authority, Utah); tema energía nuclear, no agro.
  3. "Arvensis Agro amplía sus instalaciones..." (heraldo.es, 2026-06-23) —
     empresa de nutrición vegetal de Aragón, España.
  4. "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture"
     (spa.gov.sa, 2026-06-24) — programa agrícola de Arabia Saudita.
  5. "Finep vai pagar R$ 220 milhões para inovações em agricultura
     familiar" (agenciabrasil.ebc.com.br, 2026-07-02) — Brasil.
  6. "The Persian Qanat" (whc.unesco.org, 2026-07-07) — sitio UNESCO,
     sistema de riego histórico de Irán.
  7. "AEGA pide elecciones al campo en Aragón..." (heraldo.es, 2026-06-08)
     — gremio agrario de Aragón, España.
  8. "New York Farm Bureau" (nyfb.org, 2026-06-17) — gremio agrícola de
     Nueva York, EE.UU.
  9. "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es,
     2026-05-03) — política regional de Aragón, España.
  10. "Ambient IoT: Communications Enabling Precision Agriculture"
      (ieeexplore.ieee.org, 2025-03-31) — paper técnico de telecom/6G,
      sin referencia geográfica a Panamá.
  11. "Catalogue of the diptera of the Americas South of United States"
      (archive.org, 2016-05-13) — catálogo entomológico histórico, no es
      noticia ni trata de agro panameño.

**Causa raíz identificada**: `scripts/fetch_news.py::fetch_ddg_search()`
(fuente configurada en `config/sources.yaml` como `web_searches: prensa_agro`,
`site: "prensa.com"`, query con términos genéricos + "MIDA") no aplicaba el
filtro `_is_panama_related()` que sí usa `fetch_rss()`. La API de búsqueda de
DuckDuckGo (`ddgs.news()`) no respeta de forma confiable el operador `site:`,
así que la búsqueda trae resultados de dominios completamente ajenos
(heraldo.es, sltrib.com, nyfb.org, ieeexplore.ieee.org, archive.org, etc.) y
el código los etiqueta igualmente como `fuente: prensa.com`, ocultando el
origen real. Además, "MIDA" como término primario de búsqueda coincide con
"Military Installation Development Authority" (Utah, EE.UU.) y con la
"Malaysian Investment Development Authority" (Malasia), no solo con el MIDA
panameño.

**Fix aplicado**: se agregó a `fetch_ddg_search()` el mismo guardrail que ya
usa `fetch_rss()` — `_is_blocked_domain(url)` y `_is_panama_related(title, url)`
— para exigir una señal explícita de Panamá antes de aceptar un resultado de
búsqueda web. Esto debería eliminar la mayoría de estos falsos positivos en
la próxima corrida de GitHub Actions. La etiqueta `fuente: prensa.com` en
`processed.json` para estos 11 artículos sigue siendo incorrecta (son
metadatos ya guardados en `sources/`, inmutables) — no refleja el dominio
real; se documenta aquí para que quede claro que no son señal de La Prensa
de Panamá.

**Acción**: los 11 artículos se marcan `ingested=true` (procesados, no
ingeridos al wiki) para vaciar la cola de pendientes. 0 páginas de wiki
creadas o modificadas por este lote. Pendientes: 11 → 0.

**Total de la sesión**: 16 artículos revisados, 16 falsos positivos, 0
artículos reales ingestados al wiki. Cobertura del wiki permanece en 20
páginas / 13 artículos reales (sin cambio). Se recomienda validar el fix de
`fetch_ddg_search` en la próxima corrida de Actions antes de la siguiente
sesión de routine.
