---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-04
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

## 2026-07-04 08:04
INGEST: 6 artículos marcados como ingestados por sesión Claude Code

## 2026-07-04 08:10
FALSOS POSITIVOS: 6/6 artículos pendientes rechazados — 0 ingestados al wiki
  Los 6 artículos de `pending_ingest.md` NO son sobre agro panameño:
    1. sltrib.com — "Kevin O'Leary data center timeline" (Utah, EE.UU.)
    2. sltrib.com — "Box Elder data center opponents" (Utah, EE.UU.)
    3. sltrib.com — "Utah Gov. Cox... Great Salt Lake" (Utah, EE.UU.)
    4. sltrib.com — "Utah nuclear energy state" (Utah, EE.UU.)
    5. nyfb.org — "New York Farm Bureau" (EE.UU., no Panamá)
    6. spa.gov.sa — "Reef Saudi rain-fed agriculture" (Arabia Saudita)
  Ninguno se ingestó al wiki (sin summaries/topics/entities nuevos).
  Se marcaron `ingested: true` en processed.json (vía mark-all-ingested) para
  sacarlos de la cola de pendientes — no representan trabajo pendiente real.

  CAUSA RAÍZ IDENTIFICADA:
  `scripts/fetch_news.py::fetch_ddg_search()` construye la búsqueda DDG con
  `site:{site} {query}`, pero el operador `site:` de DuckDuckGo News no es
  estricto — puede devolver resultados de dominios no relacionados. Como el
  término "MIDA" está en `search_terms.primary` (para capturar noticias del
  Ministerio de Desarrollo Agropecuario de Panamá) y también es la sigla de
  la "Military Installation Development Authority" (Utah, EE.UU.) y de la
  "Malaysian Investment Development Authority" (Malasia), cualquier noticia
  en inglés que mencione esas agencias pasa el filtro `is_agro_relevant()`
  sin ninguna verificación de dominio o país. El código además etiquetaba
  ciegamente estos resultados como `source: prensa.com, country: PA,
  language: es` sin validarlo.

  Esto NO es un incidente aislado: el mismo bug ya había producido 7 falsos
  positivos detectados en la auditoría del 2026-06-22 (thestar.com.my x4 —
  Malasia, fox13now.com, worldbank.org genérico, ieeexplore.ieee.org), que
  quedaron marcados `ingested: true` sin nota en este log. Total acumulado
  de falsos positivos detectados hasta hoy: 13/19 artículos descargados (los
  6 restantes sí son agro-Panamá y están correctamente reflejados en
  wiki/summaries/).

  FIX APLICADO (este commit): `fetch_ddg_search()` ahora compara el
  `netloc` de cada URL resultado contra el `site` solicitado (con
  `urllib.parse.urlsplit`) y descarta cualquier resultado cuyo dominio no
  coincida, antes de aplicar `is_agro_relevant()`. Esto bloquea la
  contaminación por colisión del acrónimo "MIDA" (y similares) en fuentes
  no panameñas para todas las búsquedas DDG configuradas en
  `config/sources.yaml::web_searches` (prensa_agro, oirsa_alertas,
  mida_noticias, idiap_investigacion, bda_credito, fao_panama,
  banco_mundial_pa, iica_panama).

  DIAGNÓSTICO DE FETCH — HALLAZGO CRÍTICO: GitHub Actions (`wiki_daily.yml`)
  corre diariamente sin interrupciones (commits en sources/ casi cada día
  desde 05-24 hasta 07-03) — el cron SÍ está funcionando. Pero al revisar
  `saved_at` de los 13 artículos NO-semilla en processed.json, las 13
  descargas automáticas desde el 2026-05-30 hasta hoy (2026-07-04, 41 días)
  son TODAS falsos positivos — 0 artículos reales de agro panameño desde
  que se creó la semilla manual el 2026-05-24. El "avance medible" que
  exige CLAUDE.md (≥1 artículo nuevo/día hábil) llevaba 41 días sin
  cumplirse de forma encubierta, porque el conteo de "artículos nuevos"
  del workflow no distingue falsos positivos de contenido real.
  Ventanas GDELT completadas: 44 (cerca del límite estimado de ~45;
  revisar si el rango de fechas necesita expansión en la próxima sesión —
  posible causa adicional de por qué GDELT no está aportando contenido
  real y el pipeline depende de DDG, la fuente contaminada).
