---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2026-08-10
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

## 2026-08-10 00:00
ROUTINE: Sesión de mantenimiento — 0 artículos reales ingestados, 16 falsos positivos rechazados

**Diagnóstico**: `stats` mostraba 16 pendientes de ingesta. Se revisó cada uno
en `pending_ingest.md`/`queue` — **los 16 son falsos positivos**, ninguno
trata de agro panameño:

  - `archive.org/details/Cataloguedipter2SaoP` — catálogo entomológico histórico, sin relación
  - `ieeexplore.ieee.org/document/10945742` — paper IEEE sobre IoT genérico, no específico de Panamá
  - `sltrib.com .../utah-nuclear-energy-state/` — energía nuclear en Utah, EE.UU.
  - `heraldo.es .../aragon-celebra-sentencia...` — granjas porcinas en Aragón, España
  - `msn.com .../cultural-rules-for-staying-with-locals-abroad` — artículo de viajes, menciona MIDA (Utah) de pasada
  - `heraldo.es .../luis-biendicho-vox-asume-consejeria...` — política ambiental de Aragón, España
  - `sltrib.com .../kevin-oleary-data-center-timeline/` — MIDA = Military Installation Development Authority (Utah)
  - `sltrib.com .../box-elder-data-center-opponents/` — ídem, MIDA de Utah
  - `sltrib.com .../utah-governor-issues-order-protect/` — ídem, MIDA de Utah
  - `heraldo.es .../aega-pide-elecciones-campo-aragon...` — gremio agrícola de Aragón, España
  - `nyfb.org` — New York Farm Bureau, EE.UU.
  - `heraldo.es .../arvensis-agro-amplia-sus-instalaciones...` — empresa agro de Aragón, España
  - `spa.gov.sa/en/N2096157` — programa de agricultura de secano en Arabia Saudita
  - `agenciabrasil.ebc.com.br .../finep-vai-pagar...` — financiamiento agrícola en Brasil
  - `whc.unesco.org/en/list/1506` — patrimonio UNESCO (qanats persas, Irán)
  - `paultan.org .../miti-working-on-simplified-ncm...` — MIDA = Malaysian Investment Development Authority

  Ninguno fue ingestado al wiki. No se crearon ni modificaron páginas de
  `topics/` ni `entities/` a partir de estos artículos.

**Causa raíz identificada**: la fuente `prensa_agro` (búsqueda DDG con
`site:prensa.com`, ver `config/sources.yaml`) es la responsable de los 23
falsos positivos acumulados en `sources/` bajo `source: "prensa.com"`
(7 detectados en la auditoría previa del 2026-06-22 + 16 de hoy — es decir,
**el 100% de lo que esa fuente ha aportado desde el inicio del proyecto son
falsos positivos**; cero artículos reales de Panamá). Dos problemas
combinados:
  1. El operador `site:` de DDG no restringe realmente el dominio — los
     resultados vienen de sltrib.com, heraldo.es, paultan.org, etc., no de
     prensa.com.
  2. `fetch_ddg_search()` en `scripts/fetch_news.py` nunca aplicaba los
     filtros `_is_panama_related()` / `_is_blocked_domain()` que sí usan
     los fetchers de RSS y GDELT — solo verificaba `is_agro_relevant()`
     (términos genéricos de agro), así que "MIDA" (que colisiona con la
     Malaysian Investment Development Authority y la Utah Military
     Installation Development Authority) pasaba el filtro sin más.

**Fix aplicado**: se agregó `_is_blocked_domain()` y `_is_panama_related()`
a `fetch_ddg_search()` en `scripts/fetch_news.py`, igualando su
comportamiento al de `fetch_rss()`. Esto debería frenar la reaparición de
este tipo de falso positivo en corridas futuras del fetch diario.

**Resolución de la cola**: los 16 artículos se marcaron `ingested: true` +
`false_positive: true` + `false_positive_reason` en `sources/processed.json`
(sin crear contenido de wiki) para sacarlos de la cola de pendientes —
mismo patrón usado en la auditoría del 2026-06-22 para los 7 falsos
positivos previos.

**Diagnóstico avanzado del fetch** (vía logs de GitHub Actions, corrida del
2026-08-09, run 31310552769):
  - GitHub Actions SÍ está corriendo diariamente sin fallar (verificado con
    la API de Actions — 08-08 y 08-09 corrieron OK, ambas con "0 artículos
    nuevos" antes del fix de hoy).
  - RSS IICA → 0 entradas. RSS LaPrensaGeneral (prensa.com/feed/) → 0
    entradas. Ambos feeds llevan tiempo sin devolver nada.
  - Búsquedas DDG a sitios oficiales (oirsa.org, mida.gob.pa, idiap.gob.pa,
    bda.gob.pa, fao.org, bancomundial.org, iica.int) → "No results found"
    en las 7. Ninguna está aportando artículos actualmente.
  - GDELT: ventanas 2015-01-01 → 2017-03-29 (7 ventanas) siguen fallando
    con `403/429` en cada corrida y nunca llegan a completarse. Ventanas
    2017-03-30 → 2026-06-17 (33 ventanas) ya descargadas y se saltan
    correctamente. La ventana más reciente (2026-06-18 → hoy) también
    recibe 403 en cada intento.
  - **Ventanas GDELT completadas: 63** (33 confirmadas + 30 heredadas de
    corridas previas) — supera el umbral de ~45 estimado en `CLAUDE.md`
    para "rango de fechas agotado". El backfill vía GDELT está
    esencialmente completo para el rango que la API permite acceder sin
    bloqueo; lo que falta (2015-2017 y la ventana actual) está bloqueado
    por rate-limiting, no por falta de rango.

**Conclusión**: desde la semilla inicial (2026-05-24), el pipeline
automático no ha aportado **ningún** artículo real de Panamá — solo
falsos positivos vía DDG. Las fuentes con más probabilidad de producir
contenido real (RSS IICA/La Prensa, GDELT reciente) están actualmente
sin resultados o bloqueadas. Esto no es una falla de "Actions no corrió"
sino de "las fuentes activas no están devolviendo contenido de Panamá".
Se notifica al usuario — puede requerir revisar por qué los feeds RSS
están vacíos (¿URLs cambiaron?) y si el rate-limit de GDELT necesita
backoff más largo o una IP/hora distinta.
