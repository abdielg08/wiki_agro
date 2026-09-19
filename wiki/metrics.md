---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 confirmados + 6 pendientes de marcar | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 28 (11 topics, 3 entities, 11 resúmenes, overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + refuerzo arroz/subsidios) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~46 estimadas | rango agotado, necesita expansión |
| Días sin artículos nuevos | **13** (desde 2026-09-06) | máx 3 antes de diagnosticar — EXCEDIDO |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa   : 2026-09-06 ("6 artículos nuevos descargados")
Corridas fallidas        : 10 consecutivas (runs #108-#116, 2026-09-10 → 2026-09-19)
                          conclusion=failure en TODAS, cron diario 11:00 UTC
Duración de cada run      : ~3-4s, con 0 ms de tiempo facturable en el job (nunca se aprovisionó)
Logs del job              : no disponibles (HTTP 404) — el runner no ejecutó ningún step
Causa identificada        : falla de infraestructura/cuenta de GitHub Actions (NO es un bug de
                          wiki_agro.py). Más probable: límite de gasto (spending limit) agotado,
                          o Actions deshabilitado a nivel de cuenta/repositorio.
Acción requerida          : el usuario debe revisar GitHub → Settings → Actions / Billing.
                          No corregible desde el código del repositorio.
Ventanas GDELT             : 79 completadas (> umbral de 45) → backfill histórico agotado, necesita
                          expansión del rango de años una vez restaurado el fetch diario.
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

> Tabla desactualizada: `sources/processed.json` reporta **79 ventanas GDELT completadas** (por
> encima del umbral de 45), pero no se reconstruyó aquí el desglose por año/trimestre en esta
> sesión para evitar inventar cifras no verificadas. Pendiente: recalcular esta tabla a partir de
> `_gdelt_windows` en `processed.json` y expandir el rango de años una vez resuelto el fallo de
> GitHub Actions documentado en "Estado del Fetch".

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-19 | 5 (arroz/subsidios/inundaciones) | 39 | Diagnóstico crítico: fetch diario Actions falla 10 corridas consecutivas desde 2026-09-10 (13 días sin artículos nuevos); 6 falsos positivos adicionales identificados pendientes de marcar |

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
