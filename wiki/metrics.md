---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (7 previos + 6 el 2026-07-09) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal real (GDELT) | 2017-03-30 → 2026-07-08 | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 46 (faltan 9 de 2015-01-01→2017-03-29) | 100% del rango 2015→hoy |
| Días sin artículos nuevos | 7 (último real: 2026-07-02) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-08 (run #43, schedule, completed/success)
Resultado               : 0 artículos nuevos (igual que 07-03, 07-04, 07-06, 07-07)
Último artículo real    : 2026-07-02 (7 días de estancamiento — supera el máx de 3)

Causa raíz confirmada (log completo del run 2026-07-06, id 28798415569):
  1. RSS (IICA, La Prensa)  → 0 entradas en ambos feeds
  2. DDG (ddgs, 8 queries)  → "No results found" en TODAS — sugiere bloqueo
                               de IP de GitHub Actions, no ausencia real de
                               resultados
  3. GDELT                 → las 9 ventanas de 2015-01-01→2017-03-29 (las
                               únicas que faltan) fallan SIEMPRE con
                               timeout/403/429/max-retries. La ventana
                               reciente (2026-06-18→2026-07-05) también fue
                               bloqueada (403/429) ese día.

Diagnóstico: no es un bug de cron ni de ingesta — GDELT y probablemente
DuckDuckGo están limitando/bloqueando las IPs de datacenter de GitHub
Actions casi todos los días. El fetch diario "funciona" (exit 0, commit
cuando hay cambios) pero queda casi siempre vacío. La corrida del
2026-07-02 (1 artículo) confirma que no es un bloqueo 100% permanente,
sino intermitente/agresivo.

Recomendaciones (sin aplicar aún — requieren pruebas contra la API real):
  a. Backoff/circuit-breaker en fetch_gdelt_historical() para no gastar
     ~5 min del budget diario reintentando las 9 ventanas 2015-2017 que
     siempre fallan.
  b. Mover el backfill 2015-2017 al workflow manual wiki_historical.yml
     (timeout 6h) en vez de repetirlo en el job diario de 30 min.
  c. Investigar el bloqueo uniforme de las 8 búsquedas DDG.

Ver wiki/log.md, entrada 2026-07-09 00:15, para el detalle completo.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015-01-01 → 2017-03-29 | 0/9 | **Bloqueado** — GDELT rechaza estas 9 ventanas todos los días (timeout/403/429), se reintentan sin avanzar |
| 2017-03-30 → 2026-06-17 | 37/37 | Completo |
| 2026-06-18 → hoy (ventana actual) | rolling | Se re-consulta cada día con fecha final creciente; a veces bloqueada (ver Estado del Fetch) |
| **TOTAL** | **46/~55** | **9 ventanas de 2015-2017 nunca se han completado — la cobertura real empieza en 2017-03-30, no en 2015** |

> Detalle y causa raíz en wiki/log.md, entrada 2026-07-09 00:15.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-09 | 0 (6/6 revisados eran falsos positivos) | 0 | 6 falsos positivos nuevos (colisión "MIDA"/USA + agro no-panameño); fix de bug en mark-all-ingested/mark-ingested; diagnóstico de fetch: GDELT/DDG bloqueando IPs de GitHub Actions, 7 días sin artículo real |

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
