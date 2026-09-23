---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-23T16:30
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
| Pendientes de ingesta (genuinos, verificados) | 14 en `main` (9 en cuanto se mergee el PR #307) | 0 |
| Páginas en wiki/ | 35 (13 topics, 3 entidades, 16 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 79 | 45+ (rango base ya cubierto) |
| Días sin artículos nuevos en sources/ | **17** (último: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última ejecución EXITOSA  : 2026-09-06 (run #103) → 6 artículos nuevos
Ejecuciones fallidas desde: 2026-09-07 → 2026-09-23 (17+ corridas diarias consecutivas,
                             confirmado vía API hasta run #120 de hoy)
Duración de las fallas    : ~4 segundos cada una (vs. ~5-6 min de una corrida normal)
Diagnóstico (confirmado   : `runner_id: 0`, `runner_name: ""`, `created_at` ≈
vía GitHub Actions API)     `completed_at` en TODAS las corridas — el job nunca
                             llega a ejecutar ni un solo step (ni el checkout).
                             Es un `startup_failure` de infraestructura, no un
                             bug de fetch_news.py/fetch_historical.py.
                             `promote_wiki.yml` (workflow separado que promueve
                             wiki/+processed.json de ramas claude/** a main)
                             muestra el MISMO patrón exacto en sus 3 corridas
                             hasta ahora — confirma que es un problema de
                             Actions a nivel de repo/cuenta, no de un workflow
                             puntual. Esto es también la causa de que el
                             trabajo de las rutinas siga acumulándose en
                             ramas/PRs sin llegar a main (ver PR #307).
Causa más probable         : límite de gasto/minutos de GitHub Actions agotado
                             (Settings → Billing), o Actions deshabilitado a
                             nivel de repositorio/cuenta.
Acción pendiente           : usuario debe revisar Settings → Actions / Billing en
                             GitHub — fuera del alcance de esta sesión.
Ver diagnóstico completo   : wiki/log.md, entradas 2026-09-15 08:30 y 2026-09-23
                             (routine — diagnóstico + fix sin ingesta)
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
| 2026-09-23 08:17 | 5 (draft, sin mergear) | 9 (aún no reflejado en main) | Sesión previa del mismo día: PR #307 (rama `claude/modest-galileo-21i61b`), abierto y sin mergear. Ver nota abajo. |
| 2026-09-23 16:30 | 0 (duplicado descartado) | 14 (en main) | Esta sesión detectó que `ingest --limit 5` devolvía el mismo lote ya procesado en el PR #307 y descartó el contenido duplicado para no crear un PR redundante. En su lugar: (1) root-caused y corrigió de nuevo el bug de `mark_all_ingested()` (usaba `find_pending()` alfabético en vez de las URLs reales de `pending_ingest.md`; verificado experimentalmente que solo 1 de 5 URLs coincidía), (2) confirmó vía GitHub Actions API que tanto `wiki_daily.yml` como `promote_wiki.yml` fallan con patrón `startup_failure` (sin runner asignado, ~4s) desde hace 17 días / 3 corridas respectivamente — infraestructura de Actions, no bug de scripts. **Acción pendiente del usuario**: mergear PR #307 y revisar Settings → Actions/Billing. |

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

**Estado a 2026-09-23**: esta señal de alarma sigue ACTIVA y empeorando (17 días sin
artículos nuevos, 17+ ejecuciones de `wiki_daily.yml` fallando consecutivamente, y
ahora también confirmado que `promote_wiki.yml` falla con el mismo patrón). Causa
confirmada vía GitHub Actions API: `startup_failure` — los jobs nunca llegan a
ejecutar ni un paso, probable límite de gasto/minutos de Actions agotado. Requiere
revisión manual del usuario en Settings → Actions/Billing. Ver diagnóstico completo
en wiki/log.md, entrada 2026-09-23 (routine — diagnóstico + fix sin ingesta).
