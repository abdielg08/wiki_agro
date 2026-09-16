---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-16
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 2 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | rango agotado — ver diagnóstico |
| Días sin artículos nuevos en sources/ | **10** (último: 2026-09-06) | máx 3 antes de diagnosticar — **ALERTA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions          : 2026-09-16 (run #113) — conclusion: failure
Corridas fallidas consecutivas  : 10 (runs #104-#113, 2026-09-07 → 2026-09-16)
Último commit con artículos     : 2026-09-06 ("6 artículos nuevos descargados", run #103, success)
Duración corridas fallidas      : ~4 segundos (vs. 6-8 min en corridas exitosas)
Causa identificada              : el job falla casi instantáneamente, antes del paso real de
                                   fetch — no es un problema de GDELT/RSS. El workflow file no
                                   cambió desde 2026-06-19, así que no es una regresión de código.
                                   Repo privado confirmado vía API. Hipótesis más probable:
                                   agotamiento de minutos incluidos de GitHub Actions del plan
                                   (2,000 min/mes en repos privados, plan Free), dado el consumo
                                   diario de 6-8 min desde finales de mayo 2026.
Logs detallados                 : no disponibles (404 al descargar vía API; consistente con job
                                   terminado por el runner antes de generar logs de step)
Acción requerida                : el usuario debe revisar Settings → Billing → Plans and usage →
                                   Actions minutes, y Settings → Actions → General en GitHub.
Hallazgo secundario             : 79 ventanas GDELT completadas, superando el umbral de 45 —
                                   el rango de fechas GDELT probablemente ya fue cubierto y
                                   necesitará expansión o revisión de la lógica de ventanas
                                   una vez restaurado el fetch.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | ? | ? | Ver processed.json — pendiente de desglose por trimestre |
| 2016-2025 | ? | ? | 79 ventanas completadas en total (acumulado, sin desglose por período) |
| **TOTAL** | **79/~45 estimadas** | **57 descargados** | **Rango probablemente agotado; fetch detenido desde 2026-09-07** |

> El desglose por trimestre no se ha reconstruido desde `processed.json` en esta sesión.
> Prioridad actual: restaurar el fetch de GitHub Actions (ver diagnóstico arriba) antes de
> continuar el backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-16 | 5 | 39 | Sesión routine; 0 falsos positivos nuevos. Diagnóstico avanzado: Actions fallando 10 días consecutivos (posible cuota de minutos agotada) |

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

**ALERTA ACTIVA (2026-09-16)**: 10 días sin artículos nuevos — muy por encima del umbral de 3.
Causa probable: cuota de minutos de GitHub Actions agotada (repo privado). Requiere intervención
del usuario en la configuración de billing de GitHub; no es resoluble desde una sesión de ingesta.
