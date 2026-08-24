---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-24
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

## 2026-08-24 00:00
ROUTINE: stats al inicio → 30 descargados, 13 ingestados, 17 pendientes, 20 páginas wiki
  `python wiki_agro.py ingest --limit 5` entregó 5/5 artículos que son FALSOS POSITIVOS.
  Ninguno se ingestó al wiki. Marcados como procesados vía `mark-all-ingested --limit 5`
  para sacarlos de la cola (ya evaluados, no vuelven a aparecer en pending_ingest.md).

  Falsos positivos (5/5, colisión de acrónimo "MIDA" con entidades no panameñas):
    1. https://paultan.org/2026/07/07/miti-working-on-simplified-ncm-customised-incentive-mechanism-to-build-real-local-industrial-capabilities/
       "MIDA" = Malaysian Investment Development Authority (agencia bajo el MITI de Malasia). No es Panamá.
    2. https://www.sltrib.com/news/2026/05/27/box-elder-data-center-opponents/
       "MIDA" = Military Installation Development Authority (Utah, EE.UU.), centro de datos de Kevin O'Leary. No es Panamá.
    3. https://www.sltrib.com/news/environment/2026/05/29/utah-governor-issues-order-protect/
       Mismo MIDA de Utah — orden del gobernador Cox sobre Great Salt Lake. No es Panamá.
    4. https://www.sltrib.com/news/2026/05/19/kevin-oleary-data-center-timeline/
       Mismo MIDA de Utah — timeline del proyecto de centro de datos. No es Panamá.
    5. https://www.msn.com/en-us/news/other/cultural-rules-for-staying-with-locals-abroad/ss-AA1QWARj?ocid=BingNewsVerp
       Artículo sobre reglas culturales al hospedarse con locales; menciona la demanda contra el MIDA de Utah. No es Panamá.

  DIAGNÓSTICO DE CAUSA RAÍZ: los 5 artículos quedaron con `source: "prensa.com"` en
  sources/articles/, pero sus URLs reales son de sltrib.com, paultan.org y msn.com.
  El pipeline histórico de GDELT (`scripts/fetch_historical.py::fetch_gdelt_window`,
  usado por `fetch_gdelt_years`) NO aplicaba los filtros de seguridad que sí tiene el
  pipeline nuevo (`fetch_news.py::fetch_gdelt_batch` / `_gdelt_query_string`):
    - `_AGRO_QUERY` incluía el acrónimo "MIDA" suelto, sin exigir mención de Panamá.
    - No llamaba a `_is_blocked_domain()` ni `_is_panama_related()` sobre los
      resultados antes de guardarlos — dependía solo de `sourcecountry:PA` de GDELT,
      que no es confiable (GDELT puede mal-etiquetar el país/dominio de origen).
  Esto es la misma clase de falso positivo ya identificada y corregida parcialmente
  el 2026-06-22 (7 falsos positivos), pero el fix nunca se aplicó a `fetch_historical.py`.

  FIX APLICADO (esta sesión): `fetch_gdelt_window` ahora exige mención de Panamá en la
  query (`_AGRO_QUERY_PA`) y filtra cada resultado con `_is_blocked_domain()` +
  `_is_panama_related()`, igual que el pipeline de `fetch_news.py`. `fetch_cdx_domain`
  también gana el filtro `_is_blocked_domain()` como red de seguridad adicional.
  Ver `scripts/fetch_historical.py`.

