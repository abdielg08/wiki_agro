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

## 2026-07-07 08:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-07 08:10
ROUTINE — Diagnóstico y limpieza de falsos positivos

**6 pendientes de ingesta revisados — los 6 son falsos positivos, 0 ingestados al wiki:**
  - `sltrib.com` — Timeline Kevin O'Leary data center (Utah, EE.UU.)
  - `sltrib.com` — Box Elder data center opponents (Utah, EE.UU.)
  - `sltrib.com` — Utah Gov. Cox order Great Salt Lake (Utah, EE.UU.)
  - `sltrib.com` — Utah uranium Wasatch Front (Utah, EE.UU.)
  - `nyfb.org` — New York Farm Bureau (Nueva York, EE.UU.)
  - `spa.gov.sa` — 'Reef Saudi' rain-fed agriculture (Arabia Saudita)

  Ninguno menciona a Panamá en título, URL ni texto (verificado). Los 4 artículos de
  Utah y el de Nueva York coinciden por la palabra "MIDA" (Military Institutional
  Development Authority / agricultura genérica), no por Ministerio de Desarrollo
  Agropecuario de Panamá. Se marcaron `ingested: true` en `processed.json` sin crear
  contenido en `wiki/` (siguiendo Regla Crítica #9 — no ingestar falsos positivos).

**Causa raíz identificada y corregida** (`scripts/fetch_news.py`, función
`fetch_ddg_search`): la búsqueda web DDG usa `site:{dominio}` para restringir
resultados (ej. `site:prensa.com`), pero el operador `site:` de DuckDuckGo no se
respeta de forma confiable en el backend de `ddgs` — devuelve resultados de
dominios no relacionados que matchean solo las palabras de la query. A diferencia
de los fetchers de RSS y GDELT, `fetch_ddg_search` no validaba el dominio real de
la URL devuelta ni aplicaba `_is_blocked_domain()`. Fix aplicado: se agregó
verificación de que el dominio de la URL coincida con el `site` solicitado, más
el filtro de dominios bloqueados, igual que en los otros dos fetchers.

Nota: al revisar `processed.json` completo se encontraron 7 falsos positivos
adicionales de sesiones anteriores (2026-05-30 a 2026-06-19), ya documentados en
el audit del 2026-06-22 (ver `wiki/metrics.md`) — tampoco llegaron a `wiki/`.
Total acumulado de falsos positivos detectados: 13. Con el fix de hoy, el gap
que permitía que se colaran (búsqueda DDG) queda cerrado.

**Bug adicional corregido** (`scripts/ingest.py`, función `mark_ingested`):
el comando `mark-ingested <url>` fallaba con `AttributeError` al iterar sobre
`processed.json`, porque la clave especial `_gdelt_windows` (una lista, no un
dict de artículo) no se filtraba antes de llamar `.get()`. Se agregó un
`isinstance(meta, dict)` guard.

**Diagnóstico avanzado — Estado del Fetch (GitHub Actions):**
  - Actions corrió exitosamente los últimos 3 días (07-05, 07-06 — jobs
    "completed"/"success"), pero sin commits nuevos en `sources/` esos días:
    el step de fetch corrió (~6 min) sin producir ningún cambio de estado.
  - Ventanas GDELT completadas: 45 (ver `_gdelt_windows` en `processed.json`).
    Por la regla de diagnóstico de CLAUDE.md (45+ ventanas → rango de fechas
    agotado), esto indica que el backfill histórico GDELT 2015→hoy ya cubrió
    todas las ventanas configuradas y necesita expansión de rango o nuevas
    ventanas trimestrales a medida que avanza el calendario.
  - RSS activos: IICA y La Prensa (LaPrensaGeneral) siguen devolviendo entradas
    ocasionalmente (1-3 artículos/semana).

**Resultado de la sesión**: 0 artículos nuevos añadidos al wiki (todos los
pendientes eran falsos positivos). Pendientes de ingesta: 0.
