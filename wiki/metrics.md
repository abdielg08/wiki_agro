---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-06-25
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
| Ventanas GDELT completadas | 32 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 2 (Jun 23 y Jun 24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-24T13:12 UTC
Resultado              : 0 artículos nuevos (commit "chore(sources): 0 artículos nuevos")
Causa identificada (Jun 24):
  1. RSS IICA     → "0 entradas en el feed"
  2. RSS LaPrensaGeneral → "0 entradas en el feed"
  3. DDG web search → todas las búsquedas: "No results found" (posible rate-limit DDG)
  4. GDELT backfill → múltiples ventanas con 403/429 (rate-limit GDELT API)
     - Ventanas con 0 artículos: 2017-03-30→06-28, 2019-09-26→12-25,
       2020-03-26→06-24, 2021-06-24→09-22, 2022-03-24→06-22,
       2022-09-22→12-21, 2022-12-22→2023-03-22, 2024-03-21→06-19,
       2024-12-19→2025-03-19, 2025-09-18→12-17, 2026-06-18→06-23
     - Ventanas con 403/429 bloqueadas: ~7 ventanas de 2015-2018, 2019, 2017, 2025-2026
  5. World Bank API → ejecutó pero 0 artículos nuevos

Estado actual (Jun 25):
  - Actions del Jun 25 aún no ha corrido (horario programado pendiente)
  - 2 días consecutivos sin artículos nuevos (Jun 23, Jun 24) → ALERTA en 1 día más
  - GDELT rate-limiting es el bloqueador principal del backfill

Acciones recomendadas:
  - Aumentar delay entre solicitudes GDELT (actualmente puede ser demasiado rápido)
  - Considerar implementar back-off exponencial en errores 403/429
  - Revisar si DDG cambió su API — todas las búsquedas retornan "No results found"
  - RSS feeds de IICA y La Prensa puede que hayan cambiado su URL o estructura
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas completadas | Artículos agro PA | Estado |
|---------|---------------------|-------------------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | Bloqueadas por 403/429 |
| 2016 Q1-Q4 | 0/4 | 0 | Bloqueadas por 403/429 |
| 2017 Q1-Q4 | 1/4 | 0 | Parcial — 0 resultados en ventanas exitosas |
| 2018 Q1-Q4 | 3/4 | 0 | Parcial — 0 resultados en ventanas exitosas |
| 2019 Q1-Q4 | 4/4 | 0 | Completo — 0 artículos agro PA encontrados |
| 2020 Q1-Q4 | 5/5 | 0 | Completo — 0 artículos agro PA encontrados |
| 2021 Q1-Q4 | 5/5 | 0 | Completo — 0 artículos agro PA encontrados |
| 2022 Q1-Q4 | 5/5 | 0 | Completo — 0 artículos agro PA encontrados |
| 2023 Q1-Q4 | 4/4 | 0 | Completo — 0 artículos agro PA encontrados |
| 2024 Q1-Q4 | 4/4 | 0 | Completo — 0 artículos agro PA encontrados |
| 2025 Q1-Q4 | 2/4 | 0 | Parcial — 0 artículos agro PA encontrados |
| 2026 Q1-Q2 | 2/2 | 0 | Completo — 0 artículos agro PA encontrados |
| **TOTAL** | **~32/46** | **0** | **En progreso — GDELT rate-limited** |

> GDELT retorna 0 artículos agro Panama en todas las ventanas exitosas. Posibles causas:
> 1. Query demasiado restrictivo (requiere múltiples keywords simultáneos)
> 2. GDELT no indexa bien medios panameños pequeños
> 3. Los artículos reales están en URLs que GDELT no captura

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-06-25 | 0 | 0 | Diagnóstico: GDELT rate-limited, RSS vacíos, DDG sin resultados |

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
