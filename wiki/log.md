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

## 2026-08-14 09:11
ROUTINE: 16 artículos pendientes revisados — 16/16 falsos positivos (0 ingestados al wiki)
  Todos provenían de la fuente "prensa_agro" (búsqueda DDG con site:prensa.com).
  Ninguno era sobre agro panameño; ninguno pertenecía siquiera al dominio prensa.com:
    - MITI/MIDA (Malasia) — incentivos industriales             → paultan.org
    - Kevin O'Leary data center + "MIDA" (Utah)                 → sltrib.com ×3
    - Cultural rules for staying with locals abroad              → msn.com
    - Catalogue of Diptera (entomología, no agro)                → archive.org
    - Ambient IoT precision agriculture (paper académico, no PA) → ieeexplore.ieee.org
    - Aragón, España — bienestar porcino / política agraria      → heraldo.es ×3
    - Utah — uranio para energía nuclear                         → sltrib.com
    - New York Farm Bureau (EE.UU.)                              → nyfb.org
    - "Reef Saudi" — agricultura de secano (Arabia Saudita)      → spa.gov.sa
    - Finep — agricultura familiar (Brasil)                      → agenciabrasil.ebc.com.br
    - Persian Qanat (patrimonio UNESCO, Irán)                    → whc.unesco.org
  Documentado como falso positivo por regla 9 de CLAUDE.md. Los 16 se marcaron
  `ingested: true` en sources/processed.json (vía mark-ingested) para sacarlos
  de la cola pendiente sin incorporarlos al wiki.

  DIAGNÓSTICO DE CAUSA RAÍZ (encontrado y corregido en esta sesión):
  1. `scripts/fetch_news.py::fetch_ddg_search()` arma la query como
     "site:prensa.com {query}" pero nunca valida que la URL devuelta por
     DDGS().news() pertenezca realmente a ese dominio — el operador site:
     no es respetado de forma confiable por el backend de búsqueda de
     noticias de DDG. Resultado: 0 de 23 artículos históricos de la fuente
     "prensa.com" pertenecen realmente a prensa.com.
     FIX: se agregó verificación de dominio (urlparse + comparación de
     netloc contra `site`) en fetch_ddg_search — descarta cualquier
     resultado cuyo dominio no coincida con el `site` configurado.
  2. `scripts/fetch_news.py::is_agro_relevant()` acepta un artículo si
     CUALQUIER término de `search_terms.primary/secondary` aparece en el
     título/cuerpo — sin exigir mención de Panamá. Términos genéricos como
     "agricultura", "cultivo", "cosecha" y sobre todo la sigla "MIDA"
     (que también nombra al Malaysian Investment Development Authority y
     a la Utah Military Installation Development Authority) generan
     colisiones sistemáticas con contenido no panameño. No se modificó en
     esta sesión — el fix de dominio (punto 1) ya elimina el 100% de los
     falsos positivos observados en esta fuente; si reaparecen falsos
     positivos DENTRO del dominio prensa.com, revisar is_agro_relevant()
     para exigir contexto Panamá explícito.

  BUG SECUNDARIO encontrado y corregido: `scripts/ingest.py::mark_ingested()`
  fallaba con AttributeError al iterar `processed.items()` porque la clave
  interna `_gdelt_windows` tiene valor tipo list, no dict. Se agregó
  `isinstance(meta, dict)` antes de acceder a `meta.get(...)`. Este bug
  bloqueaba por completo el flujo documentado en CLAUDE.md
  (`mark-ingested <url>` por artículo).

  DIAGNÓSTICO AVANZADO (Paso 4, pendientes=0 tras esta limpieza):
  - GitHub Actions SÍ corre a diario (commits en sources/processed.json:
    2026-08-13, 08-12, 08-10, 08-07, 08-04, 08-02, 07-31...).
  - Pero no llegan artículos NUEVOS reales desde 2026-07-30 (15 días).
    Esto excede el umbral de 3 días del CLAUDE.md — falla activa.
  - Ventanas GDELT completadas: 66 (superior al ~45 estimado en
    metrics.md). Análisis detallado: solo 47 ventanas trimestrales
    "limpias" son necesarias para cubrir 2015-01-01 → hoy; de esas, 10
    ventanas de 2015-2017 SIGUEN sin completar pese a meses de corridas
    diarias en modo "all". Las 29 ventanas "extra" son todas variantes
    de una sola ventana abierta que empieza en 2026-06-18, con fecha de
    cierre distinta cada día (20260618_20260623, _20260624, _20260626...
    hasta _20260724) — indica que `fetch_gdelt_historical()` recalcula
    el cierre dinámico ("ayer") cada corrida y genera una window_key
    nueva en vez de extender/cerrar la ventana trimestral real. Esto
    hace que el backfill quede atascado re-consultando casi el mismo
    rango de fechas recientes cada día en lugar de avanzar sobre 2015-
    2017, y explica en parte por qué la mayoría de las corridas recientes
    reportan "0 artículos nuevos". NO se modificó fetch_gdelt_historical()
    en esta sesión (requiere pruebas contra la API real de GDELT, fuera
    de alcance de una rutina) — se documenta como TODO para una sesión de
    ingeniería dedicada.
  - Fuentes RSS (IICA, La Prensa): no verificadas en vivo esta sesión
    (sin llamadas de red adicionales); revisar en próxima corrida de
    Actions si el problema persiste tras el fix del punto 1.

  Commit de esta sesión incluye: fix de dominio en fetch_ddg_search,
  fix de mark_ingested, y actualización de wiki/metrics.md.
