---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-06-26
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
| Ventanas GDELT completadas | 36 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | **3** ⚠️ ALERTA | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-25 13:20 UTC
Resultado              : 0 artículos nuevos (3er día consecutivo)
Causa identificada     : GDELT backfill 36/46 ventanas completadas. Las ventanas
                         restantes (~10) cubren 2015-2016 donde GDELT v2 tiene
                         escasa cobertura de medios panameños en español.
                         RSS IICA y La Prensa: sin artículos agro nuevos.
                         Filtros anti-falsos-positivos funcionando correctamente.
Estado                 : ALERTA ⚠️ — 3 días sin nuevos artículos
Próxima acción         : Activar CDX Wayback Machine (fetch_historical.py) para
                         recuperar archivos La Prensa/TVN 2015-2016 cuando GDELT
                         agote sus ventanas sin resultados.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | ⏳ Pendiente (GDELT v2 inicia Feb 2015, cobertura escasa) |
| 2016 Q1-Q4 | 0/4 | ⏳ Pendiente (cobertura escasa en PA-SPA) |
| 2017 Q1 | 1/1 | ✅ Completo (20170330_20170628) |
| 2017 Q2-Q3 | 0/2 | ⏳ Pendiente |
| 2017 Q4 | 1/1 | ✅ Completo |
| 2018 Q1-Q4 | 4/4 | ✅ Completo |
| 2019 Q1-Q4 | 4/4 | ✅ Completo |
| 2020 Q1-Q4 | 4/4 | ✅ Completo |
| 2021 Q1-Q4 | 4/4 | ✅ Completo |
| 2022 Q1-Q4 | 4/4 | ✅ Completo |
| 2023 Q1-Q4 | 4/4 | ✅ Completo |
| 2024 Q1-Q4 | 4/4 | ✅ Completo |
| 2025 Q1 | 0/1 | ⏳ Pendiente |
| 2025 Q2-Q4 | 3/3 | ✅ Completo |
| 2026 Q1-Q2 | 3/3 | ✅ Completo (incl. ventana reciente) |
| **TOTAL** | **36/46** | **78% completado** |

> Las ~10 ventanas pendientes son principalmente 2015-2016. Dado que GDELT v2
> tiene cobertura limitada de prensa panameña en español para ese período, es
> esperable que retornen 0-pocos artículos reales. Complementar con CDX Wayback Machine.


---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-06-26 | 0 | 0 | Diagnóstico: 3 días sin nuevos artículos. GDELT 36/46 ventanas. Ver log. |

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
