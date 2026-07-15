---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados (con contenido en wiki) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 (8 topics, 3 entidades, 6 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2017-03-30 → 2026-07-14 (real, vía GDELT) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 49 (2017-03-30 → 2026-07-14) | ~46-50 (2015→hoy) |
| Ventanas GDELT faltantes | 9 (2015-01-01 → 2017-03-29) — nunca completadas | 0 |
| Días sin artículos nuevos | 0 (Actions corrió hoy) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-15 12:17 UTC (commit 5f4d667, 1 artículo nuevo)
Resultado               : Fetch diario (RSS + búsqueda DDG) funcionando con normalidad
Bug encontrado hoy      : fetch_ddg_search() no filtraba por dominio real ni exigía
                          mención de Panamá (a diferencia del path RSS) — causó 9 de
                          los 16 falsos positivos acumulados. Corregido en
                          scripts/fetch_news.py (ver wiki/log.md 2026-07-15 16:20).
Segundo bug encontrado  : mark_ingested() (scripts/ingest.py) crasheaba con
                          AttributeError en TODA invocación por no filtrar la clave
                          interna _gdelt_windows (list) al iterar processed.json.
                          Corregido — comando mark-ingested vuelve a funcionar.
GDELT backfill          : el modo "daily" de Actions NO incluye GDELT (solo
                          RSS+DDG) — el backfill histórico solo avanza con
                          `fetch --mode gdelt` disparado manualmente desde un
                          entorno con red completa. Intento en sesión sandbox de
                          hoy bloqueado por proxy del entorno (403 en CONNECT a
                          api.gdeltproject.org, ver wiki/log.md) — no es evidencia
                          de falla real de GDELT.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Nunca completadas** — pendiente reintento desde entorno con acceso real a GDELT |
| 2016 Q1-Q4 | 0/4 | **Nunca completadas** — pendiente reintento desde entorno con acceso real a GDELT |
| 2017 (mar-dic) | 3/3 | Completo (año no inicia hasta 2017-03-30) |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (ene-jun) | 2/2 | Completo (trimestral) + 11 ventanas diarias de catch-up hasta 2026-07-14 |
| **TOTAL** | **49/58 estimadas** | **Faltan las 9 ventanas de 2015-01 a 2017-03** |

> Próximo paso: desde una sesión/workflow con salida de red completa a
> api.gdeltproject.org (no este entorno sandbox), correr
> `python wiki_agro.py fetch --mode gdelt --limit 200` repetidamente hasta
> que las 9 ventanas de 2015-2016 completen o devuelvan 0 resultados reales
> (HTTP 200 con lista vacía) — eso sí confirmaría falta de cobertura real de
> GDELT para ese período, cosa que el intento de hoy NO pudo confirmar.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Falsos positivos | Pendientes restantes | Nota |
|-------|---------------------|-------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 (acumulado) | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-15 | 0 | 9 (16 acumulado) | 0 | 9 falsos positivos por colisión "MIDA" (Malasia/Utah) y agro genérico sin mención de Panamá. 2 bugs de código corregidos: filtro de dominio/Panamá faltante en `fetch_ddg_search()`, y crash en `mark_ingested()` por clave interna `_gdelt_windows`. GDELT backfill: 49/58 ventanas — bloqueado en 2015-2016 por proxy del sandbox, requiere reintento desde entorno con red completa. |

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
