---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-01
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 51 | ↑ continuo |
| Artículos ingestados (total, incl. falsos positivos marcados) | 18 | = total sin falsos positivos |
| Artículos reales ingestados (con página en wiki/) | 10 | — |
| Falsos positivos acumulados | 8 | **0 nuevos** (1 detectado esta sesión) |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 | ~46 estimadas (2015→hoy) — meta superada |
| Días sin commit nuevo en sources/ | 5 (último: 2026-08-27) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA  : run #93, 2026-08-27 20:51 UTC (0 artículos nuevos, conclusion=success)
Últimas 4 corridas      : run #94 (2026-08-28), #95 (2026-08-29), #96 (2026-08-30), #97 (2026-08-31)
                          TODAS conclusion=failure, duración ~3s, sin runner asignado, logs 404
Diagnóstico (2026-09-01) : Falla ANTES de que el job arranque (no hay pasos ejecutados, no hay
                          logs descargables) — no es un error de GDELT/RSS/red ni del código de
                          fetch. Patrón típico de: límite de minutos/spending limit de GitHub
                          Actions agotado, o Actions deshabilitado/pausado a nivel de repo/cuenta.
Acción requerida        : el usuario debe revisar Settings → Billing → Plans and usage
                          (spending limit de Actions) y Settings → Actions → General del repo
                          abdielg08/wiki_agro. Esta sesión no tiene acceso para corregirlo.
Cron programado         : diario 11:00 UTC (6:00 AM hora Panamá) — no cambió, sigue activo
Impacto                 : 5 días sin nuevos artículos en sources/ (2026-08-27 → 2026-09-01)
                          — supera el umbral de 3 días de la definición de éxito
```

---

## Progreso del Backfill GDELT (2015 → hoy)

```
Ventanas GDELT completadas (sources/processed.json → _gdelt_windows): 76
```

> 76 ventanas ya completadas — supera la estimación original de ~46 ventanas para 2015→hoy.
> El desglose por trimestre no se recalculó en esta sesión; pendiente de una auditoría dedicada
> que cruce `_gdelt_windows` contra el calendario 2015-2026 para confirmar cobertura real vs.
> duplicados. Lo relevante para el diagnóstico de hoy: el backfill histórico SÍ avanzó bastante;
> el problema actual es el fetch DIARIO (wiki_daily.yml), que dejó de correr con éxito desde el
> 2026-08-27 (ver "Estado del Fetch" arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-01 | 4 (+1 falso positivo detectado) | 33 | Fix bug en `mark_ingested()` (crasheaba con `_gdelt_windows`); diagnóstico: fetch diario en fallo desde 2026-08-27 (spending limit / Actions deshabilitado — requiere acción del usuario) |

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
