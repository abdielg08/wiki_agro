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
| Artículos reales ingestados (wiki, esta rama local) | 53 | = total sin falsos positivos |
| Falsos positivos acumulados (documentados) | 25 | **0 nuevos** desde el fix de `fetch_ddg_search` (0 nuevos esta sesión, 2 lotes) |
| Fuera de cobertura temporal (pre-2015) | 2 | — |
| Pendientes de ingesta (genuinos, verificados) | 4 | 0 |
| Páginas en wiki/ | 48 (15 topics, 4 entidades, 26 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial, concentrada en 2019-2026) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 79 | 45+ (rango base ya cubierto) |
| Días sin artículos nuevos en sources/ | 19 (último: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL AMPLIAMENTE SUPERADO** |

> ⚠️ **Estas cifras reflejan el estado de la rama de esta sesión, no necesariamente `main`.**
> Hay ~30 PRs abiertos con ingestas de sesiones previas que nunca se mergearon (ver
> "Sísifo reincidente" abajo); `main` puede mostrar cifras menores hasta que se
> resuelva ese backlog. Ver `wiki/log.md`, entrada 2026-09-25, para el detalle completo.

---

## Estado del Fetch (GitHub Actions)

```
Última ejecución EXITOSA  : 2026-09-06 (run #103) → 6 artículos nuevos
Ejecuciones fallidas desde: 2026-09-07 → 2026-09-25 (19 corridas diarias consecutivas,
                             runs #104-#121+; confirmado vía Actions API)
Duración de las fallas    : ~3-5 segundos cada una (vs. ~5-6 min de una corrida normal)
Estado del workflow       : "active" (NO deshabilitado) — confirmado vía API
Diagnóstico               : patrón de fallo de arranque del job, consistente en 19
                             ejecuciones consecutivas; no es un bug de
                             fetch_news.py/fetch_historical.py
Causa confirmada          : CUOTA DE MINUTOS DE GITHUB ACTIONS AGOTADA (o bloqueo de
                             facturación de cuenta) — confirmado vía
                             get_workflow_run_usage (0 ms facturables pese a runs de
                             ~4s) por una sesión el 2026-09-24. Esto también bloquea
                             promote_wiki.yml (ver sección "Sísifo reincidente" abajo).
Acción pendiente          : usuario debe revisar https://github.com/settings/billing
                             y Settings → Actions → General del repo
Ver diagnóstico completo  : wiki/log.md, entradas 2026-09-15, 2026-09-24 y 2026-09-25
```

```
Fix aplicado 2026-09-15   : fetch_ddg_search() en scripts/fetch_news.py no aplicaba
                             el filtro _is_panama_related()/_is_blocked_domain() que sí
                             usan fetch_rss() y fetch_gdelt_batch(). Esto permitía que
                             resultados de DuckDuckGo de dominios no panameños (ej.
                             "MIDA" de Malasia o de Utah) se guardaran como artículos
                             pendientes. Corregido — ver wiki/log.md 2026-09-15 08:25.
Bug REINCIDENTE corregido : mark_all_ingested() volvió a marcar un conjunto de
otra vez 2026-09-25         artículos distinto al que ingest mostró a Claude (mismo bug
                             que el fix del 2026-09-15, perdido porque promote_wiki.yml
                             no promueve cambios en scripts/, solo wiki/ y
                             processed.json). Corregido de nuevo — ver wiki/log.md
                             2026-09-25 y scripts/ingest.py. Requiere merge manual del
                             PR de esta sesión para no perderse otra vez.
```

## ⚠️ Sísifo Reincidente (2026-09-25)

El fix de `promote_wiki.yml` del 2026-09-23 (pensado para que el trabajo de wiki de
ramas `claude/**` llegue a `main` sin depender de que el usuario mergee PRs a mano) no
resolvió el problema: **el workflow mismo está caído por la misma cuota de Actions
agotada**, y ha fallado en sus 8 corridas hasta la fecha. Resultado: **~30 PRs abiertos
sin mergear** (`#280`-`#311`), con ingestas de sesiones de routine entre 2026-09-15 y
2026-09-25 que nunca llegaron a `main`. Al menos 2 sesiones distintas (PR #311 y la
sesión del 2026-09-25) generaron el mismo lote de 5 "artículos pendientes" porque
ninguna ingesta previa se había promovido. Ver el detalle completo, incluida la
recomendación de revisión manual de PRs, en `wiki/log.md`, entrada 2026-09-25.

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
| 2026-09-16 → 2026-09-24 | ~90-100 (≥15 sesiones × 2 lotes de 5, estimado) | — | **Trabajo real pero atrapado en ~30 PRs sin mergear** (`#280`-`#311`) por la falla de `promote_wiki.yml`/cuota de Actions — no reflejado en `main`. Ver Hallazgo 1, wiki/log.md 2026-09-25 |
| 2026-09-25 | 10 (2 lotes de 5, 0 falsos positivos) | 4 | Routine automatizada, esta sesión (rama local). Fix REINCIDENTE de `mark_all_ingested` (regresión, ver Hallazgo 3). Páginas nuevas: `cafe_cacao.md`, `hortalizas.md`, `entities/iica_panama.md`. Diagnóstico reforzado: 19 días sin fetch nuevo, `promote_wiki.yml` caído en sus 8 corridas, ~30 PRs sin mergear |

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

**Estado a 2026-09-25**: la señal de alarma sigue ACTIVA y **sigue empeorando** (19 días
sin artículos nuevos, 19 ejecuciones de `wiki_daily.yml` fallando consecutivamente).
Además, se confirmó que `promote_wiki.yml` (creado el 2026-09-23 para mitigar esto)
también está caído por la misma causa (cuota de Actions), dejando ~30 PRs de sesiones
de routine sin mergear a `main`. Esta sesión no pudo resolver ninguna de las dos causas
raíz (requieren acceso a Settings → Billing / revisión y merge manual de PRs, fuera del
alcance de una sesión de routine). Ver diagnóstico completo en wiki/log.md, entrada
2026-09-25.
