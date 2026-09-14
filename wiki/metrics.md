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
| Falsos positivos acumulados | 7 | **0 nuevos** (0 en esta sesión) |
| Páginas en wiki/ | 26 (9 topics, 3 entidades, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | artículos entre 2016–2025 ingestados; pendientes desde 2007 | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45 (2015→hoy) — **superado** |
| Días sin artículos nuevos en sources/articles/ | **8** (última descarga real: 2026-09-06) | máx 3 antes de diagnosticar |

**⚠ ALERTA**: 8 días sin artículos nuevos — supera el umbral de 3 días. Ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-09-06 (run #103, 6 artículos, conclusion=success)
Corridas desde entonces             : #104 (09-07) a #110 (09-13) — 7 corridas, TODAS con conclusion=failure
Duración de las corridas fallidas   : ~3 segundos (vs. ~5-6 min en corridas exitosas)
Señal clave                         : runner_id=0, runner_name="" en el job — el job NUNCA llegó a
                                       ejecutarse en un runner (falla antes de "actions/checkout")
Repo                                 : privado (private: true) → consume minutos de Actions del plan
                                        (2,000 min/mes gratis, compartidos entre TODOS los repos privados
                                        de la cuenta abdielg08, no solo wiki_agro)
Causa más probable                  : cuota de minutos de GitHub Actions agotada para la cuenta
                                        (el patrón runner_id=0 + fallo instantáneo es la firma típica de
                                        "spending limit reached" / minutos agotados, no un error de código)
Causas descartadas                  : el workflow YAML no cambió desde su único commit (a5b03de);
                                        no hay corridas de wiki_historical.yml que hayan consumido minutos
                                        extra; GDELT no es la causa — el job falla antes de correr Python
Acción requerida (fuera del alcance de esta sesión)
                                     : el usuario debe revisar https://github.com/settings/billing/summary
                                       — esperar el reset mensual de minutos, aumentar el límite de gasto,
                                       o hacer público el repositorio (minutos ilimitados en repos públicos)
Estado post-diagnóstico              : Pendiente de que el usuario resuelva el límite de Actions;
                                       el código de fetch en sí no está confirmado como roto
```

---

## Progreso del Backfill GDELT (2015 → hoy)

`sources/processed.json._gdelt_windows` reporta **79 ventanas completadas**, muy por encima de las
~45 estimadas para cubrir 2015→hoy. Esto indica que el rango de fechas configurado ya fue recorrido
en su totalidad (posiblemente con ventanas más finas que trimestres, o repetidas por reintentos).
No se dispone de un desglose por período almacenado — solo el conteo agregado. El cuello de botella
actual **no es GDELT**: es que el job de GitHub Actions no está llegando a ejecutarse (ver "Estado del
Fetch" arriba).

| Período | Estado |
|---------|--------|
| 2015 → hoy | Ventanas GDELT agotadas (79/~45) — rango ya cubierto, backfill de descubrimiento no es el limitante |
| Ingesta al wiki | 18/57 artículos descargados ya ingestados; 39 pendientes en cola |

> Próximo paso útil cuando GDELT sea el cuello de botella real: expandir el rango de fechas o afinar
> palabras clave en `fetch_historical.py`. Por ahora, el paso crítico es resolver el fallo de Actions.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-14 | 5 (arroz/MIDA, prensa.com) | 39 | 0 falsos positivos. Se detectó y corrigió bug de `mark-all-ingested` /
`mark-ingested` en scripts/ingest.py (ver wiki/log.md). Diagnóstico: GitHub Actions lleva 7 corridas
consecutivas fallando (runner nunca asignado) desde 2026-09-07 — probable cuota de minutos agotada
en la cuenta (repo privado); requiere acción del usuario en la configuración de billing de GitHub. |

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
