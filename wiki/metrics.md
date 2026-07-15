---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 21 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 15 | **0 nuevos** (8 nuevos detectados y documentados hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2017-03 → 2026-07 (GDELT parcial) | 2015-02-19 → hoy real |
| Ventanas GDELT completadas | 48 (con solapes) | rango 2015→hoy sin huecos |
| Días sin artículos nuevos | 1 | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-14 (1 artículo nuevo descargado)
Resultado 2026-07-15   : 0 pendientes al inicio de sesión, 8 revisados de sesión anterior
Causa raíz encontrada  : web_search "prensa_agro" (DDG) no valida el dominio real de los
                         resultados ni exige mención de "Panamá" — 15/21 artículos históricos
                         (71%) son falsos positivos de esta única fuente.
Fix aplicado hoy       : scripts/fetch_news.py — fetch_ddg_search() ahora valida dominio real
                         (urlparse) y exige "panam" en título+cuerpo antes de aceptar resultado.
                         scripts/ingest.py — mark_ingested() ya no crashea con la clave interna
                         _gdelt_windows (usa article_entries() como mark_all_ingested).
Pendiente de validar   : próximas corridas de Actions deben mostrar 0 falsos positivos de DDG.
Problema abierto       : ventana GDELT 2015-01-01→2017-03-29 nunca se completó; el ciclo parece
                         re-consultar la ventana más reciente cada día en vez de retroceder en
                         el tiempo. Requiere revisión de fetch_gdelt_historical() — no resuelto
                         en esta sesión.
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
| **TOTAL** | **48 ventanas registradas (con solapes)** | **6 artículos reales vía GDELT/RSS** | **Hueco 2015-01-01→2017-03-29 sin completar; requiere revisión del ciclo de backfill** |

> Las 48 ventanas en `_gdelt_windows` no cubren un rango limpio: la más antigua inicia en
> 2017-03-30, no en 2015-01-01. 11 de ellas comparten el inicio "20260618" con distintos
> finales (ventana final re-consultada día a día). Ver diagnóstico en wiki/log.md (2026-07-15).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-15 | 0 (8/8 falsos positivos) | 0 | Fix de bug en mark_ingested (_gdelt_windows) + fix de fetch_ddg_search (validación de dominio + exigencia de "Panamá") |

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
