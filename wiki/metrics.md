---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-11
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 4 (MIDA Malasia, thestar.com.my) | **0 nuevos** |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2016–2025 (artículos ingestados) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45+ (rango agotado, necesita expansión) |
| Días sin artículos nuevos en sources/ | **5** (última descarga: 2026-09-06) | máx 3 antes de diagnosticar → **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con resultado    : 2026-09-06 (commit 24cfc3c, "6 artículos nuevos descargados")
Días sin nuevas descargas       : 5 (hoy: 2026-09-11) → supera el umbral de 3 días
Ventanas GDELT (_gdelt_windows) : 79 completadas (≥45 → rango de fechas agotado, necesita expansión)
Anomalía detectada              : decenas de ventanas con prefijo "20260618_2026..." (p.ej.
                                   20260618_20260624, 20260618_20260627, ...) parecen ventanas
                                   diarias/cortas generadas desde 2026-06-18, inconsistentes con
                                   el patrón trimestral del resto del histórico (2017-2026).
                                   Podrían estar inflando el conteo sin aportar cobertura real.
Diagnóstico                     : no se puede confirmar desde esta sesión si GitHub Actions dejó
                                   de correr, si corrió sin encontrar artículos nuevos, o si el
                                   bug de ventanas está bloqueando el backfill real. Requiere
                                   revisión de los logs de Actions (fuera del alcance de esta
                                   routine, que solo tiene acceso al repo, no al panel de CI).
Acción recomendada              : (1) revisar ejecución de Actions desde 2026-09-06; (2) revisar
                                   generación de ventanas GDELT (posible bug de granularidad
                                   diaria vs. trimestral desde 2026-06-18); (3) si el rango está
                                   realmente agotado, expandir la ventana de backfill.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | ? | ? | Sin confirmar (no distinguible con el bug de ventanas diarias) |
| 2016 Q1-Q4 | ✓ (parcial) | 1 ingestado | En progreso |
| 2017 Q1-Q4 | ✓ | 0 ingestados | En progreso |
| 2018 Q1-Q4 | ✓ | 1 ingestado | En progreso |
| 2019 Q1-Q4 | ✓ | 0 ingestados | En progreso |
| 2020 Q1-Q4 | ✓ | 1 ingestado | En progreso |
| 2021 Q1-Q4 | ✓ | 1 ingestado | En progreso |
| 2022 Q1-Q4 | ✓ | 2 ingestados | En progreso |
| 2023 Q1-Q4 | ✓ | 1 ingestado | En progreso |
| 2024 Q1-Q4 | ✓ | 3 ingestados | En progreso |
| 2025 Q1-Q4 | ✓ | 1 ingestado | En progreso |
| 2026 (parcial, con anomalía de ventanas diarias) | 40+ ventanas cortas | 0 ingestados | **Revisar bug de granularidad** |
| **TOTAL** | **79/45+ (rango agotado)** | **18 ingestados de 57 descargados** | **Backfill en progreso, requiere auditoría de ventanas** |

> Nota: esta tabla es una estimación basada en las fechas de los artículos ya ingestados
> (2016, 2018, 2020-2025) y en `_gdelt_windows`; no hay un mapeo exacto ventana→trimestre en
> `processed.json`, por lo que la columna "Ventanas" usa ✓ cuando hay evidencia de artículos
> de ese año y "?" cuando no se puede confirmar.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-11 | 5 (arroz, precios/subsidios, inundaciones) | 39 | 0 falsos positivos nuevos; fetch automático detenido desde 2026-09-06 (5 días) |

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

> **Estado actual: alarma activa (5 días sin descargas nuevas).** Ver diagnóstico completo en
> `wiki/log.md`, entrada `2026-09-11 00:05`.
