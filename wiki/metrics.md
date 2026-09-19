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
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 28 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45 (2015→hoy) — **umbral superado, rango agotado** |
| Días sin artículos nuevos | **13** (último: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ FALLA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions con ÉXITO : Run #103, 2026-09-06 13:50 UTC (6 artículos nuevos)
Corridas fallidas consecutivas   : Runs #104-#115 (2026-09-07 → 2026-09-18), 12 días seguidos
Patrón de falla                  : cada run falla en ~3-4 segundos, runner_id=0,
                                    runner_name vacío → el job NUNCA llega a asignarse
                                    a un runner. No es un fallo de código (GDELT/RSS/red).
Causa probable                   : cuota de minutos de GitHub Actions agotada, límite de
                                    gasto en $0, o Actions deshabilitado a nivel de repo/cuenta.
Logs de jobs fallidos            : no disponibles vía API (HTTP 404 — expirados)
Ventanas GDELT                   : 79 completadas, supera el umbral de 45 → rango de fechas
                                    de backfill agotado, necesita expansión
Estado                           : ⚠ ACCIÓN REQUERIDA del propietario — revisar GitHub →
                                    Settings → Actions y Billing → Plans & usage
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
| 2026-09-19 | 5 | 39 | Fetch de Actions detenido 13 días (ver Estado del Fetch); requiere acción del propietario |

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
