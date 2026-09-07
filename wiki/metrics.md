---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-07
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Artículos pendientes de ingesta | 39 | 0 (objetivo por sesión) |
| Falsos positivos acumulados | 7+ (ver nota) | **0 nuevos** |
| Páginas en wiki/ | 29 (12 topics, 3 entidades, 11 resúmenes) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (`_gdelt_windows`) | ≥45 (2015→hoy) — **superado** |
| Días sin artículos nuevos en sources/ | 1 (última descarga: 2026-09-06) | máx 3 antes de diagnosticar |

> Nota falsos positivos: además de los 7 previos, el fetch histórico había capturado artículos de "MIDA" en el sentido de *Malaysian Investment Development Authority* (thestar.com.my) y un caso de fox13now.com (Utah, EEUU) sin relación con Panamá. Todos están marcados `skipped: true` con `skip_reason` en `sources/processed.json` — no se ingestaron en esta ni en sesiones previas.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-09-06 (commit 24cfc3c, 6 artículos)
Resultado sesión de hoy (2026-09-07): 0 artículos nuevos en sources/ al momento de esta
                                       routine (origin/main sin commits nuevos de sources/ hoy)
Ventanas GDELT                      : 79 completadas — supera el estimado de 45 para
                                       cobertura 2015→hoy; se observan ventanas que se
                                       solapan/repiten (p.ej. "20260618_20260714",
                                       "20260618_20260801", "20260618_20260902")
Acción sugerida                     : revisar en próxima sesión si fetch_gdelt_historical()
                                       está generando ventanas duplicadas o solapadas
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
| 2026-09-07 | 5 (arroz/MIDA, 0 falsos positivos) | 39 | Creadas: precios_mercados.md, subsidios_programas.md, veraguas.md, darien_comarca.md |

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
