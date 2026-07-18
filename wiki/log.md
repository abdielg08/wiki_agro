---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-18
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

## 2026-07-18 00:00
FALSOS POSITIVOS: 5/5 artículos del batch de ingesta NO son sobre agro panameño — NO ingestados
  Causa raíz: colisión de siglas. El fetcher (fuente "prensa.com" en processed.json,
  pero URLs reales fuera de dominio prensa.com) captura resultados de búsqueda por
  keyword "MIDA"/"MITI" que matchean con:
    - MIDA = Malaysian Investment Development Authority (Malasia)
    - MIDA = Military Installation Development Authority (Utah, EE.UU.)
    - MITI = Ministry of Investment, Trade and Industry (Malasia)
  Artículos rechazados:
    - "MITI working on simplified NCM..." (paultan.org, Malasia — automotriz/industria)
    - "Box Elder data center opponents..." (sltrib.com, Utah — centros de datos)
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, Utah — ambiente)
    - "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com, Utah — centros de datos)
    - "Utah wants to process uranium on the Wasatch Front..." (sltrib.com, Utah — energía nuclear)
  Ninguno menciona Panamá, MIDA (Ministerio de Desarrollo Agropecuario) ni agro panameño.
  Acción: marcados como ingested=true vía mark-all-ingested para vaciar la cola de
  pendientes (0% falsos positivos en el wiki es la política — no se creó ninguna página).
  RECOMENDACIÓN: revisar/ajustar el filtro de keywords del fetcher (scripts/fetch*.py)
  para excluir resultados donde "MIDA"/"MITI" no vengan acompañados de contexto
  panameño (dominio .pa, "Panamá", "Ministerio de Desarrollo Agropecuario", etc.).

## 2026-07-18 01:05
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-18 01:20
BUG ENCONTRADO Y CORREGIDO: mark-all-ingested marcaba artículos incorrectos
  Síntoma: al ejecutar `mark-all-ingested --limit 5` sobre el batch de 5 falsos
  positivos (MITI/MIDA Malasia + 4 artículos de Utah), se marcó como ingested=true
  un artículo NUNCA mostrado a Claude (https://ieeexplore.ieee.org/document/10945742,
  fuente etiquetada "prensacom") — mientras que el artículo MITI/paultan.org, que sí
  fue revisado y documentado como falso positivo, quedó sin marcar.
  Causa raíz: `mark_all_ingested()` (scripts/ingest.py) recomputaba "los primeros N
  pendientes" con `find_pending()` (orden alfabético por nombre de archivo), mientras
  que `ingest` (scripts/ingest.py:run_prepare → prioritize()) selecciona y muestra el
  batch ordenado por score de relevancia. Ambos órdenes difieren, así que
  mark-all-ingested podía marcar un artículo distinto al que Claude realmente revisó
  — dejando un artículo sin revisar marcado como ingestado (integridad de la cola rota)
  y uno sí revisado (falso positivo documentado) sin marcar (reaparecería en el
  siguiente batch).
  Corrección aplicada:
    - scripts/ingest.py: run_prepare() ahora persiste el batch exacto de URLs
      mostrado a Claude en pending_ingest_batch.json.
    - scripts/ingest.py: mark_all_ingested() ahora consume ese archivo (marca
      exactamente lo que se mostró) en vez de recomputar find_pending() de forma
      independiente; conserva el comportamiento anterior como fallback si el
      archivo no existe.
    - sources/processed.json: corregido manualmente — ieeexplore.ieee.org/document/10945742
      revertido a ingested=false (nunca fue revisado); paultan.org (MITI) marcado
      ingested=true (sí fue revisado y documentado como falso positivo arriba).
  También corregido en el mismo commit: scripts/fetch_news.py `fetch_ddg_search()`
  no aplicaba los filtros `_is_blocked_domain`/`_is_panama_related` que sí tiene
  `fetch_rss()` — causa raíz de por qué estos falsos positivos entraron al pipeline.

