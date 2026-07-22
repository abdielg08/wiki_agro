---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados (con página wiki) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos publicados en wiki** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 52 / ~45-46 estimadas | rango agotado, necesita expansión |
| Días sin artículos nuevos reales (no-FP) | ≥3 (desde semilla 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions (commit en sources/) : 2026-07-21 — 0 artículos nuevos
Corridas previas                            : 07-20 (2 nuevos), 07-19 (0),
                                               07-18 (0), 07-15 (1)
Ventanas GDELT completadas                  : 52 (≥ 45-46 estimadas para 2015→hoy)
Diagnóstico                                 : rango de fechas GDELT AGOTADO —
  el backfill histórico ya cubrió las ventanas disponibles. Los "artículos
  nuevos" que sigue trayendo el fetch ya no vienen de GDELT sino de la fuente
  genérica "prensa.com" (RSS/búsqueda por palabra clave), que está produciendo
  ~100% falsos positivos por colisión de "MIDA" (Malasia, Utah) y de
  "agriculture" genérico (UNESCO, IEEE, gremios de EE.UU., Arabia Saudita) —
  ver wiki/log.md 2026-07-22 para el detalle de 11 falsos positivos de una sola
  sesión.
Acción requerida (fuera del alcance de esta sesión de ingesta, para revisión
  de scripts/fetch_news.py o config/sources.yaml):
  1. Expandir/rotar las ventanas GDELT (nuevo rango) o aceptar que el backfill
     GDELT terminó y ese canal ya no aportará más.
  2. Restringir la fuente prensa.com con filtro de país=Panamá / palabras
     clave de contexto agropecuario panameño antes de guardar en sources/,
     o bajarla de prioridad frente a fuentes oficiales (MIDA, IDIAP, IICA).
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
| 2026-07-22 | 0 (11/11 revisados = falsos positivos) | 0 | Colisión "MIDA" (Malasia/Utah) + "agriculture" genérico en fuente prensa.com; ventanas GDELT agotadas (52); fix de bug en `mark_ingested()` (scripts/ingest.py) |

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
