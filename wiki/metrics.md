---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos ingestados (total) | 18 | = total sin falsos positivos |
| Artículos reales ingestados (con contenido wiki) | 6 | ↑ continuo |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Pendientes de ingesta | 12 (todos `prensa.com`, probable falso positivo) | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 2 (última: 2026-08-19) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-08-20 (0 artículos nuevos)
Última corrida con contenido : 2026-08-19 (1 artículo nuevo)
Estado                       : Actions corre diariamente sin fallar (commits
                                "chore(sources): N artículos nuevos" cada día).
                                2 días consecutivos sin artículos nuevos —
                                dentro del umbral normal (alarma a los 3 días).

PROBLEMA ACTIVO (2026-08-21): la fuente `prensa.com` (búsqueda web
`prensa_agro` en config/sources.yaml, DuckDuckGo/ddgs con site:prensa.com +
query que incluye "MIDA" suelto) tiene 0% de rendimiento real: de 24
artículos descargados bajo ese source, 0 son de La Prensa de Panamá y los
24 son falsos positivos por colisión de acrónimo "MIDA" (Malaysian
Investment Development Authority, Utah Military Installation Development
Authority) o por términos genéricos de agricultura de otros países
hispanohablantes (Aragón, España). Ver diagnóstico completo en wiki/log.md
(entrada 2026-08-21). Recomendado corregir o desactivar esta búsqueda.
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
| 2026-08-21 | 0 reales (5 falsos positivos marcados) | 12 | 5/5 revisados eran falsos positivos (MIDA Utah/Malasia); diagnóstico de causa raíz en log.md — fuente `prensa_agro` con 0% rendimiento real |

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
