---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-13
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
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (mezcla semilla + reales) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45-46 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 7 (último fetch exitoso: 2026-09-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa (con artículos) : 2026-09-06 (run #103) — 6 artículos nuevos
Última corrida Actions                 : 2026-09-12 (run #109) — FAILURE
Runs consecutivos fallidos             : 6 (runs #104-#109, 2026-09-07 a 2026-09-12, uno por día)
Patrón del fallo                       : cada run termina en ~3-4s con conclusion=failure,
                                          sin runner_id/runner_name asignado — el job nunca
                                          llega a ejecutar el step de checkout ni de fetch
Causa identificada                     : problema de infraestructura/cuota de GitHub Actions
                                          (minutos agotados, workflow pendiente de aprobación,
                                          o permisos), NO un bug en fetch_gdelt_historical()
                                          ni en los fetchers RSS (esos steps tienen
                                          continue-on-error y ni siquiera se alcanzan)
Acción requerida                       : el usuario debe revisar
                                          github.com/abdielg08/wiki_agro/settings/actions
                                          (cuota de minutos, aprobaciones pendientes) —
                                          no corregible desde una sesión de Claude Code
Ventanas GDELT completadas             : 79 (superó el estimado de 45-46 para 2015→hoy)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — sin cobertura** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — sin cobertura** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (parcial) | 43 ventanas | En curso (año en curso, granularidad menor a trimestral) |
| **TOTAL** | **79 ventanas** | **2017-2025 cubierto; 2015-2016 sin ventanas GDELT aún** |

> Basado en `sources/processed.json` → `_gdelt_windows` (conteo real al 2026-09-13).
> **Brecha identificada**: 2015-02-19 → 2016-12-31 no tiene ninguna ventana GDELT registrada,
> pese a ser el inicio de la cobertura objetivo definida en CLAUDE.md. Priorizar estas ventanas
> en el próximo backfill histórico (`wiki_historical.yml`, ejecución manual) una vez resuelto
> el problema de Actions descrito en "Estado del Fetch".

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-13 | 5 | 39 | 0 falsos positivos; creadas precios_mercados.md y subsidios_programas.md; diagnóstico: Actions fallando 6 días consecutivos (ver Estado del Fetch) |

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
