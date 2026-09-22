---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 (incluye contaminación — ver Estado del Fetch) | 0 |
| Falsos positivos acumulados | 7+ (ver hallazgo 2026-09-22 en log.md; cola actual tiene más sin marcar) | **0 nuevos** |
| Páginas en wiki/ | 28 (11 topics, 3 entities, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (parcial, ver backfill) | 2015 → hoy real |
| Ventanas GDELT completadas | 38 fechas de inicio únicas / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos en sources/ | **16 días** (último commit: 2026-09-06) | máx 3 antes de diagnosticar — **ALERTA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit a sources/ : 2026-09-06 (commit 24cfc3c, "6 artículos nuevos")
Días sin commits a sources/          : 16 (hoy: 2026-09-22) — ALERTA: supera umbral de 3 días
Diferencia vs. fallos previos        : corridas anteriores SÍ commiteaban aunque fuera "0 artículos
                                        nuevos"; aquí no hay commits en absoluto → sospecha de que el
                                        workflow dejó de correr o falla antes del paso de commit,
                                        no solo que no encuentra artículos.
Backfill GDELT                       : 38 fechas de inicio de ventana únicas de ~45 estimadas
                                        (<45 ⇒ posible bloqueo/timeout, según umbral de CLAUDE.md)
Hueco de cobertura                   : ventanas registradas van de 2017-03-30 a 2026-06-18;
                                        el rango 2015-02-19 → 2017-03-29 (~8 trimestres) no tiene
                                        NINGUNA ventana registrada — el backfill no ha llegado al
                                        inicio real de la cobertura objetivo (2015).
Patrón de reintentos                 : 41 de 79 entradas en _gdelt_windows comparten el mismo
                                        inicio (20260618) con distintos fines — reintentos repetidos
                                        atascados en la ventana más reciente.
Contaminación de la cola             : inspección manual de pending_ingest detectó múltiples
                                        falsos positivos evidentes en prensa.com (Utah data centers,
                                        Aragón/España, Brasil, Mozambique, catálogo de dípteros, etc.)
                                        — ver detalle en wiki/log.md 2026-09-22 00:05.
Acción recomendada                   : (1) usuario debe revisar la pestaña Actions de GitHub para
                                        confirmar si el workflow programado sigue activo;
                                        (2) próxima sesión debe priorizar ventanas GDELT 2015-2017
                                        sobre reintentar 2026-06-18;
                                        (3) reforzar filtro de relevancia (Panamá) en el fetcher.
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
| 2026-09-22 | 5 (0 falsos positivos) | 39 (cola contaminada, ver Estado del Fetch) | Routine automatizada; detectado fetch de Actions detenido 16 días + hueco de backfill 2015-2017 |

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
