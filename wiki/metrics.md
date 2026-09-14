---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-14
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 (+ ~20 detectados en la cola, no ingestados) | **0 nuevos ingestados** |
| Páginas en wiki/ | 26 (9 topics, 3 entities, 11 summaries, 2 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (parcial, sesgado a prensa.com reciente) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | ✅ superado — rango cubierto |
| Días sin artículos nuevos en sources/ | **8 días** (última descarga real: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions      : 2026-09-13 (run #110) — corre a diario, cron activo
Resultado                   : FAILURE — 7 corridas consecutivas fallidas (#104-#110,
                               2026-09-07 -> 2026-09-13), cada una de solo ~3-4s de duración
Última corrida EXITOSA      : #103, 2026-09-06 - commit 24cfc3c "6 artículos nuevos descargados"
Causa identificada           : NO CONFIRMADA. Duración ~3-4s por corrida es insuficiente para
                               completar checkout+setup-python+pip install+fetch, lo que sugiere
                               fallo temprano - probablemente en el paso final "Commit artículos
                               nuevos" (`git push`), ya que los pasos Fetch/Estadísticas tienen
                               continue-on-error:true y no deberían tumbar el job por sí solos.
                               Hipótesis: cambio de permisos del GITHUB_TOKEN o política de rama
                               que bloquea el push directo a main desde el 2026-09-07.
Bloqueo de diagnóstico        : no se pudieron descargar los logs crudos del job - la API de
                               GitHub devolvió HTTP 404 y el dominio
                               results-receiver.actions.githubusercontent.com está bloqueado
                               por el proxy de egress de esta sesión
Acción pendiente (usuario)   : revisar run #110 en la pestaña Actions de GitHub y confirmar
                               Settings -> Actions -> General -> Workflow permissions = "Read
                               and write permissions"
Ventanas GDELT                : 79 completadas - ya supera el umbral de 45; el rango histórico
                               parece agotado, no es la causa de la falta de artículos nuevos
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
| **TOTAL (histórico)** | **79/~46 estimadas** | 57 descargados | **Backfill GDELT completado/superado** |

> `_gdelt_windows` en `sources/processed.json` = 79, muy por encima de la estimación original de
> ~46 ventanas trimestrales. El script de fetch no reporta el desglose por trimestre en un formato
> legible desde esta sesión, por lo que la tabla de arriba (por período) no se actualizó con datos
> reales — solo se corrigió el total. El foco ahora ya no es el backfill histórico (parece agotado)
> sino: (1) resolver el fallo de GitHub Actions que impide nuevas descargas desde 2026-09-06, y
> (2) reducir el ruido de falsos positivos en la cola de pendientes (ver wiki/log.md, 2026-09-14).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-14 | 5 | 39 | Backfill prensa.com (arroz, transición MIDA, inundaciones); 0 falsos positivos; diagnóstico: Actions falla desde 2026-09-07 (8 días sin artículos nuevos) |

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
