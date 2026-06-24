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
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 21 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículo real nuevo | >30 (desde semilla 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-19 (último artículo guardado; Actions corre ~diario)
Resultado              : Sigue funcionando — pero TODOS los artículos recientes son falsos positivos
Causa raíz             : RSS de prensa.com retorna artículos de thestar.com.my (Malasia),
                         fox13now.com (Utah EEUU), ieeexplore.ieee.org (IEEE), worldbank.org
                         porque el keyword "MIDA" coincide con Malaysian Investment Dev. Authority
                         (no con el MIDA de Panamá).
Falsos positivos Jun   : 3 (thestar.com.my), 1 (fox13now), 1 (worldbank), 1 (thestar.com.my), 1 (IEEE)
Artículos reales recibidos: 0 (desde semilla del 2026-05-24)
Estado GDELT windows   : 21 completadas (2018-Q1 a 2026-Q2), pero 0 artículos reales producidos
Acción requerida       : Mejorar filtros de dominio en script fetch para excluir dominios
                         no-panameños: thestar.com.my, fox13now.com, ieeexplore.ieee.org, etc.
                         Revisar queries GDELT para Panama agriculture específicamente.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | Pendiente |
| 2016 Q1-Q4 | 0/4 | 0 | Pendiente (semilla: 1 artículo TVN manual) |
| 2017 Q1-Q4 | 0/4 | 0 | Pendiente |
| 2018 Q1-Q4 | 3/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2019 Q1-Q4 | 3/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2020 Q1-Q4 | 2/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2021 Q1-Q4 | 3/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2022 Q1-Q4 | 2/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2023 Q1-Q4 | 3/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2024 Q1-Q4 | 2/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2025 Q1-Q4 | 1/4 | 0 reales | Ventanas completadas, 0 agro PA |
| 2026 Q1-Q2 | 2/2 | 0 reales | Ventanas completadas, 0 agro PA |
| **TOTAL** | **21/46** | **0 reales** | **GDELT activo pero sin artículos reales** |

> PROBLEMA: GDELT/RSS está completando ventanas pero no produce artículos de agro panameño.
> Los 13 artículos en sources/ son semilla manual (6 reales) + falsos positivos (7).
> Acción requerida: revisar queries y filtros del script fetch.

> Ventanas completadas (de processed.json _gdelt_windows):
> 20180329-20260617 — 21 ventanas de ~3 meses cada una.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-06-24 | 0 | 0 | Diagnóstico: GDELT 21/46 ventanas completadas, 0 artículos reales producidos. RSS con ruido de fuentes no-panameñas. |

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
