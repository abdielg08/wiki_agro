---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-12
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 11 | = total sin falsos positivos |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 25 (8 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2017 Q1 → hoy (backfill parcial) | 2015-02-19 → hoy real |
| Ventanas GDELT históricas completadas | 37 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos en sources/ | **6** (última corrida exitosa: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit nuevo : 2026-09-06 (run #103, "6 artículos nuevos descargados")
Corridas posteriores            : #104 (09-07), #105 (09-08), #106 (09-09),
                                   #107 (09-10), #108 (09-11) → conclusion: failure
Duración de cada corrida fallida: ~3 segundos, runner_id=0 (nunca se asignó un runner
                                   y ningún step llegó a ejecutarse — no es un error
                                   dentro de wiki_agro.py ni de checkout/pip install)
Cambios de código en el período : NINGUNO — no hay commits a wiki_agro.py,
                                   requirements.txt ni .github/workflows/ entre
                                   2026-09-06 y 2026-09-11 que expliquen el cambio
Causa identificada               : Falla a nivel de infraestructura de GitHub Actions
                                   (el job nunca inicia — patrón típico de límite de
                                   minutos/cuota de Actions agotado, o Actions
                                   deshabilitado/restringido a nivel de cuenta/repo).
                                   NO es un bug de GDELT/RSS ni del pipeline de fetch.
Logs detallados                  : no accesibles desde esta sesión (el dominio de
                                   descarga de logs de Actions —
                                   productionresultssa12.blob.core.windows.net— está
                                   bloqueado por la política de red de este entorno)
Acción requerida (fuera de este repo) : el dueño de la cuenta de GitHub debe revisar
                                   Settings → Billing/Actions usage del repo/organización
                                   para confirmar si se agotaron los minutos incluidos
                                   o si hay una restricción de facturación activa.
                                   Una vez resuelto, el siguiente `workflow_dispatch`
                                   o corrida programada debería volver a producir commits.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

37 ventanas trimestrales históricas completadas de forma continua desde
**2017-03-30** hasta **2026-06-17**. Faltan ~8 ventanas para cubrir
2015-02-19 → 2017-03-29 (el inicio real de cobertura GDELT v2).

Además del backfill histórico, `_gdelt_windows` registra 42 ventanas
"rolling" adicionales con inicio fijo en 2026-06-18 y fin creciente día a
día (hasta 2026-09-03) — esto sugiere que el fetch diario reciente usa una
ventana separada de "noticias recientes" en vez de avanzar el backfill
histórico. No se modificó el código en esta sesión; se documenta como
observación para una futura revisión del fetch script.

| Período | Estado |
|---------|--------|
| 2015-02-19 → 2017-03-29 | Pendiente (backfill no ha llegado a estos años) |
| 2017-03-30 → 2026-06-17 | 37 ventanas completadas |
| 2026-06-18 → 2026-09-03 (reciente) | 42 ventanas "rolling" completadas |
| **TOTAL histórico** | **37 / ~45 estimadas** |

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-12 | 5 (reales, 0 falsos positivos) | 39 | Ver wiki/log.md — además: alarma de 6 días sin fetch exitoso |

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

**Estado 2026-09-12**: alarma en 6 días. Diagnóstico apunta a un problema de
infraestructura de GitHub Actions (no de código) — ver sección "Estado del
Fetch" arriba. Requiere acción del dueño de la cuenta fuera de este repo.