## 2026-08-24 08:18
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-24 08:19
BUG ENCONTRADO Y CORREGIDO: la llamada anterior a `mark-all-ingested --limit 5`
NO marcó los 5 artículos que `pending_ingest.md` acababa de mostrar (los 5 falsos
positivos de MIDA de arriba). En vez de eso marcó 5 artículos completamente
distintos y nunca revisados:
  - https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/
  - https://ieeexplore.ieee.org/document/10945742 (Ambient IoT, precision agriculture)
  - https://www.msn.com/en-us/news/other/cultural-rules-for-staying-with-locals-abroad/... (correcto por coincidencia)
  - https://archive.org/details/Cataloguedipter2SaoP (catálogo de dípteros)
  - https://www.heraldo.es/.../aragon-celebra-sentencia-supremo... (Aragón, España)

  CAUSA RAÍZ: `ingest.py::run_prepare` selecciona los N pendientes vía
  `prioritize(strategy="score")` (orden por score de relevancia), pero
  `ingest.py::mark_all_ingested` llamaba a `find_pending(limit=N)`, que devuelve
  los pendientes en orden de archivo (`sorted(SOURCES_DIR.glob("*.json"))`), NO por
  score. Como resultado, `ingest --limit 5` y `mark-all-ingested --limit 5` casi
  nunca operan sobre el mismo conjunto de artículos — el flujo estándar de la
  routine (Paso 2 → Paso 3 de CLAUDE.md) podía marcar como ingestados artículos
  que Claude nunca vio ni procesó, y dejar sin marcar los que sí se procesaron
  (haciendo que reaparezcan en la siguiente sesión y se dupliquen).

  CORRECCIÓN DE DATOS: los 5 artículos marcados incorrectamente se revirtieron a
  `ingested: false` en `sources/processed.json` (ninguno tenía contenido en el
  wiki, así que no hubo pérdida de trabajo).

  FIX DE CÓDIGO: `mark_all_ingested()` en `scripts/ingest.py` ahora usa
  `prioritize(strategy="score")` sobre todos los pendientes, igual que
  `run_prepare()`, garantizando que ambos comandos operen sobre el mismo
  conjunto ordenado. Verificado: tras el fix, `mark-all-ingested --limit 5`
  marca exactamente los mismos 5 URLs que `pending_ingest.md` mostró.

## 2026-08-24 08:21
INGEST: 5 artículos marcados como ingestados por sesión Claude Code (re-ejecutado
  con el fix aplicado — ahora coincide con los 5 falsos positivos de MIDA listados
  arriba: MITI/Malasia, Box Elder/Utah, Utah Gov Cox, timeline O'Leary, MSN cultural
  rules)