## 2026-07-18 01:30
FALSOS POSITIVOS: 4/4 artículos restantes del batch NO son sobre agro panameño — NO ingestados
  Mismo origen (fuente etiquetada "prensa.com" mal atribuida — ver bug de arriba):
  DDG web search "prensa_agro" sin filtro geográfico devolvió contenido agrícola
  genérico de sitios no panameños.
  Artículos rechazados (ninguno menciona Panamá):
    - "The Persian Qanat" (whc.unesco.org — sitio patrimonial de Irán)
    - "New York Farm Bureau" (nyfb.org — gremio agrícola de Nueva York, EE.UU.)
    - "'Reef Saudi', a Successful Program..." (spa.gov.sa — programa agrícola de Arabia Saudita)
    - "Ambient IoT: Communications Enabling Precision Agriculture" (ieeexplore.ieee.org —
      paper académico sobre 6G/IoT, sin referencia geográfica específica)
  Acción: marcados como ingested=true vía mark-all-ingested (ahora usando
  pending_ingest_batch.json, ver fix arriba) para vaciar la cola. No se creó
  ninguna página de wiki.

## 2026-07-18 01:07
INGEST: 4 artículos marcados como ingestados por sesión Claude Code

## 2026-07-18 01:40
DIAGNÓSTICO AVANZADO: 0 artículos nuevos en sources/ desde 2026-07-15 (3 días)
  Señal de alarma activada: CLAUDE.md define "3 días consecutivos sin nuevos
  artículos en sources/articles/" como fallo del sistema.
  Investigación (GitHub Actions vía mcp__github, workflow "Wiki Agropecuario —
  Fetch Diario", cron diario 11:00 UTC):
    - Runs recientes: 2026-07-17 success/0 artículos, 2026-07-16 success/0,
      2026-07-15 success/1 (último commit real a sources/), 2026-07-14 success,
      2026-07-13 FAILURE, resto success. El workflow SÍ está corriendo a diario.
    - Logs del job 2026-07-17 (run 29578858522): GDELT API devuelve
      "GET blocked (403/429)" o "error de red" en prácticamente todas las
      ventanas intentadas, INCLUYENDO la ventana incremental más reciente
      (2026-06-18 → 2026-07-16) — la única que traería noticias nuevas de
      Panamá. No es agotamiento del rango de fechas: sources/processed.json
      tiene 49 ventanas GDELT trimestrales ya completadas (>45, cubre 2015→2026
      casi en su totalidad — el backfill histórico masivo está esencialmente
      terminado). El problema es que GDELT está bloqueando/rate-limiteando la
      IP del runner de GitHub Actions.
    - RSS (IICA, La Prensa): 0 entradas en el feed ese día — feeds vacíos, sin
      error HTTP, probablemente día sin publicaciones nuevas.
    - DDG web search: 7/8 búsquedas "site:X ..." devuelven "No results found"
      (normal). Solo "prensa_agro" (site:prensa.com) trae resultados, y por un
      bug en fetch_ddg_search() (corregido arriba, ver 01:20) esos resultados
      no pasaban por el filtro de dominio/Panamá — origen de los 9 falsos
      positivos de esta sesión.
  Conclusión: el pipeline de fetch funciona correctamente a nivel de código;
  la causa raíz de "0 artículos nuevos" es bloqueo externo de la API de GDELT
  (403/429), no un bug del repo. No hay fix de código aplicable desde esta
  sesión para el bloqueo de GDELT en sí — es un problema de rate-limit/IP
  externo a la propia API. Recomendación para próxima sesión: si el bloqueo
  persiste más de 5-7 días, evaluar backoff/retry más largo en
  fetch_gdelt_window() (scripts/fetch_historical.py) o reducir la frecuencia
  de la ventana incremental diaria.
  wiki/metrics.md actualizado con el detalle completo de este diagnóstico.
