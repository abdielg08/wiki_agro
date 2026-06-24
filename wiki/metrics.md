---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-06-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 13 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2024 (semilla manual) | 2015 → hoy real |
| Ventanas GDELT completadas | 21 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 1 (último: 2026-06-23 → 0) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-23
Resultado              : 0 artículos nuevos
Causa identificada     : Bug en fetch_gdelt_batch() — _is_panama_related() sobre-filtraba
                         artículos legítimos de fuentes PA que no mencionan "Panamá" en título
                         Ej: "MIDA presenta semillas certificadas" (mida.gob.pa) → RECHAZADO
Fix aplicado (2026-06-24): Eliminado _is_panama_related() de fetch_gdelt_batch()
                           GDELT ya filtra por sourcecountry:PA — doble filtro era incorrecto
                           21 ventanas GDELT completadas previas tendrán que volver a correr
                           (sus artículos fueron rechazados, ventanas ya marcadas como completas)
Estado post-fix        : Pendiente validación en próxima corrida Actions (hoy ~11:00 UTC)
Próxima acción         : Si 2026-06-24 Actions trae 0 artículos → resetear _gdelt_windows
                         para que vuelvan a consultarse con el filtro corregido
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
| **TOTAL** | **21/46** | **0 útiles** | **Bug filtro corregido 2026-06-24** |

> Las 21 ventanas completadas rechazaron artículos válidos por el bug del filtro.
> Después de resetear _gdelt_windows, esas ventanas serán re-consultadas con el fix.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-06-24 | 0 | 0 | Diagnóstico: bug _is_panama_related en GDELT corregido; 21 ventanas históricas necesitan reset |

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
