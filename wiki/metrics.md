---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-25
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
| Páginas en wiki/ | 43 (15 topics, 4 entidades, 21 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 79 (sin cambio desde 2026-09-15) | 45+ (rango base ya cubierto) |
| Días sin artículos nuevos en sources/ | 19 (último: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO, empeorando** |

---

## Estado del Fetch (GitHub Actions)

```
Última ejecución EXITOSA  : 2026-09-06 (run #103, id 34037328987) → 6 artículos nuevos
Ejecuciones fallidas desde: 2026-09-07 → 2026-09-24 (18 corridas diarias consecutivas,
                             runs #104-#121; el problema NO se resolvió tras el
                             diagnóstico de 2026-09-15 — empeoró de 8 a 18 fallos)
Duración de las fallas    : 3-4 segundos cada una (vs. ~6-8 min de una corrida normal
                             exitosa) — confirmado vía GitHub Actions API (mcp__github)
Diagnóstico (2026-09-25)  : patrón de fallo de arranque del job confirmado nuevamente
                             vía API (list_workflow_runs + list_workflow_jobs): el job
                             único "Fetch artículos → Commit a sources/" completa en
                             3-4s con conclusion=failure en TODAS las corridas desde
                             el 2026-09-07. Los logs del job ya expiraron (HTTP 404 al
                             intentar descargarlos vía get_job_logs), por lo que no se
                             puede leer el mensaje de error exacto desde esta sesión.
Causas probables          : cuota de minutos de Actions agotada, cambio de permisos
                             de GITHUB_TOKEN/protección de rama, secreto faltante, o
                             workflow pausado a nivel de repositorio — requiere
                             revisión manual del usuario en GitHub (fuera del alcance
                             de esta sesión; no hay acceso a Settings/Billing vía API)
Acción pendiente          : usuario debe revisar Settings → Actions / Billing en GitHub
                             y abrir el run más reciente (run #121,
                             https://github.com/abdielg08/wiki_agro/actions/runs/36021398821)
                             mientras los logs sigan disponibles en la UI de GitHub
Ver diagnóstico completo  : wiki/log.md, entradas 2026-09-15 08:30 y 2026-09-25
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
Re-fix (2026-09-25)       : el fix del 2026-09-15 arriba descrito NO estaba presente
                             en scripts/ingest.py de main (se perdió en el problema de
                             ramas huérfanas resuelto el 2026-09-23) — el bug había
                             vuelto a ocurrir: 4 de 5 artículos marcados por esta misma
                             sesión de routine eran incorrectos. Re-aplicado el fix
                             (urls_from_pending_ingest() en scripts/ingest.py) y
                             corregido sources/processed.json manualmente. Ver
                             wiki/log.md 2026-09-25, entrada "FIX BUG mark_all_ingested".
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
| 2026-09-25 | 5 | 9 | Routine automatizada. 0 falsos positivos (los 5 artículos eran genuinamente sobre agro panameño, aunque con `full_text` truncado en la fuente). Páginas nuevas: topics/darien_comarca.md, topics/cafe_cacao.md, entities/ima.md (resuelven broken links preexistentes). Diagnóstico confirmado vía GitHub Actions API: 18 fallos consecutivos del fetch diario desde 2026-09-07 (empeoró de 8 a 18 desde el diagnóstico anterior) |

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

**Estado a 2026-09-25**: esta señal de alarma sigue ACTIVA y ha empeorado (19 días sin
artículos nuevos, 18 ejecuciones de Actions fallando consecutivamente desde 2026-09-07,
frente a 9 días / 8 fallos reportados el 2026-09-15). El backlog de 9 artículos
pendientes genuinos alcanza para ~2 sesiones más de routine antes de agotarse. Se
requiere intervención manual del usuario en GitHub Settings → Actions/Billing — no
resoluble desde una sesión de Claude Code. Ver diagnóstico en wiki/log.md, entrada
2026-09-25.
