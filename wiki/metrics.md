---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-11
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
| Falsos positivos acumulados | 7 | **0 nuevos** (0 detectados en esta sesión) |
| Páginas en wiki/ | 25 | ↑ continuo |
| Cobertura temporal | artículos ingestados hoy: 2022, 2024, 2025 | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45+ (rango histórico ya cubierto) |
| Días sin artículos nuevos en sources/ | **5** (último: 2026-09-06) | máx 3 antes de diagnosticar → **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA con push  : 2026-09-06 (run #103) — 6 artículos nuevos
Últimas 4 corridas (#104-#107)   : 2026-09-07, 09-08, 09-09, 09-10 → FALLAN, conclusion=failure
Duración de las corridas fallidas: ~4 segundos (vs. ~5-6 min en corridas exitosas)
Diagnóstico                      : runner_id=0, runner_name="" en las 4 corridas fallidas →
                                    el job nunca llegó a asignarse a un runner; falla antes del
                                    paso "actions/checkout" (no es un fallo del script Python ni
                                    de GDELT/RSS). Logs del job no disponibles (HTTP 404 al
                                    descargarlos), consistente con un job que nunca inició
                                    ejecución real.
Causa raíz más probable           : límite de minutos/cuota de GitHub Actions agotado, o restricción
                                    a nivel de repositorio/organización sobre runners — requiere
                                    revisión en GitHub Settings → Actions/Billing por el dueño del
                                    repositorio (fuera del alcance de esta sesión de Claude Code).
Corrida de hoy (2026-09-11)       : aún no se había disparado al momento de este diagnóstico
                                    (cron 11:00 UTC / ~6:00 AM Panamá)
Acción recomendada                : el usuario debe verificar en
                                    github.com/abdielg08/wiki_agro/settings/actions y en la
                                    facturación de Actions si hay minutos agotados o ejecuciones
                                    bloqueadas; también revisar disponibilidad del runner ubuntu-latest.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | Pendiente |
| 2016 Q1-Q4 | 0/4 | ? | Pendiente |
| 2017 Q1-Q4 | 0/4 | ? | Pendiente |
| 2018 Q1-Q4 | 0/4 | ? | Pendiente |
| 2019 Q1-Q4 | 0/4 | ? | Pendiente |
| 2020 Q1-Q4 | 0/4 | ? | Pendiente |
| 2021 Q1-Q4 | 0/4 | ? | Pendiente |
| 2022 Q1-Q4 | 0/4 | ? | Pendiente |
| 2023 Q1-Q4 | 0/4 | ? | Pendiente |
| 2024 Q1-Q4 | 0/4 | ? | Pendiente |
| 2025 Q1-Q4 | 0/4 | ? | Pendiente |
| 2026 Q1-Q2 | 0/2 | ? | Pendiente |
| **TOTAL** | **0/46** | **0** | **Backfill no iniciado** |

> Una vez que Actions corra con el código corregido, actualizar esta tabla con los datos reales.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-11 | 5 | 39 | Sesión automatizada; 0 falsos positivos; diagnosticado fallo del fetch diario de Actions (4 corridas consecutivas fallidas desde 09-07, ~4s cada una, sin runner asignado) |

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
