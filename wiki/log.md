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

## 2026-08-12 08:03
FALSOS POSITIVOS: 5/5 artículos del lote ingest --limit 5 rechazados — 0% falsos positivos en el wiki
  Causa raíz: colisión de acrónimo "MIDA" — la fuente prensa.com (agregador que replica contenido
  de sltrib.com, paultan.org y msn.com) trajo artículos sobre MIDA = "Military Installation
  Development Authority" (Utah, EE.UU.) y MIDA = agencia de MITI (Malasia), no MIDA = Ministerio
  de Desarrollo Agropecuario de Panamá. Ninguno trata temas agropecuarios panameños.
  Artículos rechazados (NO se creó contenido en wiki/):
    - 20260708_prensacom_2026-07-07-miti-working-on-simplified-ncm-customised-incenti.json
      → "MITI working on simplified NCM..." — Malasia, industria/inversión, sin relación agro-PA
    - 20260519_prensacom_news-2026-05-19-kevin-oleary-data-center-timeline.json
      → Utah MIDA (Military Installation Development Authority) — centro de datos, no agro
    - 20260527_prensacom_news-2026-05-27-box-elder-data-center-opponents.json
      → Utah MIDA — oposición a centro de datos, no agro
    - 20260529_prensacom_news-environment-2026-05-29-utah-governor-issues-order-prote.json
      → Utah MIDA — calidad de aire/agua, no agro Panamá
    - 20260307_prensacom_en-us-news-other-cultural-rules-for-staying-with-locals-abro.json
      → "Cultural Rules For Staying With Locals Abroad" — artículo de viajes, mención tangencial a MIDA (Utah)
  Acción: marcados como ingested=true en processed.json vía mark-all-ingested para despejar la cola
  (ya fueron evaluados y descartados; no requieren reproceso). Notificar al usuario: revisar el
  scraper de la fuente prensa.com — probablemente está indexando resultados de búsqueda genéricos
  por keyword "MIDA" sin filtro geográfico Panamá, contaminando la cola de pendientes.
  Fuentes con cobertura: MIDA (2), TVNNoticias (1), LaPrensaEco (1), BDA (1), IICA (1)

## 2026-08-12 08:03 (corrección)
NOTA: La línea de log automática "INGEST: 5 artículos marcados..." generada tras la primera
llamada a `mark-all-ingested --limit 5` fue revertida (`git checkout -- sources/processed.json`)
porque ese comando tenía un bug (ver entrada BUGFIX abajo): marcó 5 artículos *distintos* a los
5 realmente evaluados en este lote (por orden de archivo, no por score). Los 5 artículos correctos
del lote 1 se re-marcaron individualmente vía `mark-ingested <url>` — ver entrada de arriba.

## 2026-08-12 09:00
BUGFIX: 2 bugs corregidos en scripts/ingest.py y scripts/fetch_news.py
  1. `mark_ingested()` (individual) crasheaba con AttributeError al iterar `processed.items()`
     directamente — la clave interna `_gdelt_windows` (una lista) no tiene `.get()`. Corregido
     para usar `article_entries(processed)` (ya existía y filtra claves `_meta`).
  2. `mark_all_ingested()` usaba `find_pending()` en orden alfabético de archivo, pero `ingest`
     (run_prepare) selecciona por score de prioridad — dos órdenes distintas. Resultado: el paso
     4 de la routine (`mark-all-ingested --limit 5`) marcaba artículos DIFERENTES a los 5 que
     realmente se mostraron en pending_ingest.md y se evaluaron. Corregido para usar
     `prioritize(strategy="score")`, igual que `run_prepare`.
  3. Causa raíz de por qué TODA la cola pendiente (11/11) resultó ser falsos positivos: la
     búsqueda web `prensa_agro` en config/sources.yaml usa `site:prensa.com` vía DDG news search,
     pero DDG no respeta el operador `site:` de forma confiable — devolvía resultados de dominios
     no relacionados (sltrib.com, heraldo.es, archive.org, ieeexplore.ieee.org, nyfb.org,
     whc.unesco.org, spa.gov.sa, agenciabrasil.ebc.com.br) etiquetados incorrectamente como
     `source: prensa.com` y `country: PA`. Además, el filtro `is_agro_relevant()` solo exige
     términos agro genéricos ("MIDA", "agricultura", "cosecha") sin exigir mención de Panamá,
     por lo que coincidencias de acrónimo (MIDA = Military Installation Development Authority
     en Utah) o agro global (Aragón/España, Reef Saudi, Finep/Brasil) pasaban el filtro.
     Corregido: `fetch_ddg_search()` ahora descarta cualquier resultado cuyo dominio no coincida
     exactamente con el `site` configurado.

## 2026-08-12 09:05
FALSOS POSITIVOS: 11/11 artículos restantes de la cola rechazados — 0% falsos positivos en el wiki
  Todos con country=PA (mal etiquetado) pero 0 menciones de "Panam" en título/texto/resumen.
  Rechazados (NO se creó contenido en wiki/):
    - https://www.heraldo.es/noticias/economia/2025/11/25/aragon-celebra-... (Aragón, España — regulación porcina)
    - https://www.sltrib.com/news/environment/2025/06/12/utah-nuclear-energy-state/ (Utah MIDA — energía nuclear)
    - https://www.heraldo.es/noticias/economia/2026/06/23/arvensis-agro-amplia-... (Aragón, España — nutrición vegetal)
    - https://www.spa.gov.sa/en/N2096157 (Arabia Saudita — "Reef Saudi")
    - https://agenciabrasil.ebc.com.br/economia/noticia/2026-07/finep-vai-pagar-... (Brasil — Finep)
    - https://whc.unesco.org/en/list/1506 (UNESCO — Persian Qanat, Irán)
    - https://www.heraldo.es/noticias/economia/2026/06/08/aega-pide-elecciones-... (Aragón, España)
    - https://www.nyfb.org/ (New York Farm Bureau, EE.UU.)
    - https://www.heraldo.es/noticias/aragon/2026/05/03/luis-biendicho-vox-asume-... (Aragón, España)
    - https://ieeexplore.ieee.org/document/10945742 (IEEE — Ambient IoT, paper técnico genérico)
    - https://archive.org/details/Cataloguedipter2SaoP (archive.org — catálogo de dípteros, 1937)
  Acción: marcados como ingested=true en processed.json vía mark-ingested (ya evaluados y
  descartados individualmente; no requieren reproceso). Con el fix de dominio en fetch_news.py,
  la próxima corrida de GitHub Actions no debería volver a traer este tipo de ruido desde
  `prensa_agro`. Recomendación al usuario: revisar si la fuente `prensa_agro` (DDG site search)
  vale la pena mantener — con el fix de dominio, es posible que ahora devuelva 0 resultados si
  DDG nunca indexa bien prensa.com vía site:; considerar reemplazarla por scraping directo del
  feed/sección agropecuaria de prensa.com si existe.

## 2026-08-12 08:11
INGEST: 0 artículos marcados como ingestados por sesión Claude Code
