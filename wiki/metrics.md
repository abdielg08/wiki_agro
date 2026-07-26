---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-26
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (7 previos + 5 nuevos hoy) | **0 nuevos** |
| Pendientes de ingesta | 6 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal (contenido real) | 2015-2024 (semilla, 6 artículos) | 2015 → hoy real |
| Ventanas GDELT completadas | 56 (36 trimestrales 2017-03-30→2026-06-17 + 20 diarias 2026-06-18→2026-07-25) | 2015-02-19 → hoy |
| Gap de backfill sin cubrir | 2015-01-01 → 2017-03-29 (0 ventanas completadas, fallan en cada corrida) | 0 |
| Días sin artículos nuevos | 6 (última descarga real: 2026-07-20) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-26 (corre diario, commits "0 artículos nuevos" 07-23..07-26)
Resultado               : 0 artículos nuevos desde 2026-07-20
Causa identificada (1)  : 5/5 artículos pendientes de esta sesión eran falsos positivos por
                          colisión de la sigla "MIDA" (Malaysian Investment Development
                          Authority / Utah Military Installation Development Authority) —
                          ver wiki/log.md 2026-07-26 para detalle
Causa identificada (2)  : el backfill histórico 2015-01-01→2017-03-29 nunca se completa —
                          ninguna ventana de ese rango aparece en _gdelt_windows pese a
                          reintentarse en cada corrida diaria desde el reset 2026-06-22.
                          wiki_historical.yml (el workflow diseñado para el crawl 2015-2025)
                          nunca se ha disparado manualmente (sin commits "crawl histórico").
Estado                  : Pendiente — requiere (a) disparar wiki_historical.yml manualmente
                          con years=2015-2017 mode=gdelt para ver el error real, y (b) acotar
                          el filtro de "MIDA" por país/idioma real del artículo.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — 0 ventanas completadas, fallan en cada corrida** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — 0 ventanas completadas, fallan en cada corrida** |
| 2017 Q1 | 0/1 | **Pendiente — 0 ventanas completadas, fallan en cada corrida** |
| 2017 Q2-Q4 | 3/3 | Completo (desde 2017-03-30) |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 Q1-Q2 (hasta 2026-06-17) | 1/1 | Completo |
| 2026-06-18 → 2026-07-25 | 20/20 días | Al día (barrido diario incremental) |
| **TOTAL** | **56 ventanas** | **Gap real: 2015-01-01 → 2017-03-29 (~9 trimestres) nunca completado** |

> Diagnóstico completo en wiki/log.md (2026-07-26). El backfill NO está agotado ni
> completo: cubre continuamente 2017-03-30 → hoy, pero el tramo 2015–2017-Q1 (el inicio
> real del objetivo de cobertura, 2015-02-19) nunca logra completarse — cada corrida
> diaria lo reintenta desde cero y sigue fallando antes de llegar a las ventanas nuevas.
> Investigar disparando `wiki_historical.yml` manualmente (nunca se ha ejecutado).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-26 | 0 (5/5 falsos positivos por colisión "MIDA") | 6 | Diagnóstico: gap de backfill 2015→2017-Q1 nunca completado; wiki_historical.yml nunca disparado |

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
