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
| Artículos en sources/ | 50 | ↑ continuo |
| Artículos ingestados (total) | 18 | = total sin falsos positivos |
| Artículos reales ingestados (excl. falsos positivos) | 17 | ↑ continuo |
| Falsos positivos acumulados | 8 (7 previos + 1 nuevo 2026-08-26) | **0 nuevos** por sesión |
| Pendientes de ingesta | 32 | 0 |
| Páginas en wiki/ | 24 (8 topics, 3 entities, 10 summaries, ~3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 75 (`_gdelt_windows` en processed.json) | 45-46 (2015→hoy) — **superado** |
| Días sin artículos nuevos | 1 (última corrida Actions 2026-08-25 trajo 0) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-25 (commit a8ccd35→4908c54)
Resultado 2026-08-25    : 0 artículos nuevos
Resultado 2026-08-24    : 20 artículos nuevos (última corrida productiva)
Racha reciente          : 0,0,0,20,0,0,1,0,0,0,0,0,0,0,0 (últimos ~15 días,
                           más reciente primero) — fetch corre a diario pero
                           trae artículos nuevos de forma intermitente.
Diagnóstico (Paso 4)    : `_gdelt_windows` = 75 completadas, superando el
                           umbral de ~45-46 ventanas estimadas para cubrir
                           2015→hoy. Según CLAUDE.md esto sugiere que el
                           rango de fechas GDELT ya está agotado y el fetch
                           puede estar reintentando ventanas ya cubiertas
                           sin encontrar contenido nuevo. Recomendado:
                           revisar scripts/fetch_historical.py para
                           verificar si necesita expansión de rango o
                           una fuente adicional (RSS IICA/La Prensa activos).
Estado                  : Sin fallo crítico (días_sin_nuevos=1 < 3), pero
                           el ritmo de nuevos artículos se está desacelerando
                           — monitorear en próximas sesiones.
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
| 2026-08-26 | 4 (+1 falso positivo excluido) | 32 | Fix de bug en `mark-ingested` (AttributeError con `_gdelt_windows`); GDELT windows en 75 (>45 umbral) |

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
