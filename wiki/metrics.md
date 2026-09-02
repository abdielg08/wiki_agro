---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (total, incl. falsos positivos) | 18 | = total sin falsos positivos |
| Artículos reales ingestados a wiki | 10 | ↑ continuo |
| Falsos positivos acumulados | 8 | **0 nuevos** por sesión (documentar siempre) |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 (8 topics, 3 entities, 10 summaries, 2 overview) | ↑ continuo |
| Cobertura temporal | 2017-03 → 2026-08 (ventanas GDELT reales) | 2015-02 → hoy |
| Ventanas GDELT completadas | 77 (38 trimestres distintos, con solapes) | cubrir 2015-02→hoy sin huecos |
| Hueco de cobertura detectado | 2015-02 a 2017-03 (~2 años) sin ventanas GDELT | 0 |
| Días sin artículos nuevos (hoy) | 1 (última descarga: 2026-09-01, 1 artículo) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa  : 2026-09-01 (1 artículo nuevo)
Corrida de hoy (09-02)  : aún no registrada al momento de esta sesión
Historial reciente      : 2026-08-28 a 2026-08-31 → 4 corridas consecutivas
                           con conclusion=failure, ~3 segundos de duración
                           cada una (fallo temprano, antes de completar
                           fetch/commit — posible fallo de checkout/runner).
                           Logs no recuperables vía API (HTTP 404, expirados).
                           Se recuperó solo el 2026-09-01 sin intervención.
Volumen actual           : la mayoría de corridas traen 0-1 artículos/día,
                           muy por debajo de la meta de ~15/día. La única
                           excepción reciente fue 2026-08-24 (20 artículos).
Diagnóstico ventanas      : 77 ventanas GDELT completadas (> 45) → según
                           regla de CLAUDE.md esto indica que el rango de
                           fechas configurado está agotado y necesita
                           expansión. Cobertura real: 2017-03 a 2026-08 —
                           falta backfill de 2015-02 a 2017-03 (~2 años).
Acción recomendada        : ejecutar el workflow "Wiki Agropecuario — Crawl
                           Histórico 15 Años" (wiki_historical.yml) con
                           rango 2015-2017 — nunca se ha ejecutado (0
                           corridas registradas en Actions al 2026-09-02).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas (trimestres distintos) | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — hueco confirmado** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — hueco confirmado** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 Q1-Q3 | 2/3 (falta Q3) | En progreso |
| **TOTAL** | **38/39 trimestres desde 2017-03; 0/8 de 2015-2016** | **Backfill 2017→hoy completo; 2015-02→2017-03 NO iniciado** |

> Recalculado el 2026-09-02 a partir de `sources/processed.json["_gdelt_windows"]`
> (77 entradas registradas, 38 trimestres distintos por solapes de ventanas).
> Próximo paso: ejecutar `wiki_historical.yml` (nunca ejecutado) con rango
> 2015-2017 para cerrar el hueco de los 2 años más antiguos del período objetivo.
> El conteo de artículos por ventana no está expuesto en processed.json —
> requeriría instrumentar fetch_news.py para registrarlo por ventana.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-02 | 4 reales + 1 falso positivo | 33 | Bugfix mark_ingested(); diagnóstico Actions (4 fallas 08-28→08-31); hueco GDELT 2015-2017 detectado |

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
