---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 el 2026-08-03) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + ingestas reales) | 2015 → hoy real |
| Ventanas GDELT completadas | 61 (2017-2025 completos, 2015-2016 SIN CUBRIR, 2026 rolling) | 2015→hoy |
| Días sin artículos nuevos | 2 (última con artículos: 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-30 (3 artículos)
Corridas recientes                  : 2026-07-31 (0), 2026-08-02 (0)
Causa identificada (2026-08-03)     : fetch_ddg_search() no verificaba que la URL
                                       devuelta por ddgs coincidiera con el dominio
                                       "site:" configurado → 16 falsos positivos de
                                       fuentes globales (España, Brasil, Arabia Saudita,
                                       Utah/EE.UU., Malasia) etiquetados como prensa.com/PA
                                       por coincidencia de palabras clave genéricas
                                       (ej. "MIDA", "agricultura"). Ver wiki/log.md 2026-08-03.
Fix aplicado                        : scripts/fetch_news.py::fetch_ddg_search() ahora
                                       descarta resultados cuyo netloc no coincida con
                                       el "site" configurado. scripts/ingest.py::mark_ingested()
                                       corregido (crasheaba con la clave interna _gdelt_windows).
Estado post-fix                     : Pendiente validación en próxima corrida Actions
GDELT (revisado por trimestre)      : 2017 Q1 → 2025 Q4 completos (1 ventana c/u, 36 total).
                                       2026: ventana rolling 20260618→hoy que se re-ejecuta
                                       cada corrida (25 registros acumulados, esperado).
                                       2015 Q1 → 2016 Q4 (8 trimestres): CERO ventanas
                                       consultadas — brecha real, no agotamiento. Es el
                                       tramo prioritario pendiente del backfill histórico.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Sin cubrir — prioridad backfill** |
| 2016 Q1-Q4 | 0/4 | **Sin cubrir — prioridad backfill** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (rolling 20260618→hoy) | — | En curso (se re-consulta cada corrida) |
| **TOTAL trimestres 2015-2025** | **36/44** | **8 trimestres de 2015-2016 pendientes** |

> Nota (2026-08-03): estos datos vienen de un recuento real de `_gdelt_windows` en
> `sources/processed.json` (bucketed por trimestre de la fecha de inicio de cada
> ventana), no de una estimación. La tabla previa mostraba "0/46 — Backfill no
> iniciado", lo cual estaba desactualizado; el backfill de 2017-2025 ya se
> completó pero nunca generó artículos nuevos relevantes de Panamá para esos
> trimestres (0 artículos por ventana, o filtrados por falsos positivos antes
> del fix de esta sesión). El tramo 2015-2016 nunca fue consultado por GDELT —
> es la brecha real pendiente para cumplir el objetivo de cobertura
> "2015-02-19 → hoy".

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-03 | 0 (16 falsos positivos) | 0 | Fix causa raíz: `fetch_ddg_search()` sin verificación de dominio; fix bug `mark_ingested()` |

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
