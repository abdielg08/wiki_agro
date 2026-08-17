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

## 2026-08-17 00:00
ROUTINE: Sesión programada — 16 artículos pendientes revisados, 0 ingestados (16/16 falsos positivos)

**Falsos positivos detectados (0 mentions de "Panama"/"Panamá" en el texto completo):**
  Lote 1/3:
    - "MITI working on simplified NCM..." (paultan.org) — MIDA = agencia de Malasia (MITI-MIDA), no MIDA-Panamá
    - "Kevin O'Leary data center timeline" (sltrib.com) — MIDA = Military Installation Development Authority, Utah
    - "Box Elder data center opponents..." (sltrib.com) — mismo MIDA de Utah
    - "Utah Gov. Cox issues order..." (sltrib.com) — mismo MIDA de Utah
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) — mismo MIDA de Utah, artículo sin relación agro
  Lote 2/3:
    - "Aragón celebra sentencia del Supremo..." (heraldo.es) — agricultura de Aragón, España
    - "Utah wants to process uranium..." (sltrib.com) — MIDA de Utah otra vez
    - "'Reef Saudi'..." (spa.gov.sa) — agricultura de Arabia Saudita
    - "Finep vai pagar R$ 220 milhões..." (agenciabrasil.ebc.com.br) — agricultura de Brasil
    - "The Persian Qanat" (whc.unesco.org) — sistema de riego histórico de Irán
  Lote 3/3:
    - "AEGA pide elecciones al campo en Aragón..." (heraldo.es) — España
    - "New York Farm Bureau" (nyfb.org) — EE.UU.
    - "Arvensis Agro amplía sus instalaciones..." (heraldo.es) — España (Aragón)
    - "Luis Biendicho asume la consejería..." (heraldo.es) — España (Aragón)
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org) — paper técnico genérico, sin país
    - "Catalogue of the diptera of the Americas..." (archive.org) — catálogo taxonómico de 1966/1967, no es noticia

  Los 16 se marcaron `ingested: true` en processed.json (sin crear páginas de wiki) para
  despejar la cola, siguiendo el precedente del 2026-06-22. Pendientes de ingesta: 16 → 0.

**Causa raíz identificada y corregida** (`scripts/fetch_news.py::fetch_ddg_search`):
  Los 16 falsos positivos venían todos de la fuente "prensa.com" (búsqueda DDG con
  `site:prensa.com ... MIDA ...`). A diferencia de `fetch_rss()`, `fetch_ddg_search()`
  NO verificaba que el dominio del resultado coincidiera con el `site:` solicitado
  (el operador `site:` de DuckDuckGo no se respeta de forma confiable) ni aplicaba
  el filtro `_is_panama_related()`. Resultado: cualquier artículo global que mencionara
  "MIDA" (agencia de Malasia, autoridad de Utah) o coincidiera con términos genéricos
  de la query ("agricultura", "cosecha") se colaba, venga de heraldo.es, sltrib.com,
  ieeexplore.org, archive.org, etc.
  FIX: se agregó verificación de dominio (`urlparse(url).netloc` debe contener el
  `site` configurado) + filtro `_is_panama_related()` como respaldo para dominios que
  no son oficiales `.gob.pa`. Commit en `scripts/fetch_news.py`.

**Bug adicional corregido** (`scripts/ingest.py::mark_ingested`):
  La función iteraba `processed.items()` sin filtrar la clave interna `_gdelt_windows`
  (una lista, no un dict de metadatos), causando `AttributeError: 'list' object has no
  attribute 'get'` en todo intento de `mark-ingested`. Se corrigió para usar
  `article_entries(processed)`, que ya excluye claves `_meta`.

**Diagnóstico avanzado — 17 días consecutivos sin artículos nuevos** (2026-07-31 → 2026-08-16):
  GitHub Actions SÍ está corriendo diariamente (`wiki_daily.yml`, cron 11:00 UTC) y
  reporta "success", pero guarda 0 artículos nuevos desde 2026-07-30. Revisando el log
  del run más reciente (run 31943677402, 2026-08-16):
  1. RSS: IICA (`iica.int/es/rss/noticias`) y La Prensa (`prensa.com/feed/`) devuelven
     "0 entradas en el feed" — la request HTTP no falla, pero el parser no encuentra
     items. No se pudo verificar el contenido real del feed en esta sesión (el proxy
     de red de este entorno bloquea egress a iica.int y prensa.com) — pendiente de
     inspección directa en una sesión con acceso de red sin restricciones.
  2. DDG búsqueda web: de 8 queries configuradas, 7 (oirsa.org, mida.gob.pa,
     idiap.gob.pa, bda.gob.pa, fao.org, bancomundial.org, iica.int) devuelven
     "No results found." — solo `site:prensa.com` devolvía resultados, y eran los
     falsos positivos ya documentados arriba (ahora corregidos por el fix de dominio).
  3. GDELT: las ventanas 2015-01-01→2017-03-29 (7 ventanas) fallan con "GET blocked
     (403/429)" en cada corrida — GitHub Actions IPs ya no están exentas del bloqueo
     de GDELT como asumía el comentario en `wiki_daily.yml`. Las ventanas 2017-2026
     (33 ventanas) ya están completas (`ya descargado`). La ventana viva actual
     (2026-06-18 → 2026-08-15) SÍ responde sin error pero devuelve "0 artículos" —
     posible indicio de que el query GDELT (`sourcecountry:PA` + términos agro) es
     demasiado restrictivo para la cobertura reciente, o que simplemente no hay
     coincidencias en esa ventana.
  4. World Bank API corre sin error pero no se ven artículos nuevos guardados de esa
     fuente tampoco.

  **Conclusión**: el pipeline de fetch no está muerto, pero cada una de sus 4 fuentes
  (RSS, DDG, GDELT, WorldBank) está degradada simultáneamente. El fix de DDG aplicado
  hoy debería reducir falsos positivos en la próxima corrida, pero no resolverá el
  problema de "0 artículos nuevos" por sí solo — persisten: RSS feeds sin verificar,
  GDELT bloqueado en ventanas 2015-2017, y DDG sin resultados en 7/8 queries oficiales.
  **Próximos pasos recomendados**: (a) verificar manualmente si las URLs de RSS
  cambiaron (iica.int, prensa.com) desde una red sin restricciones de egress;
  (b) considerar un backoff/retry más largo para GDELT en vez de reintentar ventanas
  bloqueadas en cada corrida diaria (desperdicia ~6 min de cada run); (c) revisar si
  las queries DDG con `site:` a dominios .gob.pa necesitan ajuste de sintaxis.
