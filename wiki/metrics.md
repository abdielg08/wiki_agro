---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados (total) | 18 | = total sin falsos positivos |
| — páginas reales creadas | 11 | resúmenes en wiki/summaries/ |
| Falsos positivos acumulados | 7 | **0 nuevos esta sesión** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 25 (8 topics, 3 entidades, 11 resúmenes, 2 overview, 1 log, 1 metrics) | ↑ continuo |
| Cobertura temporal | 2015-2025 (artículos reales) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45+ (umbral alcanzado) |
| Días sin artículos nuevos en sources/ | **9** (último commit: 2026-09-06) | máx 3 — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA    : run #103, 2026-09-06 13:50 UTC → commit 24cfc3c (6 artículos)
Corridas fallidas desde   : run #104 al #112 (2026-09-07 → 2026-09-15), 9 corridas
                             diarias consecutivas, TODAS conclusion=failure
Duración de cada corrida  : ~30-35s (falla temprana; fetch/stats tienen
                             continue-on-error:true, así que no pueden ser
                             la causa — el sospechoso es checkout/pip install
                             o, más probablemente, el `git push` final)
Logs del job              : NO accesibles vía API de GitHub (HTTP 404) ni por
                             descarga directa (bloqueado por política de red
                             de este entorno) — no se confirmó el paso exacto
Hipótesis principal       : rechazo del `git push` del bot wiki-agro-bot
                             (posible cambio en branch protection de `main`
                             o en permisos de Actions, alrededor del 2026-09-06/07)
Ventanas GDELT            : 79 completadas — supera el umbral de 45; el
                             backfill histórico probablemente ya cubrió gran
                             parte de 2015→hoy vía GDELT; lo bloqueado ahora
                             es el fetch diario (RSS + GDELT incremental) por
                             el mismo fallo de push
Acción requerida (usuario): revisar GitHub → Settings → Actions → General
                             (Workflow permissions) y Settings → Branches
                             (reglas de protección de `main`)
Detalle completo           : ver wiki/log.md, entrada 2026-09-15 16:25
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 | 0/4 | **Pendiente — sin cubrir** |
| 2016 | 0/4 | **Pendiente — sin cubrir** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 | 43 ventanas (anómalo, ver nota) | Ver nota |
| **TOTAL** | **79** | — |

> Recalculado el 2026-09-15 agrupando `sources/processed.json._gdelt_windows` por año
> de inicio de ventana (script ad-hoc, no persistido). 2017-2025 están cubiertos
> trimestralmente (4 ventanas/año); **2015-2016 nunca se cubrieron** — es el hueco
> real pendiente del backfill histórico (`wiki_historical.yml`, ejecución manual).
> **Anomalía 2026**: 43 ventanas registradas ese año (vs. ~2-4 esperadas), sugiere que
> el fetch diario incremental está generando/registrando ventanas GDELT repetidas o
> mal acotadas dentro de 2026 en lugar de extender el backfill hacia 2015-2016 — revisar
> la lógica de generación de ventanas en `wiki_agro.py` en la próxima sesión de mantenimiento.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-15 | 5 | 39 | 0 falsos positivos; diagnosticado fallo de Actions desde 2026-09-06 (9 días) |

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
