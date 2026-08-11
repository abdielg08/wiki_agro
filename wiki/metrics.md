---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-11
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** (5 detectados hoy, no ingestados) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 64 (con gap 2015-2017 + 27 duplicadas cerca de hoy) | 45 (2015→hoy) sin gaps ni duplicados |
| Días sin artículos nuevos | 1+ (0 nuevos hoy 2026-08-11) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-10 (previas: 2026-08-07, 2026-08-04)
Resultado              : 0 artículos nuevos en las últimas 3 corridas registradas
Causa identificada #1  : GAP histórico real 2015-01-01 → 2017-03-29 (9
                         trimestres) — GDELT falla en red para fechas tan
                         antiguas en cada corrida, la ventana nunca se marca
                         completa, nunca avanza. NO es "rango agotado".
Causa identificada #2  : 27 ventanas duplicadas/solapadas con inicio fijo
                         20260618 y fin creciente día a día — bug de cálculo
                         cuando `current` queda a <90 días de `end`(=ayer).
                         Cada corrida re-consulta casi el mismo rango,
                         desperdiciando cuota en su mayoría duplicados.
                         Detalle técnico en wiki/log.md (2026-08-11 00:05).
Falso positivo detectado: colisión de keyword "MIDA" trae artículos de la
                         Malaysian Investment Development Authority y de la
                         Utah Military Installation Development Authority,
                         etiquetados incorrectamente con country="PA".
                         5/5 del lote de hoy — 0 ingestados.
Estado                 : Pipeline corre según cron diario, pero NO avanza el
                         backfill 2015-2017 y desperdicia cuota en 2026.
                         Recomendado (fuera de alcance de esta rutina):
                         arreglar fetch_gdelt_historical() en
                         scripts/fetch_news.py (ver log.md), sumar fuentes
                         Nivel 3 (Panamá América, TVN, La Estrella), y
                         filtrar por país/entidad en el matching de "MIDA".
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
| 2026-08-11 | 0 | 11 | 5/5 pendientes eran falsos positivos (colisión "MIDA"); diagnóstico de gap GDELT 2015-2017 y ventanas duplicadas 2026 |

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
