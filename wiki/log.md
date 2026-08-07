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

## 2026-08-07 08:05
ROUTINE: 5 artículos revisados de la cola de ingesta — los 5 son FALSOS POSITIVOS (0 ingestados)
  Ninguno menciona "Panama"/"Panamá" ni tema agropecuario panameño. Todos entraron por
  colisión del acrónimo "MIDA" con organizaciones homónimas fuera de Panamá:
    - "MITI working on simplified NCM..." (paultan.org) → MIDA = Malaysian Investment
      Development Authority (agencia de inversión de Malasia)
    - "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com) →
      MIDA = Military Installation Development Authority (Utah, EE.UU.)
    - "Box Elder data center opponents hope for a vote..." (sltrib.com) → mismo MIDA de Utah
    - "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com) → mismo MIDA de Utah
    - "Cultural Rules For Staying With Locals Abroad" (msn.com) → mismo MIDA de Utah,
      mención tangencial en un artículo sin relación con Panamá
  No se creó ningún summary ni se tocó wiki/topics/ o wiki/entities/ para estos 5.
  Marcados como procesados vía `mark-all-ingested --limit 5` para vaciar la cola
  (quedan excluidos de futuras ejecuciones de `ingest`, pero no cuentan como artículos reales).

  CAUSA RAÍZ IDENTIFICADA Y CORREGIDA: scripts/fetch_news.py::fetch_ddg_search() era el
  único fetcher (de RSS/GDELT/DDG) que NO aplicaba el filtro `_is_panama_related()` ni
  `_is_blocked_domain()` antes de aceptar un resultado — solo comprobaba `is_agro_relevant()`,
  que matchea por keywords sueltas como "MIDA" sin exigir contexto panameño. Además
  etiquetaba `source` con el sitio configurado (p.ej. "prensa.com") en vez del dominio real
  de la URL devuelta por DDGS, ocultando que los resultados venían de dominios no panameños.
  Fix aplicado: se agregaron ambos filtros y se corrigió `source` para usar `_url_domain(url)`.
  Ver commit de esta sesión para el diff.

## 2026-08-07 08:05
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-07 08:07
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-07 08:07
INGEST: 6 artículos marcados como ingestados por sesión Claude Code

## 2026-08-07 08:15
ROUTINE (continuación): revisados los 11 artículos restantes de la cola — TODOS falsos
positivos (0 ingestados). Cola de pendientes ahora en 0.
  Lote 2 (5 artículos, mismos 4 del lote 1 + 1 nuevo):
    - paultan.org MITI/MIDA Malasia, sltrib.com ×3 MIDA Utah (ya documentados arriba)
    - "New York Farm Bureau" (nyfb.org) → home institucional de un farm bureau de
      EE.UU., sin mención de Panamá; matcheó por keywords genéricos de agricultura.
  Lote 3 (6 artículos, todos de heraldo.es/spa.gov.sa/agenciabrasil.ebc.com.br/unesco.org):
    - "Arvensis Agro amplía sus instalaciones..." (heraldo.es) → agroindustria de Aragón, España
    - "'Reef Saudi', a Successful Program..." (spa.gov.sa) → agricultura de secano, Arabia Saudita
    - "Finep vai pagar R$ 220 milhões..." (agenciabrasil.ebc.com.br) → fondo de innovación agrícola, Brasil
    - "The Persian Qanat" (whc.unesco.org) → sitio Patrimonio Mundial UNESCO, Irán
    - "AEGA pide elecciones al campo en Aragón..." (heraldo.es) → gremio agrario de Aragón, España
    - "Luis Biendicho asume la consejería de Medio Ambiente..." (heraldo.es) → gobierno regional
      de Aragón, España
  Los 11 se verificaron programáticamente (0 menciones de "panama"/"panamá" en el JSON
  completo de cada uno). Todos venían etiquetados `"source": "prensa.com"` pese a no ser
  de ese dominio — síntoma del mismo bug de `fetch_ddg_search()` corregido en esta sesión
  (ver entrada anterior): el buscador DDG con `site:prensa.com` no restringía realmente el
  dominio, y sin el filtro `_is_panama_related()` cualquier resultado que matcheara
  keywords agro genéricos ("agricultura", "agro", "cosecha", etc.) se aceptaba sin
  importar el país. No se creó ningún summary ni se tocaron topics/entities para estos 11.
  Todos marcados como procesados (`ingested: true`) para vaciar la cola — no cuentan
  como artículos reales ingestados (0 de 16 revisados esta sesión eran sobre agro de Panamá).

  BUG ADICIONAL ENCONTRADO Y CORREGIDO: `mark_all_ingested(limit=N)` en scripts/ingest.py
  seleccionaba los primeros N artículos de `find_pending()` (orden alfabético por nombre
  de archivo), mientras que `ingest --limit N` selecciona por `prioritize()` (score de
  relevancia, orden por defecto). Ambos órdenes casi nunca coinciden, así que
  `mark-all-ingested --limit 5` marcaba como ingestados artículos DISTINTOS a los que
  Claude acababa de revisar — en la práctica, del primer lote de 5 revisados en esta
  sesión, solo 1 quedó marcado correctamente y los otros 4 siguieron apareciendo como
  pendientes en la siguiente corrida. Fix: `mark_all_ingested()` ahora usa `prioritize()`
  con la misma estrategia por defecto ("score") que `run_prepare()`, así que marca
  exactamente el mismo conjunto que `ingest` mostró. Verificado: tras el fix, los 5
  artículos del lote 2 quedaron con `ingested: true` en `sources/processed.json`.

