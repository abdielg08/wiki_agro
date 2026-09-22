---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados (esta sesión) | 0 | **0 nuevos** |
| Páginas en wiki/ | 28 | ↑ continuo |
| Cobertura temporal (sources/articles/) | 2016-2025 (datos reales, ver detalle abajo) | 2015 → hoy real |
| Ventanas GDELT completadas | ver `_gdelt_windows` en processed.json | 45 (2015→hoy) |
| Días sin artículos nuevos en sources/ | **16 días** (último commit: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA          : 2026-09-06 (run #103, wiki_daily.yml, 6 artículos)
Corridas fallidas consecutivas  : 16 (run #104 al #119, 2026-09-07 → 2026-09-22)
Duración de las corridas fallidas: ~3-5 segundos (vs. ~4-6 minutos en corridas exitosas)
Diagnóstico                     : El job "Fetch artículos → Commit a sources/" nunca
                                   llega a asignarse un runner (runner_id=0, runner_name="")
                                   y falla antes del paso "actions/checkout" — no es un
                                   error de código de wiki_agro.py ni de GDELT/RSS.
                                   Patrón típico de: límite de gasto/minutos de GitHub
                                   Actions agotado, Actions deshabilitado a nivel de
                                   cuenta/repo, o política de runners bloqueando el job.
Logs de job                     : No disponibles (404) — consistente con que el job
                                   nunca corrió en un runner real.
Acción requerida                : Revisar en GitHub (Settings → Actions, y
                                   Settings → Billing → Plans and usage) si hay un
                                   límite de minutos/gasto alcanzado o si Actions está
                                   deshabilitado para abdielg08/wiki_agro. Esto requiere
                                   acceso del dueño de la cuenta — no se puede corregir
                                   editando el workflow o el código del repo.
Workaround aplicado esta sesión : Ninguno automático posible; se documenta el hallazgo
                                   aquí y en wiki/log.md para que el usuario lo resuelva.
                                   Mientras tanto, la ingesta manual vía Claude Code
                                   (sesión interactiva) sigue avanzando el backlog de
                                   los 57 artículos ya descargados antes del corte.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

`sources/processed.json._gdelt_windows` reporta **79 ventanas** marcadas como completadas
(vs. la estimación original de ~45-46 para todo 2015→hoy), con cobertura observada desde
2017 hasta 2026. Esto ya supera la meta original de ventanas, pero **no** garantiza
cobertura completa 2015-2016 ni ausencia de huecos — no se detectaron ventanas de 2015 ni
2016 en la muestra revisada.

**Anomalía detectada**: hay múltiples ventanas distintas con el mismo inicio
`20260618_...` y distintos finales (`_20260623`, `_20260627`, `_20260703`, `_20260707`,
`_20260714`, `_20260727`, `_20260801`, `_20260902`, `_20260903`, …), lo que sugiere que el
crawler histórico pudo haber reintentado/expandido la misma ventana repetidamente en vez
de avanzar limpiamente por trimestre. No se investigó a fondo en esta sesión (routine
diaria, no backfill histórico) — queda como hallazgo para una sesión de mantenimiento del
`wiki_historical.yml`.

> Backfill activo mayormente vía sources/ ya descargados (57 artículos, 5 fuentes de
> confianza + prensa.com). El detalle de ventanas por año/trimestre requiere una
> auditoría dedicada de `_gdelt_windows`, no incluida en esta sesión de routine.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-22 | 5 (0 falsos positivos) | 39 | Routine programada. Hallazgo crítico: `wiki_daily.yml` lleva **16 corridas fallidas consecutivas** (2026-09-07 → 2026-09-22), job nunca asignado a runner — requiere revisión de Actions/billing por el dueño de la cuenta |

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
