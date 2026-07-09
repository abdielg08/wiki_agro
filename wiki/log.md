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

## 2026-07-09 00:00
ROUTINE: 6 artículos pendientes revisados — 6/6 falsos positivos, 0 ingestados
  Ninguno califica como "100% sobre agro de Panamá" — no se crearon páginas wiki:
    - sltrib.com/.../kevin-oleary-data-center-timeline (2026-05-19): centro de datos en Utah;
      "MIDA" = Military Installation Development Authority (Utah), no Ministerio panameño
    - sltrib.com/.../box-elder-data-center-opponents (2026-05-27): mismo caso, oposición local a MIDA (Utah)
    - sltrib.com/.../utah-governor-issues-order-protect (2026-05-29): orden del gobernador de Utah sobre
      calidad de aire/Great Salt Lake y centros de datos; menciona MIDA (Utah)
    - sltrib.com/.../utah-nuclear-energy-state (2025-06-13): procesamiento de uranio en Utah;
      menciona MIDA (Military Installation Development Authority, Utah)
    - spa.gov.sa/en/N2096157 (2026-06-24): programa "Reef Saudi" de agricultura de secano — agricultura
      real, pero de Arabia Saudita, no de Panamá
  Los 6 artículos se marcaron `ingested` vía `mark-all-ingested` para que no reaparezcan en
  `pending_ingest.md` (no porque se hayan procesado, sino porque ya fueron evaluados y descartados).

DIAGNÓSTICO — causa raíz de los falsos positivos (recurrente desde el fix del 2026-06-22):
  Los 6 artículos de hoy, y los 3 "artículos nuevos" que GitHub Actions trajo entre 2026-06-19 y
  2026-07-02 (documento IEEE, "New York Farm Bureau", "Utah nuclear energy"), son TODOS producto del
  mismo bug en `scripts/fetch_news.py::fetch_ddg_search()`:
    1. La búsqueda usa `site:{dominio} {keywords con OR}` (ej. `site:prensa.com ... OR MIDA ...`),
       pero la verticalidad "news" de DuckDuckGo (vía librería `ddgs`) no siempre respeta el operador
       `site:`, devolviendo resultados de dominios no relacionados cuando coinciden las keywords.
    2. El código etiquetaba `"source": site` (el dominio configurado) sin verificar el dominio real
       de la URL devuelta — por eso todo aparecía como "prensa.com" aunque viniera de sltrib.com,
       spa.gov.sa, thestar.com.my, fox13now.com, worldbank.org o ieeexplore.ieee.org.
    3. El filtro `is_agro_relevant()` hace *substring match* simple sobre términos genéricos
       ("MIDA", "cultivo", "agricultura", "cosecha") sin exigir contexto de Panamá, así que coincide
       con "MIDA" (Utah, Malasia) y con agricultura de cualquier país.
  Resultado: desde el fix del 2026-06-22 (17 días), CERO artículos reales nuevos han entrado al
  pipeline — el 100% de lo que trajo el fetch automático fueron falsos positivos de este bug.
  Esto viola la métrica de "avance medible: ≥1 artículo nuevo por día hábil".

FIX APLICADO: `scripts/fetch_news.py::fetch_ddg_search()` ahora valida que el dominio real de la URL
  devuelta coincida con el `site` configurado antes de aceptar el resultado; si no coincide, se
  descarta silenciosamente. Esto debería eliminar esta fuente de falsos positivos en las próximas
  corridas de GitHub Actions. Las fuentes RSS (IICA, La Prensa) no se ven afectadas por este bug.

DIAGNÓSTICO — cobertura GDELT: 47 ventanas trimestrales completadas, cubriendo 2017–2026 sin
  interrupciones. Los años 2015–2016 (objetivo real: 2015-02-19 en adelante) NO tienen ninguna
  ventana completada — indica que esas ventanas fallan consistentemente (error de red/timeout) en
  cada corrida y nunca llegan a marcarse como completas, bloqueando el backfill histórico temprano.
  Pendiente investigar por qué GDELT falla específicamente para 2015-2016 (posible límite de la API
  para fechas muy antiguas).

## 2026-07-09 19:25
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-09 19:25
INGEST: 1 artículos marcados como ingestados por sesión Claude Code
