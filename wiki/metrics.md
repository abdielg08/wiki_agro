---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos publicados en wiki** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~45 estimadas | 45 (2015→hoy) — **rango agotado** |
| Días sin artículos nuevos (git) | 4 (desde 2026-07-04) | ⚠️ excede máx 3 |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit registrado : 2026-07-04 12:08 UTC ("0 artículos nuevos")
Días sin NINGÚN commit de Actions    : 4 (07-05, 07-06, 07-07, 07-08) ⚠️ FALLA
Ventanas GDELT completadas           : 45 → rango de fechas agotado (backfill
                                        histórico necesita expansión de ventanas)
Causa más probable                   : el workflow de Actions dejó de ejecutarse
                                        por completo (no es solo "0 artículos");
                                        no se puede confirmar RSS IICA/La Prensa
                                        desde esta sesión interactiva
Acción pendiente (usuario)           : revisar pestaña Actions del repo en GitHub
                                        para confirmar si el cron sigue activo
Diagnóstico completo                 : ver wiki/log.md, entrada 2026-07-08 08:45
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
| 2026-07-08 | 0 (6 falsos positivos rechazados) | 0 | Colisión de acrónimo "MIDA" (Utah/Malasia) + 1 art. no-Panamá. Fix de 2 bugs en `mark_ingested`/`mark_all_ingested` (ver log.md). GDELT en 45/45 ventanas — backfill agotado. Actions sin commits desde 2026-07-04. |

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
