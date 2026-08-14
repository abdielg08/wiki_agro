---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-14
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 67 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 8 corridas consecutivas (desde 2026-07-31) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-14
Resultado              : 0 artículos nuevos (8ª corrida consecutiva en 0 desde 2026-07-30)
Causa identificada      : Ventanas GDELT completadas = 67, superan las ~45 estimadas para
                          cubrir 2015→hoy en franjas de 90 días → el rango de fechas de la
                          query actual está agotado, no está trayendo contenido nuevo.
                          RSS (IICA, La Prensa) sin confirmar en esta sesión (sin acceso de
                          red interactivo); el historial de commits sugiere 0 aportes recientes.
Acción pendiente        : Ampliar términos de búsqueda GDELT o afinar franjas de fecha en
                          scripts/fetch_news.py / scripts/fetch_historical.py.
                          Además, fetch_historical.py aún no tiene el AND-require de mención
                          de Panamá que sí tiene fetch_news.py::_gdelt_query_string() — esto
                          causó los 5 falsos positivos de "MIDA" no panameño de esta sesión.
Estado                  : Requiere sesión dedicada al fetch (fuera del alcance de esta rutina)
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
>
> **Nota 2026-08-14**: `_gdelt_windows` en `processed.json` ya registra 67 ventanas
> completadas (ver "Estado del Fetch" arriba), muy por encima de las 46 de esta tabla.
> La tabla de arriba quedó desactualizada y no se recalculó en esta sesión por falta de
> mapeo ventana→trimestre; pendiente de recomputar en una sesión dedicada al fetch.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-14 | 0 | 11 | 5/5 rechazados como falsos positivos (colisión "MIDA" no panameño); GDELT con 67 ventanas completadas — rango de fechas agotado, requiere expansión de query en próxima sesión de fetch |

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
