---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-07-19
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

## 2026-07-19 00:00
FALSOS POSITIVOS: 5/5 artículos del lote de ingesta descartados — 0% ingestados
  Causa raíz: colisión de sigla "MIDA" — el filtro de fetch capturó artículos que
  mencionan "MIDA" pero refieren a organismos homónimos no panameños, no al
  Ministerio de Desarrollo Agropecuario de Panamá.
  Artículos descartados (NO ingestados al wiki):
    1. "MITI working on simplified NCM..." (paultan.org, 2026-07-08)
       → MIDA = Malaysian Investment Development Authority (agencia de MITI, Malasia)
    2. "Box Elder data center opponents..." (sltrib.com, 2026-05-27)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    4. "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.)
    5. "Utah wants to process uranium on the Wasatch Front..." (sltrib.com, 2025-06-13)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.)
  Ninguno trata sobre agro panameño — ninguno fue ingestado al wiki (tasa de
  falsos positivos del sistema: 0% innegociable, cumplida al rechazar los 5).
  Acción: marcados como procesados en processed.json (revisados y descartados)
  para que no vuelvan a aparecer en pending_ingest.md.
  RECOMENDACIÓN: el fetch (GDELT/RSS) debería excluir o desambiguar la sigla
  "MIDA" cuando el contexto geográfico no sea Panamá (ej. filtrar por dominio
  .pa, o exigir co-ocurrencia con términos como "Panamá", "agropecuario").

## 2026-07-19 00:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-19 00:10
BUG DETECTADO: `mark-all-ingested --limit N` usa un orden de selección
(find_pending, ordenado por nombre de archivo) DISTINTO al que usa
`ingest --limit N` (prioritize por score de relevancia). Consecuencia:
el comando anterior marcó como ingestado un artículo que nunca fue
revisado ("Ambient IoT: Communications Enabling Precision Agriculture",
ieeexplore.org, 2025-03-31) en vez del artículo MITI/NCM que sí fue
revisado y descartado como falso positivo — este quedó sin marcar y
reapareció en el siguiente lote de pending_ingest.md.
  Corrección aplicada en esta sesión: se revisó manualmente el artículo
  "Ambient IoT" (ya marcado ingested=true por el bug) — es un paper
  académico genérico sobre IoT/6G para agricultura de precisión, sin
  ninguna mención a Panamá. Se confirma como falso positivo (la marca
  ingested=true queda correcta en el resultado, aunque el proceso que
  la generó fue incorrecto). Se marcó el artículo MITI/NCM individualmente
  con `mark-ingested <url>` para no perderlo de la cola.
  RECOMENDACIÓN: `mark_all_ingested()` en scripts/ingest.py debería
  usar la misma función de priorización (`prioritize`) que `run_prepare()`,
  o mejor aún, recibir la lista exacta de artículos ya revisados por
  Claude Code en vez de re-derivar su propia selección.

## 2026-07-19 00:12
FALSOS POSITIVOS: 4/4 artículos del segundo lote descartados — 0% ingestados
  Ninguno trata sobre agro panameño:
    1. "MITI working on simplified NCM..." (paultan.org) — duplicado del
       lote anterior (Malasia, MIDA=Malaysian Investment Development
       Authority); marcado ahora individualmente vía mark-ingested.
    2. "The Persian Qanat" (whc.unesco.org, sitio UNESCO Irán) — sistema
       de riego ancestral persa, sin relación con Panamá.
    3. "New York Farm Bureau" (nyfb.org) — gremio agrícola de Nueva York,
       EE.UU., sin relación con Panamá.
    4. "'Reef Saudi', a Successful Program Based on Rain-Fed Agriculture"
       (spa.gov.sa) — programa de agricultura de secano de Arabia Saudita,
       sin relación con Panamá.
  Ninguno fue ingestado al wiki. Tasa de falsos positivos del sistema
  cumplida (0% ingestado incorrectamente).

## 2026-07-19 00:20
DIAGNÓSTICO AVANZADO: pendientes=0 tras esta sesión (todo el lote de 9 eran
falsos positivos). Se investigó el estado del fetch automático per Paso 4:

  1. ¿Corrió GitHub Actions hoy? NO hay commit de sources/ para 2026-07-19
     todavía. Últimos commits: 2026-07-18 (0 artículos nuevos), 2026-07-15
     (1 nuevo), 2026-07-14 (1 nuevo), 2026-07-10 (1 nuevo). Sin commits
     los días 2026-07-16 y 2026-07-17 (workflow no corrió o no hubo push).
  2. Días sin artículos REALES nuevos en sources/: 4 (desde 2026-07-15).
     Esto excede el umbral de 3 días de CLAUDE.md → **señal de alarma activa**.
  3. Ventanas GDELT: `_gdelt_windows` tenía 50 entradas, pero 13 de ellas
     eran el MISMO trimestre en curso (2026-06-18 → hoy) re-marcado con una
     clave distinta cada día — bug real en `fetch_gdelt_historical()`
     (scripts/fetch_news.py): la ventana final se limita a `end` = ayer,
     que avanza cada día, así que su `window_key` cambia a diario y nunca
     se reconoce como "ya completada". Ventanas trimestrales limpias reales:
     37 (2017-03-30 → 2026-06-17). **Faltan por completo 9 trimestres**:
     2015 Q1–Q4, 2016 Q1–Q4 y 2017 Q1 (2015-01-01 → 2017-03-29) — nunca
     aparecen en `_gdelt_windows`, ni como error reintentable ni como éxito.
     No se pudo determinar la causa raíz exacta desde este entorno (sin
     acceso de red saliente a la API de GDELT para reproducir); posibles
     causas: rate-limit/bloqueo específico para rangos muy antiguos, o un
     límite de ventanas-por-corrida que nunca alcanza esos trimestres
     porque quedan "por delante" de trimestres más recientes en el orden
     de iteración (el bucle siempre arranca desde 2015-01-01, así que en
     teoría debería intentarlos primero — requiere reproducir con logs
     reales de Actions para confirmar).
  4. RSS: IICA y La Prensa son las únicas fuentes activas — sin evidencia
     de que estén caídas (los artículos "1 nuevo" recientes vienen de
     prensa.com vía RSS/DDG, no de GDELT).

  ACCIONES TOMADAS:
  - Corregido el bug de re-marcado diario en scripts/fetch_news.py: ahora
    una ventana solo se agrega a `_gdelt_windows` si es un trimestre
    completo (≥90 días); la ventana final parcial se re-consulta cada día
    sin ensuciar el registro de completadas.
  - Corregido bug en `mark_ingested()` (scripts/ingest.py): iteraba
    `processed.items()` sin filtrar la clave interna `_gdelt_windows`
    (una lista), causando `AttributeError` en cualquier llamada a
    `wiki_agro.py mark-ingested <url>`. Ahora usa `article_entries()`.
  - Corregido `mark_all_ingested()` para usar el mismo orden de prioridad
    por score que `run_prepare()/ingest`, evitando que marque artículos
    distintos a los que Claude Code realmente revisó (ver entrada 00:10).
  - Limpiadas las 13 entradas duplicadas/obsoletas de `_gdelt_windows` en
    sources/processed.json (no se pierde información: los artículos ya
    descargados siguen registrados individualmente por URL y el dedup por
    URL en `_save()` evita duplicados si esas fechas se re-consultan).

  PENDIENTE PARA PRÓXIMA SESIÓN: confirmar con logs reales de GitHub
  Actions por qué los trimestres 2015 Q1–2017 Q1 nunca se completan, y
  por qué no corrió Actions los días 07-16 y 07-17.
