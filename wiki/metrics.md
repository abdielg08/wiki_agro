---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-16
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 (histórico) + ≥5 detectados hoy sin marcar (ver nota) | **0 nuevos ingestados como agro-PA** |
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (artículos reales: 2015-2025) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45 (2015→hoy) — **umbral superado** |
| Días sin artículos nuevos en sources/ | **10** (último commit de fetch con contenido: 2026-09-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions      : 2026-09-15 (run #112, "Wiki Agropecuario — Fetch Diario")
Resultado                   : FALLA — conclusion="failure"
Racha de fallas             : 9 corridas diarias consecutivas en failure (runs #104 a #112,
                               2026-09-07 → 2026-09-15). Última corrida exitosa: run #103,
                               2026-09-06 (6 artículos descargados).
Causa identificada          : No se pudo determinar la causa exacta — los logs del job ya no
                               están disponibles para descarga (HTTP 404 al pedirlos vía API
                               de GitHub Actions / blob storage; WebFetch a ese dominio también
                               bloqueado por el proxy de egress de esta sesión). Los pasos
                               "Fetch artículos nuevos" y "Estadísticas" del workflow tienen
                               `continue-on-error: true`, así que la falla probablemente ocurre
                               en checkout / setup-python / pip install / o en el paso final
                               "Commit artículos nuevos" (git add/commit/push), que SÍ puede
                               abortar el job.
Hallazgo adicional           : `_gdelt_windows` en sources/processed.json ya tiene **79**
                               ventanas completadas, por encima del umbral de ~45 estimado en
                               CLAUDE.md para "rango de fechas agotado". Aun si el workflow se
                               arregla, GDELT puede estar devolviendo cada vez menos artículos
                               nuevos porque el rango 2015→hoy ya fue mayormente recorrido.
Acción recomendada           : (1) Revisar manualmente el run en
                               https://github.com/abdielg08/wiki_agro/actions/runs/34987787411
                               desde la UI de GitHub (esta sesión no tiene acceso a los logs
                               crudos). (2) Si el fallo es en el commit/push, revisar permisos
                               del token/branch protection en `main`. (3) Considerar expandir el
                               rango de ventanas GDELT o activar más fuentes RSS dado que el
                               backfill histórico está cerca de agotarse.
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
| 2026-09-16 | 5 (todos arroz/MIDA, 100% verificados agro-PA) | 39 | Routine automatizada. Fetch Diario en falla 9 días seguidos; GDELT en 79 ventanas (>45). Fuentes de estos 5 artículos sin `full_text` (solo extracto truncado) — ver wiki/log.md |

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