## 2026-08-24 08:30
ROUTINE: revisados los 12 pendientes restantes (todos con `source: prensa.com`
  mal etiquetado). Se verificó texto completo/summary de cada uno buscando
  "panam" en título, URL y cuerpo — NINGUNO menciona Panamá. Los 12 son FALSOS
  POSITIVOS del mismo pipeline histórico roto (`fetch_gdelt_window` sin filtro
  de Panamá, ver diagnóstico de causa raíz arriba, ya corregido en el código).
  Ninguno se ingestó al wiki.

  Falsos positivos (12/12):
    1. https://www.heraldo.es/noticias/economia/2025/11/25/aragon-celebra-sentencia-supremo-tumba-ampliacion-obligatoria-espacio-cerdo-granjas-1873321.html
       Aragón (España) — sentencia sobre espacio por cerdo en granjas.
    2. https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/
       Utah (EE.UU.) — uranio para energía nuclear; menciona MIDA de Utah, no agro ni Panamá.
    3. https://www.maine.gov/dacf/ard/index.shtml
       Maine (EE.UU.) — página institucional del Dept. de Agricultura estatal.
    4. https://agenciabrasil.ebc.com.br/economia/noticia/2026-07/finep-vai-pagar-r-220-milhoes-para-inovacoes-em-agricultura-familiar
       Brasil — Finep financia innovación en agricultura familiar brasileña.
    5. https://whc.unesco.org/en/list/1506
       Irán — sistema de qanats (UNESCO), patrimonio de riego antiguo.
    6. https://www.heraldo.es/noticias/economia/2026/06/08/aega-pide-elecciones-campo-aragon-consejera-agricultura-le-responde-que-no-esta-dispuesta-gastar-un-millon-euros-2027313.html
       Aragón (España) — política agraria regional, elecciones al campo.
    7. https://www.nyfb.org/
       EE.UU. — página institucional de New York Farm Bureau.
    8. https://www.heraldo.es/noticias/economia/2026/06/23/arvensis-agro-amplia-sus-instalaciones-preve-aumentar-un-50-su-facturacion-2030-2031462.html
       Aragón (España) — empresa de nutrición vegetal amplía instalaciones.
    9. https://www.spa.gov.sa/en/N2096157
       Arabia Saudita — programa "Reef Saudi" de agricultura de secano.
    10. https://www.heraldo.es/noticias/aragon/2026/05/03/luis-biendicho-vox-asume-consejeria-medio-ambiente-con-un-inaga-bajo-lupa-investigacion-judicial-por-caso-forestalia-2017165.html
        Aragón (España) — nombramiento de consejero de Medio Ambiente.
    11. https://ieeexplore.ieee.org/document/10945742
        Paper IEEE — "Ambient IoT" para agricultura de precisión (genérico, sin país).
    12. https://archive.org/details/Cataloguedipter2SaoP
        Catálogo entomológico histórico de dípteros de América, sin relación con Panamá actual.

  Todos comparten `source: "prensa.com"` incorrecto en sources/articles/ — confirma
  que provienen del pipeline `fetch_gdelt_years`/`fetch_gdelt_window` ya corregido
  esta sesión (ver entrada de las 00:00). Marcados como procesados vía
  `mark-all-ingested --limit 0` para vaciar la cola de pendientes.

  RESULTADO DE LA SESIÓN: 17 artículos revisados, 17/17 falsos positivos (0
  ingestados al wiki — correcto, cumple la regla de 0% falsos positivos).
  Pendientes de ingesta: 12 → 0. Ningún artículo nuevo agregado al wiki hoy
  porque no había contenido genuino de agro panameño en la cola actual.

## 2026-08-24 08:22
INGEST: 12 artículos marcados como ingestados por sesión Claude Code

## 2026-08-24 08:45
DIAGNÓSTICO REFINADO DE CAUSA RAÍZ (falsos positivos "prensa.com"):
  Los 17 falsos positivos de esta sesión tenían `source: "prensa.com"` exacto
  (sin "www."), lo cual NO coincide con `fetch_cdx_domain`/`fetch_sitemap_domain`
  (que usan `"www.prensa.com"`) ni con el `domain` real reportado por GDELT.
  Se rastreó hasta `config/sources.yaml::web_searches` → entrada `prensa_agro`
  (`site: "prensa.com"`), consumida por `fetch_news.py::fetch_ddg_search`.

  BUG REAL: `fetch_ddg_search` arma la query como `site:prensa.com <términos>`
  y confía en que DuckDuckGo/ddgs respete el operador `site:`, pero luego etiqueta
  CADA resultado con `"source": site` sin verificar que la URL devuelta
  pertenezca realmente a ese dominio. El operador `site:` de ddgs.news() no es
  confiable al 100% — quedaron resultados de sltrib.com, paultan.org, heraldo.es,
  maine.gov, nyfb.org, spa.gov.sa, ieeexplore.org, archive.org, whc.unesco.org y
  agenciabrasil.ebc.com.br todos etiquetados como si fueran de La Prensa (Panamá,
  fuente confiable Nivel 3). Este es el origen real de los 17 falsos positivos
  de hoy (más probable que el bug de `fetch_gdelt_window` corregido antes, que
  también se dejó arreglado por seguridad).

  FIX APLICADO: `fetch_ddg_search()` en `scripts/fetch_news.py` ahora verifica
  que el dominio de la URL devuelta termine en `site` antes de aceptarla
  (`_url_domain(url).endswith(site.lower())`) y aplica `_is_blocked_domain()`
  como red adicional. Así ya no se puede mal-atribuir contenido extranjero a
  una fuente panameña de confianza.

## 2026-08-24 08:25
LINT: 20 páginas revisadas, 54 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:11, no_index:1
