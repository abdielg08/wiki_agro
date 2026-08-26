---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-26
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 50 | ↑ continuo |
| Artículos ingestados (marcados) | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 32 | 0 |
| Falsos positivos acumulados | 8 (7 previos + 1 nuevo 2026-08-26) | **0 nuevos** |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + ingesta parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 75 (superó estimado de 45) | rango agotado — necesita expansión |
| Días sin artículos nuevos (último run Actions) | 1 (última carga real: 2026-08-24, 20 artículos) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-25 (0 artículos nuevos)
Última carga con datos : 2026-08-24 (20 artículos nuevos)
Resultado               : Actions SÍ está corriendo diariamente (commits [skip ci] casi todos los días)
Diagnóstico 2026-08-26  : Ventanas GDELT completadas = 75, muy por encima del umbral de 45
                          indicado en CLAUDE.md → el rango de fechas disponible en GDELT
                          está agotado (no quedan ventanas nuevas por cubrir con la
                          configuración actual). Los 20 artículos del 08-24 probablemente
                          vinieron de RSS (IICA / La Prensa) más que de GDELT.
Acción recomendada      : expandir la lógica de ventanas GDELT (nuevo rango de fechas,
                          términos de búsqueda adicionales, o fuentes RSS adicionales)
                          para seguir alimentando sources/articles/.
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
| 2026-08-26 | 4 reales + 1 falso positivo descartado (5 marcados) | 32 | Ver wiki/log.md; fix de bug en scripts/ingest.py::mark_ingested() |

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
