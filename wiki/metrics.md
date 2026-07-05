---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-05
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (+5 esta sesión) | **0 nuevos** |
| Pendientes sin procesar | 1 (candidato a falso positivo: "Reef Saudi") | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~46 estimadas | 46 (2015→hoy) |
| Rango real cubierto por ventanas | 2017-03-30 → 2026-07-03 | 2015-02-19 → hoy |
| Días sin artículos nuevos | 2 (07-03 y 07-04 en cero; 07-05 aún no corre) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-04 (0 artículos nuevos)
Frecuencia             : diaria, commits "chore(sources): N artículos..." en main
Rendimiento reciente   : mayormente 0-1 artículo/día (pico de 3 el 2026-06-27)
Problema activo #1     : 45 ventanas GDELT completadas cubren 2017-03-30 → 2026-07-03,
                         pero el rango objetivo empieza 2015-02-19. El backfill temprano
                         (2015-2017, ~8 trimestres) nunca se generó — no es que el rango
                         esté "agotado", es que nunca arrancó desde el inicio real.
Problema activo #2     : colisión de acrónimo "MIDA" — GDELT/RSS traen resultados de
                         "Military Installation Development Authority" (Utah, EE.UU.) y
                         "Malaysian Investment Development Authority" (Malasia) en vez de
                         Ministerio de Desarrollo Agropecuario (Panamá). Causa 5/7 falsos
                         positivos previos y 5/6 pendientes de esta sesión.
Recomendación          : (1) revisar el generador de ventanas GDELT para que arranque en
                         2015-02-19; (2) agregar filtro geográfico ("Panama"/"Panamá") al
                         fetch antes de guardar en sources/articles/.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | **Falta generar** |
| 2016 Q1-Q4 | 0/4 | ? | **Falta generar** |
| 2017 Q1-Q4 | 3/4 | 0 | En curso (desde 2017-03-30) |
| 2018 Q1-Q4 | 4/4 | 0 | Completo |
| 2019 Q1-Q4 | 4/4 | 0 | Completo |
| 2020 Q1-Q4 | 4/4 | 0 | Completo |
| 2021 Q1-Q4 | 4/4 | 0 | Completo |
| 2022 Q1-Q4 | 4/4 | 0 | Completo |
| 2023 Q1-Q4 | 4/4 | 0 | Completo |
| 2024 Q1-Q4 | 4/4 | 0 | Completo |
| 2025 Q1-Q4 | 4/4 | 1 | Completo |
| 2026 Q1-Q2+ | 10/2 (ventanas de reintento acumuladas) | ~4 (incl. falsos positivos) | En curso |
| **TOTAL** | **45/46 estimadas** | **~1 real + falsos positivos** | **Falta backfill 2015-2017** |

> Conteo de ventanas tomado de `sources/processed.json:_gdelt_windows` (2026-07-05).
> El rendimiento real de GDELT es muy bajo (~0-1 artículo real/trimestre reciente) —
> la mayoría de "artículos" recuperados en 2026 son falsos positivos por la colisión MIDA.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-05 | 0 (5 revisados, 5/5 falsos positivos) | 1 | Colisión de acrónimo MIDA (Utah/Malasia) confirmada como causa raíz; backfill 2015-2017 pendiente de generar |

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
