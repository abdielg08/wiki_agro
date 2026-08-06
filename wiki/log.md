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

## 2026-08-06 08:05
DIAGNÓSTICO: 5 falsos positivos detectados y rechazados (0 ingestados al wiki)
  Los 5 artículos del batch pending_ingest.md (fuente: prensa.com) resultaron ser
  colisiones de keyword "MIDA"/"MITI" NO relacionadas con Panamá:
    - MITI/MARii/MIDA (Malasia) — Ministry of Investment, Trade & Industry
    - Kevin O'Leary data center, Utah — MIDA = Military Installation Development Authority (Utah)
    - Box Elder data center opponents, Utah — mismo MIDA de Utah
    - Utah Gov. Cox, calidad del aire, data centers — mismo MIDA de Utah
    - Cultural Rules For Staying With Locals Abroad — menciona el MIDA de Utah en un litigio
  Los 5 artículos venían etiquetados country=PA, language=es a pesar de ser
  contenido en inglés sobre Malasia/Utah — indica un bug en el pipeline de
  fetch/tagging que está etiquetando mal el país de origen basado en la
  coincidencia de la sigla "MIDA" sin verificar el contexto geográfico.
  Acción: marcados ingested=true + false_positive=true en sources/processed.json
  (para no reprocesarlos), NO se creó contenido en wiki/. Tasa de falsos
  positivos se mantiene en 0% dentro del wiki (ningún falso positivo publicado).
  Recomendación: revisar scripts/fetch_news.py / fetch_historical.py para
  agregar verificación de dominio/país de la fuente antes de aceptar coincidencias
  de keyword como "MIDA".

## 2026-08-06 08:10
FIX: corregido bug de falsos positivos en fetch_ddg_search (scripts/fetch_news.py)
  Diagnóstico: los 16 artículos pendientes de esta sesión (ver entrada anterior
  y processed.json con false_positive=true) provenían todos de la fuente
  web_search "prensa_agro", que arma queries "site:prensa.com ..." para DDG
  News. El backend de DDG no respeta "site:" de forma confiable, y
  is_agro_relevant() sólo hacía substring match de términos genéricos sin
  validar dominio/geografía — permitiendo pasar artículos de Aragón (España),
  Utah (EEUU), Malasia, Brasil, Arabia Saudita, IEEE, archive.org y UNESCO,
  todos mal etiquetados como country=PA/source=prensa.com.
  Fix: fetch_ddg_search ahora compara el netloc real de cada resultado con el
  dominio configurado en `site` (config/sources.yaml → web_searches) y
  descarta cualquier resultado fuera de ese dominio antes de aceptarlo.
  Validado con `python3 -m py_compile scripts/fetch_news.py`.
  Pendiente: confirmar en la próxima corrida de GitHub Actions que
  prensa_agro deja de producir falsos positivos.
  Nota adicional: ventanas GDELT completadas = 62, superando la estimación de
  ~45 en CLAUDE.md — sugiere que el rango de fechas 2015→hoy ya fue cubierto
  y conviene auditar/expandir la estrategia de backfill en la próxima sesión.
