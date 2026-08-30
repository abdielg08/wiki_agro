---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-30
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 51 | ↑ continuo |
| Artículos ingestados (marcados) | 18 | = total sin falsos positivos |
| Artículos pendientes de ingesta | 33 | 0 |
| Artículos reales ingestados al wiki | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Páginas en wiki/ | 25 (9 topics, 3 entities, 10 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 | 45+ (rango histórico ya cubierto; ventanas recientes son diarias) |
| Días consecutivos sin artículos nuevos | 2 (2026-08-28, 2026-08-29 — corridas Actions fallidas) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit nuevo : 2026-08-27 20:57 UTC (run #93, "1 artículos nuevos")
Corridas fallidas consecutivas  : run #94 (2026-08-28T21:16 UTC, failure, ~6s)
                                   run #95 (2026-08-29T15:23 UTC, failure, ~3s)
Causa identificada               : ambas corridas terminaron casi instantáneamente
                                    (3-6s) — descarta timeout de GDELT/RSS (tomaría
                                    minutos) y apunta a falla temprana del pipeline
                                    (checkout/setup-python/runner). Logs ya expirados
                                    en GitHub (404), causa exacta no confirmada.
Workflow sin cambios recientes    : .github/workflows/wiki_daily.yml no fue tocado
                                    recientemente — no es una regresión de config.
Corrida de hoy (2026-08-30)       : aún no ejecutada al momento de esta sesión
                                    (cron 11:00 UTC / 6am Panamá).
Acción requerida próxima sesión   : si la corrida de 2026-08-30 también falla, se
                                    alcanza el umbral de 3 días — escalar: revisar
                                    permisos de GITHUB_TOKEN, estado del runner, o
                                    correr workflow_dispatch manual para ver logs en vivo.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — sin iniciar** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — sin iniciar** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (ventanas diarias recientes) | 40 | En curso (fetch incremental, no backfill trimestral) |
| **TOTAL** | **76** | **2015-2016 son el único vacío real en la cobertura histórica** |

> Cifras calculadas directamente de `sources/processed.json` → `_gdelt_windows` (2026-08-30).
> **Hallazgo clave**: el backfill trimestral 2017-2025 está completo (36/36 ventanas), pero
> **2015 y 2016 no tienen ninguna ventana completada** — es el hueco real de cobertura frente
> a la meta de CLAUDE.md ("Cobertura objetivo: 2015-02-19 → hoy"). Priorizar estas 8 ventanas
> (2015 Q1-Q4, 2016 Q1-Q4) en el próximo fetch histórico.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-30 | 4 (+1 falso positivo excluido) | 33 | Routine automatizada; fix bug en `mark_ingested` (scripts/ingest.py); diagnóstico Actions (2 corridas fallidas); hueco de cobertura 2015-2016 identificado |

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
