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
| Artículos reales ingestados (wiki) | 21 | = total sin falsos positivos |
| Falsos positivos acumulados (documentados) | 25 | **0 nuevos** desde el fix de `fetch_ddg_search` (0 nuevos detectados esta sesión) |
| Fuera de cobertura temporal (pre-2015) | 2 | — |
| Pendientes de ingesta (genuinos, verificados) | 9 | 0 |
| Páginas en wiki/ | 41 (14 topics, 3 entidades, 21 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 79 | 45+ (rango base ya cubierto) |
| Días sin artículos nuevos en sources/ | 18 (último: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO (empeoró vs. 09-15: 9 días)** |

---

## Estado del Fetch (GitHub Actions)

```
Última ejecución EXITOSA  : 2026-09-06 (run #103) → 6 artículos nuevos
Ejecuciones fallidas desde: 2026-09-07 → 2026-09-24 (18 corridas diarias consecutivas,
                             runs #104-#121; confirmado vía Actions API)
Duración de las fallas    : ~3-5 segundos cada una (vs. ~5-6 min de una corrida normal)
Estado del workflow       : "active" (NO deshabilitado) — confirmado vía API 2026-09-24
Diagnóstico               : patrón de fallo de arranque del job, consistente en 18
                             ejecuciones consecutivas; no es un bug de
                             fetch_news.py/fetch_historical.py (el job falla antes de
                             llegar a ese paso); logs expiran (404) en todos los casos
                             revisados (2026-09-15 y 2026-09-24)
Causa más probable         : cuota de minutos de GitHub Actions agotada (típico en
                             repos privados en plan gratuito) o bloqueo de facturación
                             a nivel de cuenta — el patrón sistemático e instantáneo
                             descarta un bug de código
Acción pendiente          : usuario debe revisar https://github.com/settings/billing
                             (cuota de minutos de Actions) y Settings → Actions →
                             General del repo abdielg08/wiki_agro
Ver diagnóstico completo  : wiki/log.md, entradas 2026-09-15 08:30 y 2026-09-24
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
| 2026-09-24 | 5 | 9 | Routine automatizada. 0 falsos positivos. Página nueva `topics/cafe_cacao.md`. Diagnóstico reforzado del fetch caído: confirmado vía Actions API que el workflow sigue activo pero acumula 18 corridas fallidas consecutivas (09-07 → 09-24); causa más probable: cuota de minutos de Actions agotada |

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

**Estado a 2026-09-15**: esta señal de alarma está ACTIVA (9 días sin artículos nuevos,
8 ejecuciones de Actions fallando consecutivamente). Ver diagnóstico en wiki/log.md.

**Estado a 2026-09-24**: la señal de alarma sigue ACTIVA y **ha empeorado** (18 días
sin artículos nuevos, 18 ejecuciones de Actions fallando consecutivamente, runs
#104-#121). El workflow está confirmado como `active` vía la API de GitHub Actions,
por lo que se descarta que esté deshabilitado; el patrón de fallo instantáneo (3-5s)
en todas las corridas apunta a cuota de minutos de Actions agotada o bloqueo de
facturación. Requiere intervención del usuario en Settings → Billing / Actions de
GitHub. Ver diagnóstico completo en wiki/log.md, entrada 2026-09-24.
