---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 57 | ↑ continuo |
| Artículos ingestados al wiki | 36 | = total sin falsos positivos |
| Pendientes de ingesta | 21 | 0 |
| Falsos positivos acumulados (excluidos de la cola) | 24 (7 previos + 17 esta sesión) | **0 nuevos entrando al wiki** |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (mezcla semilla + real) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45+ (rango 2015→hoy agotado; ver nota) |
| Días sin artículos nuevos (sources/) | **17** (último commit real: 2026-09-06) | máx 3 antes de diagnosticar — **EXCEDIDO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida CON commit real  : 2026-09-06 (run #103, 0 artículos, pero job completó bien)
Última corrida del cron         : 2026-09-22 (se ejecuta a diario sin falta, 11:00 UTC)
Resultado últimas 16 corridas   : FALLA en ~3 segundos, runner_id=0 (nunca se asigna runner)
Causa identificada              : NO es un bug del script de fetch ni de GDELT/RSS — el job
                                   nunca llega a ejecutar ningún step (ni siquiera checkout).
                                   Patrón típico de límite de gasto/minutos de Actions agotado,
                                   o Actions deshabilitado a nivel de repo/organización.
Ventanas GDELT                  : 79 completadas (por encima del umbral de 45 → el rango de
                                   fechas 2015-hoy ya fue cubierto en corridas previas; el
                                   estancamiento actual NO es por agotamiento de rango sino
                                   por el fallo de infraestructura de Actions arriba descrito)
Acción requerida                : Revisar Settings → Billing and plans → Actions (o
                                   Settings → Actions → General) del repositorio en GitHub.
                                   Ver detalle completo en wiki/log.md (entrada 2026-09-23,
                                   "DIAGNÓSTICO CRÍTICO: GitHub Actions Fetch Diario roto").
Estado                           : NO RESUELTO — requiere acción del owner del repositorio,
                                   fuera del alcance de esta sesión de Claude Code.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

79 ventanas GDELT completadas (por encima de las ~45 estimadas para cubrir 2015→hoy). El
backfill histórico avanzó considerablemente entre 2026-06-22 y 2026-09-06 vía las corridas
exitosas de Actions (#90–#103), antes de que el fetch diario se rompiera (ver arriba). No se
dispone de un desglose por trimestre en `processed.json` (solo se registra la lista de
ventanas completadas); reconstruir esa tabla requeriría analizar los 79 rangos de fecha
directamente, lo cual queda fuera del alcance de esta sesión.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-23 | 5 (arroz/MIDA: importaciones, inundaciones, siembra 2022-23, transición ministerial, compensaciones) | 21 | Corregidos 2 bugs críticos en `mark-ingested`/`mark-all-ingested` (ver log.md); excluidos 17 falsos positivos nuevos de la cola; diagnosticado fallo de GitHub Actions desde 2026-09-07 (requiere acción del owner) |

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

**Nota permanente (desde 2026-09-23)**: si en una futura sesión "Días sin artículos nuevos"
sigue creciendo y la corrida más reciente de Actions sigue fallando en segundos con
`runner_id=0`, NO reabrir el diagnóstico de GDELT/RSS — el problema ya está identificado como
de infraestructura de Actions (billing/permisos) y requiere acción manual del owner. Verificar
primero si ya fue resuelto antes de re-diagnosticar desde cero.
