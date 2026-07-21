---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (7 previos + 11 esta sesión) | **0 nuevos** desde el fix de fetch_ddg_search |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2017-03-30 → 2026-07-18 (ventanas GDELT) | 2015-02-19 → hoy real |
| Ventanas GDELT completadas | 51 / ~46 estimadas | rango 2015-02-19→hoy agotado en el tramo cubierto; falta expandir hacia atrás |
| Días sin artículos nuevos | 1 (último: 2026-07-20) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-20 (2 artículos nuevos)
Resultado              : fetch diario funcionando con normalidad
Ventanas GDELT         : 51 completadas, cubren continuamente 2017-03-30 → 2026-07-18
                         SIN cubrir 2015-02-19 → 2017-03-29 (~2 años de historia faltante)
Acción sugerida        : disparar wiki_historical.yml (workflow_dispatch, mode=gdelt)
                         con years="2015-2017" para cerrar el hueco de backfill
```

## Diagnóstico de Falsos Positivos (2026-07-21)

```
Hallazgo   : 11/11 artículos pendientes esta sesión eran falsos positivos
             (Malasia, Utah EE.UU., Irán, Arabia Saudita, paper técnico 6G,
             catálogo de zoología brasileña — ninguno sobre Panamá)
Causa raíz : fetch_ddg_search() en scripts/fetch_news.py no verificaba el
             dominio real del resultado ni aplicaba _is_blocked_domain() /
             _is_panama_related(), a diferencia de fetch_rss() y
             fetch_gdelt_batch(). El operador site: de DuckDuckGo no se
             respeta de forma confiable.
Fix        : aplicado en esta sesión — ver wiki/log.md 2026-07-21 08:05.
Además     : se corrigió un bug separado en mark_ingested() (scripts/ingest.py)
             que crasheaba al iterar la clave interna _gdelt_windows.
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
| 2026-07-21 | 0 | 0 | 11 falsos positivos rechazados (0 ingestados, 0% contaminación) + fix de causa raíz en fetch_ddg_search() + fix de bug en mark_ingested() |

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
