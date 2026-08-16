---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-16
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 69 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos | 17 (desde 2026-07-30) | máx 3 antes de diagnosticar — **⚠ alarma activa** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-16 (corre regularmente, cada 1-3 días)
Resultado               : 0 artículos nuevos desde 2026-07-30 (17 días, 10+ corridas)
Causa identificada       : (1) _gdelt_windows = 69 ventanas completadas (≥45) → rango de
                            fechas GDELT agotado, necesita expansión del período cubierto.
                            (2) fetch_ddg_search() (scripts/fetch_news.py) no validaba el
                            dominio real del resultado contra search_cfg["site"] — el
                            operador site:prensa.com de DuckDuckGo no es confiable y
                            devolvía artículos internacionales sin relación con Panamá,
                            inflando pending_ingest.md con basura (16/16 pendientes hoy
                            eran falsos positivos: Utah, Malasia, España/Aragón, Arabia
                            Saudita, Brasil, Irán, EEUU).
Fix aplicado (2026-08-16): fetch_ddg_search() ahora exige que el dominio del resultado
                            coincida con search_cfg["site"] y pasa por _is_blocked_domain()
                            antes de aceptarlo (mismo patrón que fetch_rss()). También se
                            corrigieron 2 bugs en scripts/ingest.py: mark_ingested()
                            crasheaba con _gdelt_windows (no-dict) en processed.json, y
                            mark_all_ingested() marcaba artículos distintos a los
                            realmente revisados (usa find_pending() sin score en vez del
                            orden de prioritize() usado por `ingest`).
Estado post-fix          : Pendiente validación en próxima corrida Actions. El rango
                            GDELT agotado (69≥45) sigue siendo la causa probable de que
                            el conteo de artículos nuevos siga bajo incluso después del
                            fix — requiere expandir el período de backfill en
                            scripts/fetch_historical.py.
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
| 2026-08-16 | 0 | 0 | 16/16 pendientes eran falsos positivos (DDG site: no confiable). Fix de fetch_ddg_search() + 2 bugs en ingest.py |

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
