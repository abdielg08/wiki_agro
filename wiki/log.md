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

## 2026-08-11 00:00
ROUTINE: Sesión de mantenimiento — 16 pendientes revisados, 0 artículos reales (0% falsos positivos preservado)

  **Falsos positivos identificados y documentados (16/16 pendientes)** — ninguno trata sobre
  agro panameño; todos llegaron a `sources/articles/` antes de que un fix previo (sesión
  2026-06-22) agregara el filtro `_is_panama_related`/`_is_blocked_domain` a `fetch_news.py`.
  Causa raíz: el término de alta prioridad "MIDA" en la query de GDELT colisiona con otras
  entidades del mundo que comparten la sigla — Malaysian Investment Development Authority
  y la Military Installation Development Authority de Utah — y GDELT etiqueta
  `sourcecountry:PA` de forma poco fiable para esos artículos.
    - paultan.org — MITI/MIDA Malasia, incentivos industriales (NO es Panamá)
    - sltrib.com ×4 — MIDA = Military Installation Development Authority, Utah (data centers, energía nuclear)
    - msn.com — "Cultural Rules for Staying with Locals Abroad" (menciona MIDA de Utah de pasada)
    - fox13now.com — ya documentado ingested previamente, mismo caso Utah MIDA
    - heraldo.es ×4 — Aragón, España (porcicultura, elecciones agrarias, Forestalia/Inaga)
    - spa.gov.sa — "Reef Saudi", agricultura de secano en Arabia Saudita
    - agenciabrasil.ebc.com.br — Finep, agricultura familiar en Brasil
    - whc.unesco.org — sistema qanat persa (Irán), patrimonio UNESCO
    - nyfb.org — New York Farm Bureau (EE.UU.)
    - ieeexplore.ieee.org — paper técnico "Ambient IoT" agricultura de precisión (genérico, sin país)
    - archive.org — catálogo de dípteros de Sudamérica (Brasil, 1966/67), no es noticia agro

  Ninguno se ingestó al wiki (sin `wiki/summaries/`, `topics/` ni `entities/` nuevos), conforme
  a la Regla Crítica #9. Todos marcados `ingested: true` en `processed.json` vía
  `mark-ingested <url>` individual para que no vuelvan a aparecer en la cola.

  **Bugs encontrados y corregidos en `scripts/`:**
    1. `scripts/ingest.py::mark_ingested()` — iteraba `processed.items()` sin filtrar la clave
       interna `_gdelt_windows` (una lista, no un dict), causando `AttributeError` en TODO
       intento de `mark-ingested <url>` — el flujo documentado en `pending_ingest.md`. Fix:
       usar `article_entries(processed)`.
    2. `scripts/ingest.py::mark_all_ingested()` — usaba `find_pending()` (orden por nombre de
       archivo) mientras `ingest`/`run_prepare` usa `prioritize()` (orden por score). Con
       `--limit N` ambos comandos operaban sobre subconjuntos DISTINTOS de artículos: esta
       sesión detectó 4 artículos marcados `ingested: true` sin haber sido revisados jamás
       (nunca mostrados a Claude). Se revirtieron a `ingested: false` y se corrigió
       `mark_all_ingested()` para usar el mismo orden por score que `run_prepare()`.
    3. `scripts/fetch_historical.py::fetch_gdelt_window()` (crawler histórico manual, workflow
       "Crawl Histórico 15 Años") no aplicaba el filtro de relevancia Panamá que sí tiene
       `fetch_news.py::fetch_gdelt_historical()` (el fetcher diario). Se agregó
       `_is_panama_related`/`_is_blocked_domain` para prevenir que futuras corridas manuales
       reintroduzcan el mismo tipo de falso positivo.

  **Diagnóstico del fetch (Paso 4):**
    - Último commit de `sources/` con cambios: 2026-08-10 (`0 artículos nuevos descargados`).
      Commits de `sources/` en los últimos 7 días: 08-04, 08-07, 08-10 — no diario pese al
      cron `0 11 * * *`; posible espaciado por baja actividad del repo en GitHub Actions.
    - `sources/processed.json["_gdelt_windows"]`: 64 ventanas completadas (más que el
      estimado de 45), pero la ventana más antigua es `20170330_20170628`. El rango
      2015-01-01 → 2017-03-29 configurado en `config/sources.yaml` (gdelt.date_range.start)
      **nunca se ha escaneado** — hueco real en el backfill histórico objetivo 2015→hoy.
      Recomendación: disparar manualmente el workflow "Crawl Histórico 15 Años" con
      `--years 2015-2017` para cerrar el hueco (no se disparó en esta sesión: es una acción
      potencialmente larga (horas) en CI, se deja para decisión explícita del usuario/próxima
      sesión).
    - GDELT no es alcanzable desde este entorno de sesión (solo desde IPs de GitHub Actions,
      como documenta el propio workflow) — no se pudo intentar fetch manual aquí.

  Total artículos ingestados (acumulado): 13 → 29 (todos falsos positivos ya existentes en cola)
  Pendientes al cierre: 0
  Páginas wiki: sin cambios (20 — 8 topics, 3 entities, 6 summaries, 3 overview)

## 2026-08-11 08:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code
