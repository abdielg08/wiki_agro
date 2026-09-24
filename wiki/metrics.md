---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ (descargados) | 57 | ↑ continuo |
| Artículos reales ingestados (wiki) | 16 | = total sin falsos positivos |
| Falsos positivos acumulados (documentados) | 25 | **0 nuevos** desde el fix de `fetch_ddg_search` |
| Fuera de cobertura temporal (pre-2015) | 2 | — |
| Pendientes de ingesta (genuinos, verificados) | 14 | 0 |
| Páginas en wiki/ | 35 (13 topics, 3 entidades, 16 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 79 | 45+ (rango base ya cubierto) |
| Días sin artículos nuevos en sources/ | 18 (último: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última ejecución EXITOSA  : 2026-09-06 (run #103) → 6 artículos nuevos
Ejecuciones fallidas desde: 2026-09-07 → 2026-09-23 (17 corridas diarias consecutivas,
                             hasta run #120 — confirmado vía GitHub Actions API el
                             2026-09-24, el problema NO se ha resuelto)
Duración de las fallas    : ~3-5 segundos cada una (vs. ~5-6 min de una corrida normal)
Diagnóstico               : patrón de fallo de arranque del job (no es un bug de
                             fetch_news.py/fetch_historical.py); logs ya expirados
                             (404) para todas las corridas revisadas
Causas probables          : cuota de minutos de Actions agotada, cambio de permisos
                             de GITHUB_TOKEN/protección de rama, o workflow pausado
                             a nivel de repositorio — requiere revisión manual del
                             usuario (fuera del alcance de esta sesión)
Nuevo dato (2026-09-24)   : promote_wiki.yml (el workflow que promueve wiki/ +
                             processed.json de ramas claude/** a main) también falla
                             con el mismo patrón en sus 4 corridas — el mismo problema
                             de infraestructura bloquea tanto el fetch diario como la
                             promoción automática del trabajo de las routines
Acción pendiente          : usuario debe revisar Settings → Actions / Billing en GitHub
Ver diagnóstico completo  : wiki/log.md, entradas 2026-09-15 08:30 y 2026-09-24
```

```
BACKLOG DUPLICADO (2026-09-24): esta sesión de routine encontró 14 pendientes en main
y, al pedir el siguiente lote de 5, recibió el mismo lote que YA había sido procesado
por dos sesiones anteriores el 2026-09-23, ambas sin mergear:
  - PR #307 (rama claude/modest-galileo-21i61b): contenido real de ingesta (5 resúmenes
    + topics/entities actualizados)
  - PR #308 (rama claude/modest-galileo-qsbryn): fix de la regresión en
    mark_all_ingested() (ver wiki/log.md 2026-09-24)
Recomendación: mergear #307 y #308 para que "Pendientes" baje de 14 a 9 en main. Hasta
entonces, cada nueva sesión de routine seguirá recibiendo el mismo lote de 5 artículos.
```

```
Fix aplicado esta sesión  : fetch_ddg_search() en scripts/fetch_news.py no aplicaba
                             el filtro _is_panama_related()/_is_blocked_domain() que sí
                             usan fetch_rss() y fetch_gdelt_batch(). Esto permitía que
                             resultados de DuckDuckGo de dominios no panameños (ej.
                             "MIDA" de Malasia o de Utah) se guardaran como artículos
                             pendientes. Corregido — ver wiki/log.md 2026-09-15 08:25.
Bug adicional corregido   : mark_all_ingested() marcaba un conjunto de artículos
                             distinto al que ingest realmente mostraba a Claude (los
                             dos usaban órdenes de prioridad distintos). Corregido para
                             leer las URLs directamente de pending_ingest.md — ver
                             wiki/log.md 2026-09-15 08:20 y scripts/ingest.py.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> 79 ventanas GDELT completadas según `sources/processed.json` (`_gdelt_windows`), por
> encima del umbral de 45 que CLAUDE.md usa como señal de "rango base agotado". La
> cobertura real de artículos, sin embargo, sigue concentrada en 2019-2026; años
> 2015-2018 tienen cobertura escasa (solo los artículos semilla). Pendiente de una
> auditoría detallada de qué ventanas específicas (por trimestre) ya se cubrieron vs.
> cuáles devolvieron 0 resultados por falta de cobertura mediática de esa época.

| Período | Estado |
|---------|--------|
| 2015-2018 | Cobertura escasa — solo artículos semilla (1 por año aprox.) |
| 2019-2026 | Cobertura activa — mayoría de artículos ingestados y pendientes |

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-15 | 10 (2 lotes de 5) | 14 | Routine automatizada. Además: fix de bug crítico en `mark_all_ingested` (marcaba artículos equivocados), 17 falsos positivos nuevos detectados y documentados, 7 falsos positivos antiguos re-etiquetados, fix de raíz en `fetch_ddg_search` (faltaba filtro Panamá), y diagnóstico de 8 fallos consecutivos de GitHub Actions |
| 2026-09-24 | 0 (duplicado, ver nota) | 14 (sin cambio en main) | Routine detectó que el lote pendiente ya había sido procesado por dos sesiones del 2026-09-23 (PRs #307 y #308, sin mergear). No se duplicó el trabajo; se documentó el hallazgo y se recomendó mergear ambos PRs. Confirmado: 17 fallos consecutivos de `wiki_daily.yml` (hasta run #120) y 4 fallos de `promote_wiki.yml` |

---

## Instrucciones para la Routine

Al ejecutar, la routine DEBE:

1. Correr `python wiki_agro.py stats` y copiar los números aquí
2. Si ingestó artículos: actualizar la tabla "Historial de Sesiones"
3. Si pendientes = 0: actualizar "Estado del Fetch" con diagnóstico
4. Actualizar "last_updated" en el frontmatter
5. Si `Ventanas GDELT completadas` subió: actualizar tabla de Backfill

**Señal de alarma**: si "Días sin artículos nuevos" llega a 3, la routine debe:
- Revisar el último log de GitHub Actions (ver wiki/log.md para contexto)
- Identificar si el problema es GDELT rate-limit, RSS caído, o config
- Documentar el diagnóstico en wiki/log.md con pasos para resolverlo

**Estado a 2026-09-24**: esta señal de alarma sigue ACTIVA y ha empeorado (18 días sin
artículos nuevos, 17 ejecuciones de `wiki_daily.yml` fallando consecutivamente, y ahora
también `promote_wiki.yml` fallando en sus 4 corridas). Ver diagnóstico en wiki/log.md.
