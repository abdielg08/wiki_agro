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

## 2026-08-11 00:03
ROUTINE: 5 artículos pendientes revisados — 5/5 FALSOS POSITIVOS (0 ingestados)
  Causa raíz: colisión de keyword "MIDA" — el query de scraping matchea la sigla
  "MIDA" sin verificar la entidad. Los 5 artículos son sobre:
    - MITI/MIDA Malasia (Malaysian Investment Development Authority) —
      "MITI working on simplified NCM customised incentive mechanism..." (paultan.org)
    - MIDA Utah (Military Installation Development Authority) — 3 artículos sobre
      el data center de Kevin O'Leary en Box Elder County, Utah (sltrib.com):
      "Kevin O'Leary data center timeline", "Box Elder data center opponents",
      "Utah Gov. Cox issues order to protect Great Salt Lake"
    - Artículo de viajes sin relación agro ("Cultural Rules For Staying With
      Locals Abroad", msn.com) que menciona la demanda contra MIDA Utah de pasada
  Nota: los 5 artículos tienen metadata `country: "PA"` incorrecta en
  sources/articles/*.json — ninguno es sobre Panamá. No se creó ninguna página
  wiki ni se modificó sources/. Marcados como ingestados vía mark-all-ingested
  para vaciar la cola de pendientes (no se re-evaluarán).
  Ningún artículo agregado al wiki en esta sesión — tasa de falsos positivos
  del lote: 100%.

## 2026-08-11 00:05
DIAGNÓSTICO (Paso 4/5 — pendientes llegó a 0 tras marcar los 5 falsos positivos):
  - Artículos nuevos en sources/articles/ HOY (2026-08-11): 0
  - Último commit a sources/: 2026-08-10 "0 artículos nuevos descargados"
    (commits previos: 2026-08-07, 2026-08-04)
  - Ventanas GDELT completadas: 64 (`_gdelt_windows` en processed.json).
    Inspección detallada de las claves revela DOS problemas distintos, no
    "rango agotado":
    1) GAP HISTÓRICO REAL 2015-01-01 → 2017-03-29 (9 trimestres) — ninguna
       ventana de ese rango aparece en `_gdelt_windows`. La ventana más
       antigua completada es `20170330_20170628`. Como `fetch_gdelt_historical()`
       (scripts/fetch_news.py) solo marca una ventana completa tras una
       respuesta HTTP exitosa, y en error de red avanza `current` SIN marcarla
       completa, esto indica que GDELT falla consistentemente para consultas
       muy antiguas (2015-2017) en cada corrida, sin nunca tener éxito — el
       backfill de esos 9 trimestres está efectivamente bloqueado, no
       completado.
    2) VENTANAS DUPLICADAS/SOLAPADAS cerca del presente: 27 ventanas
       distintas todas con inicio fijo `20260618` y fin creciente día a día
       (`20260618_20260623` … `20260618_20260809`). Causa: una vez que
       `current` llega a 2026-06-18, `next_q = min(current+90d, end)` con
       `end = ayer` — como `ayer` está a menos de 90 días de `current`,
       `next_q` = `end` cada vez. Cada corrida diaria genera una window_key
       nueva (el fin cambia), así que nunca coincide con una ya completada
       y se re-consulta casi el mismo rango cada día sin que `current` avance
       nunca más allá de 2026-06-18. Efecto: cuota de GDELT gastada en
       re-consultas mayormente duplicadas (deduplicadas por URL al guardar),
       lo cual explica el patrón de "0 artículos nuevos" en la mayoría de
       corridas — no es que no haya noticias, es que se re-piden las mismas.
  - RSS activos (IICA, La Prensa): no produjeron artículos nuevos en las
    últimas 3 corridas registradas.
  Conclusión: el pipeline corre según cron (0 11 * * *) pero NO está
  avanzando el backfill histórico 2015-2017 (bloqueado por error de red
  persistente en GDELT para fechas muy antiguas) y desperdicia llamadas
  re-consultando el mismo rango 2026-06-18→hoy cada día por un bug de
  cálculo de ventana cuando `current` queda a menos de 90 días de `end`.
  Recomendado para próxima sesión de desarrollo (fuera del alcance de esta
  rutina de ingesta): en `fetch_gdelt_historical()` (scripts/fetch_news.py),
  (a) marcar/loggear explícitamente los reintentos fallidos de 2015-2017
  para diagnosticar si es bloqueo de GDELT por antigüedad de fecha o rate
  limit, y (b) cuando `next_q == end` y `end - current < 90d`, no generar
  una nueva window_key cada día — usar una ventana "cola abierta" separada
  (ej. `_gdelt_last_seen_date`) en vez de re-derivar el rango completo desde
  `current` fijo. RSS: agregar fuentes Nivel 3 adicionales (Panamá América,
  TVN, La Estrella) para aumentar señal diaria independiente de GDELT.

## 2026-08-11 00:10
FIX + BUGS ENCONTRADOS en herramientas de ingesta (scripts/ingest.py):
  1. `mark-all-ingested --limit N` NO marca los mismos N artículos que
     `ingest --limit N` mostró: `find_pending()` (usado por mark-all-ingested)
     ordena por nombre de archivo, mientras que `run_prepare()` (usado por
     `ingest`) ordena por `prioritize()` (score). Al correr
     `mark-all-ingested --limit 5` tras revisar los 5 de pending_ingest.md,
     se marcaron 5 artículos DISTINTOS y nunca revisados (incluyendo uno
     potencialmente relevante: "Ambient IoT: Communications Enabling
     Precision Agriculture"). Se detectó antes de commitear, se revirtió
     `sources/processed.json` con `git checkout`, y se corrigió usando
     `mark-ingested <url>` individual para cada una de las 5 URLs
     efectivamente revisadas (las mismas que pending_ingest.md lista al
     final). Los 4 artículos afectados por el bug (incluido el de IoT)
     siguen `ingested: false` y quedan pendientes para revisión real en la
     próxima sesión.
  2. `mark-ingested <url>` (individual) estaba roto: iteraba
     `processed.items()` directamente, y como `processed["_gdelt_windows"]`
     es una lista (no dict), `meta.get("path", "")` lanzaba
     `AttributeError`. Corregido en scripts/ingest.py para usar el helper
     existente `article_entries(processed)` (ya usado en otras partes del
     código), que filtra las claves internas `_`-prefijadas.
  Recomendación: no confiar en `mark-all-ingested --limit N` para marcar
  exactamente los artículos mostrados por `ingest --limit N` hasta que
  ambos usen el mismo criterio de orden (`prioritize()`); usar
  `mark-ingested <url>` por artículo mientras tanto.