## 2026-08-07 08:30
DIAGNÓSTICO AVANZADO (Pendientes=0 tras esta sesión): 3 hallazgos sobre el fetch.

1. **GitHub Actions SÍ está corriendo** (verificado vía API de GitHub, no solo git log):
   corridas diarias del 2026-07-23 al 2026-08-06, todas `completed`/`success`. Pero
   `git log -- sources/` muestra el último commit el 2026-08-04 — las corridas de
   2026-08-05 y 2026-08-06 no generaron ningún commit porque `git diff --staged` quedó
   vacío: 0 artículos nuevos de RSS (IICA/La Prensa) y 0 cambios de estado en GDELT.
   2 días consecutivos sin novedades (08-05, 08-06); la corrida de hoy (08-07, cron
   11:00 UTC) aún no se ejecuta al momento de este diagnóstico (08:30 UTC).

2. **BUG DE FONDO encontrado y corregido — ventana GDELT final duplicada cada día**
   (`scripts/fetch_news.py::fetch_gdelt_historical()`): la última ventana trimestral
   del backfill queda acotada por `end = ayer` en vez de por `current + 90 días`. El
   código anterior marcaba esa ventana parcial como "completa" con una clave que incluye
   la fecha de corte (`"20260618_20260803"`, etc.), así que cada corrida diaria generaba
   una clave NUEVA para prácticamente el mismo rango de ~6 semanas en vez de avanzar al
   siguiente trimestre real. Resultado en `processed.json`: 62 "ventanas completadas"
   reportadas, pero solo 37 eran trimestres reales de 90 días (2017-03-30 → 2026-06-17);
   las otras 25 eran variantes diarias de la misma ventana de cola (2026-06-18 → hoy).
   Esto inflaba el contador de progreso del backfill sin aportar cobertura nueva.
   Fix aplicado: una ventana solo se marca completa y hace avanzar el cursor si alcanzó
   un trimestre completo (90 días) o el `end` configurado; la ventana de cola parcial ya
   no se persiste — se reconsulta (creciendo) cada día hasta cerrarse como trimestre real.
   Se limpiaron las 25 entradas basura de `sources/processed.json._gdelt_windows`
   (quedan 37, las reales).

3. **GAP DE COBERTURA REAL en el backfill histórico**: la ventana completada más antigua
   es `20170330_20170628`. El objetivo de CLAUDE.md es cobertura desde 2015-02-19, y
   `config/sources.yaml` sí configura `gdelt.date_range.start: 2015-01-01`, pero NINGUNA
   ventana entre 2015-01-01 y 2017-03-29 (~9 trimestres) aparece completada — probablemente
   porque `fetch_gdelt_batch()`/`_get()` devuelve error (no `None` "reintentar", sino algo
   que tampoco se marca "completo") para ese rango, posiblemente por cobertura limitada de
   GDELT en español para fechas anteriores a ~2017. No se investigó más a fondo esta
   sesión — queda pendiente confirmar la causa exacta (correr
   `python scripts/fetch_historical.py --years 2015-2017 --mode gdelt` manualmente y
   revisar el error) y decidir una fuente alterna para ese tramo (p. ej. Wayback CDX o
   sitemaps de La Prensa/TVN para 2015-2017) si GDELT no tiene cobertura ahí.

  Ver `wiki/metrics.md` para las cifras actualizadas de esta sesión.
