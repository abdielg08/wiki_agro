---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-28
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos reales ingestados | 18 (17 con contenido + 1 falso positivo marcado) | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos | 1 (última corrida: 2026-08-27) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-27 20:57 UTC
Resultado               : 1 artículo nuevo (foot-and-mouth-vaccine, no agro-Panamá — pendiente evaluación)
Corridas previas        : 2026-08-25 (0 nuevos), 2026-08-24 (20 nuevos)
Ventanas GDELT          : 76 completadas — supera el umbral de 45 estimadas para cobertura 2015→hoy.
                          Diagnóstico (CLAUDE.md Paso 4.2): con 45+ ventanas completadas, el rango de fechas
                          configurado está agotado y necesita expansión para seguir trayendo artículos nuevos
                          vía GDELT. Revisar scripts/fetch para ampliar el rango o rotar queries.
Fuentes activas         : RSS IICA y La Prensa siguen aportando artículos ocasionales fuera de GDELT.
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
| 2026-08-28 | 4 (+1 falso positivo descartado) | 33 | Routine automatizada; detectado patrón de mal etiquetado source/country en fetch (2do caso: Mozambique) |

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
