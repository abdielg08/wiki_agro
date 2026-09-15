---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados (descartados) | ~14 | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 27 | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | rango agotado — ver nota abajo |
| Días sin artículos nuevos en sources/ | **9** (desde 2026-09-06) | máx 3 antes de diagnosticar — **⚠ SISTEMA EN FALLA** |

---

## Estado del Fetch (GitHub Actions) — Diagnóstico 2026-09-15

```
Última corrida con artículos nuevos : 2026-09-06 (run #103, 6 artículos)
Corridas fallidas consecutivas      : 8 (runs #104 a #111, 2026-09-07 a 2026-09-14)
Duración de cada corrida fallida    : ~3-5 segundos
Causa identificada                  : runner_id=0 en todos los jobs fallidos — el job nunca
                                       llegó a asignarse un runner de GitHub Actions. No es un
                                       error del script de fetch (GDELT/RSS): el job falla ANTES
                                       del checkout, en 3-5s, firma típica de cuota de minutos
                                       de Actions agotada, un problema de facturación/plan del
                                       repositorio, o una política de organización bloqueando
                                       runners.
Logs de los jobs                    : no disponibles vía API (HTTP 404) — consistente con que
                                       el job nunca llegó a ejecutarse en un runner real.
Ventanas GDELT                      : 79 completadas, muy por encima del umbral estimado de 45.
                                       No se puede confirmar que el backfill esté realmente
                                       agotado, ya que refleja corridas exitosas previas al corte
                                       del 2026-09-06, no actividad reciente.
Acción requerida (fuera del alcance de esta sesión)
                                     : revisar en GitHub → Settings → Billing/Actions si la
                                       cuota de minutos gratuitos del repositorio/organización se
                                       agotó, o si hay un problema de facturación/plan. Esta
                                       sesión de Claude Code no tiene acceso para modificar
                                       billing/plan de GitHub.
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
| 2026-09-15 | 5 | 39 | Routine automatizada. 0 falsos positivos entre los 5 ingestados. Diagnóstico: fetch de GitHub Actions falla 8 días consecutivos (runner nunca asignado) — ver sección "Estado del Fetch" |

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
