---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos ingestados al wiki** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | ≥1 (ver diagnóstico) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-21 (última corrida confirmada; sin evidencia de
                         corridas exitosas entre esa fecha y 2026-08-09)
Resultado               : 16 artículos descargados desde entonces, 16/16 falsos
                         positivos (0 artículos reales de agro Panamá)
Causa identificada      : fetch_ddg_search() (búsqueda DuckDuckGo "prensa_agro",
                         site:prensa.com) no aplicaba los filtros
                         _is_blocked_domain()/_is_panama_related() que sí tienen
                         fetch_rss() y fetch_gdelt_batch(). El calificador site: de
                         ddgs.news() no se respeta de forma confiable → resultados de
                         dominios/países arbitrarios que matchean "agro" o el acrónimo
                         ambiguo "MIDA" (Malasia, Utah) se colaban con fuente
                         etiquetada "prensa.com".
Fix aplicado            : scripts/fetch_news.py::fetch_ddg_search() ahora aplica los
                         mismos guards que fetch_rss()/fetch_gdelt_batch() (commit
                         2026-08-09). También se corrigió mark_ingested() en
                         scripts/ingest.py, que fallaba con AttributeError por no
                         excluir la clave interna _gdelt_windows.
Estado post-fix         : Pendiente validación en próxima corrida Actions — debería
                         eliminar (o reducir drásticamente) los falsos positivos DDG.
Ventanas GDELT          : siguen en 0/~45 — el backfill histórico real (2015→hoy) NO
                         ha arrancado; solo se ha usado la búsqueda DDG diaria, que no
                         cubre el histórico.
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
| 2026-08-09 | 0 | 0 | 16 falsos positivos descartados (0 ingestados al wiki) + fix de raíz en fetch_ddg_search() + fix de mark_ingested() |

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
