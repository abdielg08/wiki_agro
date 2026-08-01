---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-01
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 nuevos 2026-08-01) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 60 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos | ~2 (última descarga con contenido: 2026-07-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-31 (0 artículos nuevos; último día con contenido: 2026-07-30, 3 nuevos)
Resultado              : Pendientes de ingesta = 0 tras esta sesión (16 falsos positivos descartados)
Causa identificada #1  : _gdelt_windows = 60, ya supera las ~45 ventanas estimadas para
                         cubrir 2015→hoy → el rango GDELT disponible está agotado y
                         necesita expandirse (nuevas ventanas / trimestres) para seguir
                         trayendo artículos históricos.
Causa identificada #2  : fetch_ddg_search() (fuente "prensa.com" vía DuckDuckGo News)
                         no aplicaba _is_blocked_domain() ni _is_panama_related(),
                         a diferencia de fetch_rss()/fetch_gdelt_batch(). Esto dejó pasar
                         16 artículos no relacionados con Panamá (colisión de siglas MIDA
                         con Malasia/Utah, y agro genérico de Arabia Saudita, España,
                         Brasil, etc. — ver wiki/log.md 2026-08-01 para detalle completo).
Fix aplicado           : Se agregaron ambos filtros a fetch_ddg_search() en
                         scripts/fetch_news.py (commit de esta sesión, 2026-08-01).
Estado post-fix        : Pendiente validación en próxima corrida Actions.
                         Ventanas GDELT (60) aún requieren expansión de rango — no resuelto
                         en esta sesión, requiere decisión sobre cómo ampliar backfill.
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
| 2026-08-01 | 0 | 0 | 16 falsos positivos descartados (colisión siglas MIDA + agro genérico global) + fix de fetch_ddg_search() sin filtro Panamá + diagnóstico GDELT (60/45 ventanas, rango agotado) |

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
