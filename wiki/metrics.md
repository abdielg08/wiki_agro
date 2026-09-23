---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-23 (08:13 UTC)
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ (descargados) | 57 | ↑ continuo |
| Artículos reales ingestados (wiki) | 21 | = total sin falsos positivos |
| Falsos positivos acumulados (documentados) | 25 | **0 nuevos** desde el fix de `fetch_ddg_search` |
| Fuera de cobertura temporal (pre-2015) | 2 | — |
| Pendientes de ingesta (genuinos, verificados) | 9 | 0 |
| Páginas en wiki/ | 42 (15 topics, 3 entidades, 21 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 79 | 45+ (rango base ya cubierto) |
| Días sin artículos nuevos en sources/ | 17 (último: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última ejecución EXITOSA  : 2026-09-06 (run #103, commit 24cfc3c) → 6 artículos nuevos
Ejecuciones fallidas desde: 2026-09-07 → 2026-09-22 (confirmado vía API: runs #110-#119,
                             10 corridas diarias consecutivas con conclusion=failure,
                             sin contar posibles corridas anteriores ya rotadas del historial)
Duración de las fallas    : 3-4 segundos cada una (vs. ~5-6 min de una corrida normal);
                             runner_id=0, runner_name="" en cada job — el job NUNCA
                             llega a asignarse un runner, no es un fallo del script Python
Diagnóstico (confirmado esta sesión vía GitHub Actions API, run #119 = 35746215613,
job 106808407217): logs ya expirados (HTTP 404) para descarga completa, pero los
metadatos del job confirman el mismo patrón de fallo de arranque reportado el
2026-09-15 — persiste sin cambios 17 días después.
Dato adicional            : wiki_historical.yml (crawl histórico 15 años) registra
                             **0 ejecuciones totales** — nunca ha corrido ni una vez
                             desde que se creó (2026-05-26); no es solo un fallo del
                             fetch diario, sino de los workflows programados en general.
Causas probables          : cuota de minutos de Actions agotada, cambio de permisos
                             de GITHUB_TOKEN/protección de rama, o Actions deshabilitado/
                             pausado a nivel de repositorio u organización — requiere
                             revisión manual del usuario (fuera del alcance de esta sesión;
                             no hay acceso de administración de Settings/Billing vía API)
Acción pendiente          : usuario debe revisar Settings → Actions → General (¿workflows
                             habilitados?) y Settings → Billing → Actions minutes en GitHub
Ver diagnóstico completo  : wiki/log.md, entradas 2026-09-15 08:30 y 2026-09-23 08:13
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
REGRESIÓN 2026-09-23      : el fix anterior de mark_all_ingested() no estaba en el
                             código de main (se perdió en la recuperación de rama
                             de esta sesión) — el bug volvió a marcar 4 artículos
                             equivocados. Corregido de nuevo, con docstring
                             explícito para evitar que se repita — ver
                             wiki/log.md 2026-09-23 08:35 y scripts/ingest.py.
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
| 2026-09-23 | 5 | 9 | Routine automatizada. Artículos con `summary_raw` truncado (0 falsos positivos); páginas nuevas: `topics/cafe_cacao.md`, `topics/agroturismo.md`. Diagnóstico avanzado confirmado vía GitHub Actions API: `wiki_daily.yml` lleva 10 corridas diarias consecutivas fallidas (09-13 a 09-22, runner nunca asignado) y `wiki_historical.yml` nunca ha corrido — requiere revisión manual de Settings/Billing por el usuario |

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

**Estado a 2026-09-23**: la señal de alarma sigue ACTIVA y se agravó (17 días sin
artículos nuevos en sources/, 10 corridas diarias consecutivas de `wiki_daily.yml`
fallando con conclusion=failure según la API de GitHub Actions, y `wiki_historical.yml`
sin ninguna ejecución registrada desde su creación). El backlog de 9 pendientes
genuinos alcanza para ~2 sesiones de routine más antes de agotarse; si el fetch no
se restablece, el backfill histórico 2015→hoy quedará detenido por completo. Acción
requerida del usuario: revisar Settings → Actions → General y Settings → Billing →
Actions en GitHub (fuera del alcance de esta sesión).
