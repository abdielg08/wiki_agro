---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-07
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 3 (último: 2026-07-04, "1 artículo") | máx 3 antes de diagnosticar — **ALARMA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit en sources/ : 2026-07-04 (hace 3 días respecto a hoy 2026-07-07)
Resultado esa corrida                 : "0 artículos nuevos descargados"
Sin commits en sources/ desde         : 2026-07-05, 2026-07-06, 2026-07-07 (0 corridas registradas)
Ventanas GDELT completadas            : 45 (>= 45 → rango de fechas 2015-2026 agotado)
Diagnóstico                           : Doble causa probable:
  1. GDELT: las 45 ventanas históricas (2015→hoy) ya se completaron — no hay
     más rango que backfillear con la config actual. Necesita expansión del
     rango de fechas (ventanas hacia el presente/futuro) para seguir trayendo
     artículos nuevos.
  2. GitHub Actions: no hay commits en sources/ en los últimos 3 días
     (07-05, 07-06, 07-07), lo que sugiere que el workflow no corrió en esas
     fechas o corrió sin generar commit — a diferenciar de "corrió y no
     encontró nada" (que sí generaría un commit "0 artículos nuevos" como el
     de 07-04 y 07-03).
Acción recomendada                    : (a) Revisar el historial de runs del
  workflow de GitHub Actions para confirmar si se ejecutó en 07-05/06/07 y
  por qué no generó commit; (b) expandir la ventana GDELT más allá de las
  45 completadas o añadir una fuente RSS adicional para no depender solo de
  IICA y La Prensa.
Riesgo colateral detectado esta sesión: además del estancamiento de fechas,
  el fetch de "prensa.com" está trayendo falsos positivos por colisión del
  acrónimo "MIDA" con entidades no panameñas (ver wiki/log.md 2026-07-07
  16:14) — 13 falsos positivos acumulados hasta ahora. Se recomienda agregar
  un filtro de "Panamá"/"Panama" en el texto o dominio antes de encolar.
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
| 2026-07-07 | 0 | 0 | 6 falsos positivos rechazados (colisión acrónimo "MIDA"); fix de bug en `mark_ingested()`; diagnóstico de estancamiento del fetch (0 commits en sources/ en 3 días, 45/45 ventanas GDELT agotadas) |

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
