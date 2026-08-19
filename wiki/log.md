---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-19
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

## 2026-08-19 (routine automática)
FALSOS POSITIVOS: 16/16 artículos pendientes eran falsos positivos — 0 ingestados al wiki

`python wiki_agro.py stats` mostró 16 pendientes. Los 5 del lote de `ingest --limit 5`
(y, tras auditar el resto de la cola, los 11 restantes) resultaron ser 100% ajenos al
agro panameño. Ninguno se ingestó al wiki — se marcaron `ingested: true` en
`processed.json` (vía `mark-ingested`) para vaciar la cola sin contaminar el wiki,
tal como indica la Regla Crítica #9 de CLAUDE.md.

Artículos descartados (16):
  - MITI/MIDA Malasia (paultan.org) — "MIDA" = Malaysian Investment Development Authority
  - 4x Salt Lake Tribune / MSN Utah — "MIDA" = Utah Military Installation Development Authority
    (data centers de Kevin O'Leary, Great Salt Lake, uranio)
  - Saudi Press Agency (spa.gov.sa) — programa "Reef Saudi" de agricultura de secano en Arabia Saudita
  - NY Farm Bureau (nyfb.org) — agricultura de Nueva York, EE.UU.
  - UNESCO (whc.unesco.org) — "The Persian Qanat", patrimonio de Irán
  - IEEE Xplore — paper académico de IoT en agricultura de precisión, sin país específico
  - archive.org — catálogo de dípteros de las Américas (entomología, 1900s)
  - 4x Heraldo.es — agricultura y medio ambiente en Aragón, España
  - Agência Brasil — financiamiento Finep a agricultura familiar en Brasil
  Ninguno mencionaba a Panamá en el título, URL ni full_text (verificado con grep).

CAUSA RAÍZ identificada en `scripts/fetch_news.py`:
  `fetch_ddg_search()` (fuente DDG usada para prensa.com, oirsa.org, mida.gob.pa, etc.)
  NO tenía el filtro `_is_panama_related()` / `_is_blocked_domain()` que sí tienen
  `fetch_rss()` y `fetch_gdelt_batch()`. Solo validaba `is_agro_relevant()` (palabras
  clave genéricas de agro + "MIDA"), así que cualquier resultado de DuckDuckGo con
  "MIDA" o "agricultura" en cualquier país colaba, y además se etiquetaba con
  `source="prensa.com"` y `country="PA"` sin verificar el dominio real. Esto
  contaminó el 100% de la cola de pendientes acumulada en sesiones recientes.

FIX aplicado (scripts/fetch_news.py, fetch_ddg_search):
  Se agregó el mismo guard que ya usan fetch_rss/fetch_gdelt_batch: rechazar
  dominios de la blocklist (_is_blocked_domain) y exigir al menos un término
  panameño en título/URL/cuerpo (_is_panama_related) antes de aceptar el
  resultado. Efecto esperado: 0 falsos positivos nuevos desde la fuente DDG
  en la próxima corrida de GitHub Actions.

FIX adicional (scripts/ingest.py, mark_ingested):
  `mark_ingested()` iteraba `processed.items()` crudo e intentaba `.get()` sobre
  la clave interna `_gdelt_windows` (una lista), causando `AttributeError` y
  abortando el comando. Se corrigió para iterar solo `article_entries(processed)`,
  igual que ya hacía `mark_all_ingested()`. Sin este fix no se podía marcar
  ningún artículo individual como ingestado.

DIAGNÓSTICO — backfill GDELT (Paso 4, avanzado):
  `_gdelt_windows` en processed.json tenía 70 entradas, pero solo 38 son
  ventanas trimestrales reales y distintas (2017-03-30 → 2026-03-19). Las
  otras 33 eran variantes casi-duplicadas de una sola ventana "abierta"
  (`20260618_202608XX`, una clave nueva cada día). Causa: en
  `fetch_gdelt_historical()`, `end = min(config_end, ayer)` — y como
  `config.gdelt.date_range.end = "2027-12-31"` (futuro), el límite efectivo
  siempre es "ayer", que avanza cada día, generando una clave de ventana
  distinta en cada corrida sin volver a marcarse como completada de forma
  estable. FIX aplicado: la ventana final ya no se agrega a
  `completed_windows` mientras esté acotada por "ayer" en vez de un límite
  fijo — se re-consulta cada día hasta que cierre en un borde trimestral
  real, sin inflar el contador de ventanas.

  Cobertura real de GDELT: 2017-03-30 → hoy. Falta el tramo 2015-02-19 →
  2017-03-29 (~8 trimestres) — nunca aparece en `_gdelt_windows`, lo que
  sugiere que esas ventanas tempranas fallan de forma persistente (no es
  un simple "45+ ventanas = agotado" como asume CLAUDE.md; el conteo
  bruto de 70 era engañoso por el bug de arriba). No se pudo probar en
  vivo: este sandbox no tiene salida de red a api.gdeltproject.org
  (ProxyError 403) — GDELT solo funciona desde runners de GitHub Actions,
  como ya documentaba CLAUDE.md. Pendiente: revisar el log de la próxima
  corrida de Actions para ver si esas 8 ventanas tempranas devuelven error
  HTTP, 0 resultados, o timeout.

  Última corrida de Actions con commit a sources/: 2026-08-17 (0 artículos
  nuevos). Último día con artículos genuinamente nuevos: 2026-07-30 (3).
  Han pasado 20 días sin artículos nuevos reales — muy por encima del
  umbral de 3 días de CLAUDE.md. Combinado con el hallazgo de arriba, la
  causa más probable es la fuente DDG (ahora corregida) más el tramo GDELT
  2015-2017 sin cubrir.

RESULTADO de la sesión: `python wiki_agro.py stats` → 29 descargados,
  29 marcados como "ingestados" (13 reales de sesiones previas + 16 falsos
  positivos de esta sesión, procesados sin agregar contenido al wiki),
  0 pendientes. Sin páginas nuevas en wiki/topics ni wiki/entities (no
  había contenido legítimo que ingestar esta sesión — la cola completa
  era contaminación). 0% falsos positivos ingestados al wiki — mantenido.

## 2026-08-19 08:20
LINT: 20 páginas revisadas, 54 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:41, stale:11, no_index:1
