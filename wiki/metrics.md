---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados (con página de wiki) | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 el 2026-08-15) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla, sin backfill real aún) | 2015 → hoy real |
| Ventanas GDELT completadas | 67 / ~45 estimadas | 45 (2015→hoy) — **estimación superada, revisar** |
| Días sin artículos nuevos REALES | 16 (último: 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions (histórico) : 2026-06-21 fix; corre diario desde entonces, "0 artículos nuevos"
Último artículo REAL de Panamá     : 2026-07-30 → 16 días sin avance real al 2026-08-15
Causa identificada (2026-08-15)    : scripts/fetch_news.py::fetch_ddg_search() (búsqueda
                                      "prensa_agro") no aplicaba el filtro _is_panama_related()
                                      que sí tienen RSS y GDELT. El operador site:prensa.com de
                                      DuckDuckGo no se respeta de forma confiable y "MIDA" es
                                      ambiguo (Malasia, Utah), así que los "artículos nuevos"
                                      descargados en días recientes eran 100% falsos positivos,
                                      no relacionados con Panamá ni con agro (ver wiki/log.md).
Fix aplicado                       : se agregó el guard _is_panama_related()/_is_blocked_domain()
                                      a fetch_ddg_search() (scripts/fetch_news.py), igual que
                                      RSS/GDELT. Se corrigió también un bug en
                                      scripts/ingest.py::mark_ingested() que crasheaba con
                                      AttributeError al iterar la clave interna _gdelt_windows.
Estado post-fix                    : pendiente validar en la próxima corrida de Actions que
                                      fetch_ddg_search ya no traiga resultados fuera de Panamá.
Ventanas GDELT (67, > ~45 est.)    : sugiere backfill histórico 2015→hoy ya cubierto, o que el
                                      generador de ventanas en fetch_historical.py está
                                      re-creando ventanas no alineadas a trimestre calendario
                                      (ver p.ej. "20260618_20260708" en _gdelt_windows).
                                      Pendiente de revisión en próxima sesión.
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
| 2026-08-15 | 0 | 0 | 16 falsos positivos detectados y descartados (0 páginas nuevas) + fix de fetch_ddg_search() (faltaba filtro Panamá) + fix de mark_ingested() (crash con _gdelt_windows) |

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
