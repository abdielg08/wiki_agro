---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-13
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
| Falsos positivos acumulados | 7 (previos, ya excluidos vía skip_reason) | **0 nuevos esta sesión** |
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45+ (rango agotado, ver diagnóstico) |
| Días sin artículos nuevos en sources/articles | **7** (última descarga real: 2026-09-06) | máx 3 antes de diagnosticar → **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA (con commit)  : 2026-09-06 (run #103) — 6 artículos nuevos
Corridas desde entonces               : #104 (09-07) a #109 (09-12) — 6 corridas CONSECUTIVAS
                                         con conclusion="failure"
Duración de las corridas fallidas     : ~3 segundos (13:48:24 → 13:48:27), sin runner_id asignado
Causa identificada                    : STARTUP FAILURE — el job nunca llega a ejecutar ningún step
                                         (ni siquiera actions/checkout). No es un fallo de código
                                         (GDELT/RSS) ni de timeout de red: el runner nunca se asigna.
                                         Los logs del job ya no están disponibles vía API (404) por
                                         ser demasiado cortos/antiguos para inspección detallada.
Hipótesis más probable                : límite de minutos incluidos de GitHub Actions agotado o
                                         "spending limit" en $0 para la cuenta/organización, o
                                         Actions deshabilitado a nivel de repo/cuenta — esto requiere
                                         revisión MANUAL en GitHub (Settings → Actions / Billing),
                                         no es corregible desde el código del repositorio.
Ventanas GDELT                        : 79 completadas (>45) → el rango histórico configurado está
                                         agotado; en cuanto el fetch se restablezca, evaluar expandir
                                         el rango de años en fetch-historical.
Acción pendiente del usuario           : revisar en GitHub → Settings → Actions → General si Actions
                                         está habilitado, y en Settings → Billing si hay minutos o
                                         "spending limit" disponibles para Actions.
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
| 2026-09-13 | 5 | 39 | 0 falsos positivos; creadas topics/precios_mercados.md y topics/subsidios_programas.md; detectado fallo de GitHub Actions (6 corridas consecutivas con startup_failure desde 2026-09-07) |

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
