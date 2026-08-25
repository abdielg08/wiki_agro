---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-25
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 50 | ↑ continuo |
| Artículos ingestados/marcados | 18 | = total sin falsos positivos ingestados |
| Pendientes de ingesta | 32 | 0 |
| Falsos positivos acumulados | 8 (7 previos + 1 nuevo: colisión MIDA-Malasia) | **0 nuevos** por sesión, se documentan siempre |
| Páginas en wiki/ | 24 (8 topics, 3 entities, 10 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2017-03 → 2026-08 (ventanas GDELT); faltan 2015-02 → 2017-03 | 2015-02-19 → hoy real |
| Ventanas GDELT completadas | 74 (38 fechas de inicio únicas) / ~46 estimadas | 46 (2015→hoy) — cobertura ya excede la meta en cantidad, pero faltan ventanas 2015-2016 |
| Días sin artículos nuevos | 0 (último fetch: 2026-08-24, +20 artículos) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-24 (commit a8ccd35)
Resultado               : 20 artículos nuevos descargados — fetch funcionando correctamente
Historial reciente      : 2026-08-19 (+1), 2026-08-20 (0), 2026-08-21 (0), 2026-08-22 (0), 2026-08-24 (+20)
Ventanas GDELT           : 74 completadas, cubren de 2017-03-30 a 2026-06-18 (38 fechas de inicio únicas)
Gap identificado         : faltan ventanas 2015-02-19 → 2017-03-30 (backfill histórico incompleto)
Falso positivo detectado : artículo etiquetado fuente "prensa.com" resultó ser de paultan.org
                            (medio automotriz de Malasia) — colisión de siglas MIDA(PA)/MIDA(MY).
                            Ver wiki/log.md 2026-08-25 para detalle. No requiere fix de código
                            urgente pero se recomienda validar dominio real vs. fuente etiquetada
                            en el fetcher.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — gap real de backfill** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — gap real de backfill** |
| 2017 Q1-Q4 | 4/4 | Completado |
| 2018 Q1-Q4 | 4/4 | Completado |
| 2019 Q1-Q4 | 4/4 | Completado |
| 2020 Q1-Q4 | 4/4 | Completado |
| 2021 Q1-Q4 | 4/4 | Completado |
| 2022 Q1-Q4 | 4/4 | Completado |
| 2023 Q1-Q4 | 4/4 | Completado |
| 2024 Q1-Q4 | 4/4 | Completado |
| 2025 Q1-Q4 | 4/4 | Completado |
| 2026 Q1-Q2 | 2/2 | Completado (Q3-Q4 aún no aplican — fechas futuras) |
| **TOTAL** | **38/42 trimestres calendarizados** | **2015-2016 son el único gap real; 2017→2026-Q2 cubierto** |

> Actualizado 2026-08-25 a partir de `sources/processed.json._gdelt_windows` (74 ventanas registradas,
> 38 fechas de inicio únicas). El fetch de GitHub Actions está sano (20 artículos el 2026-08-24).
> Prioridad de backfill: generar ventanas GDELT para 2015-02-19 → 2016-12-31, únicos trimestres
> sin cobertura dentro del objetivo 2015→hoy.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-25 | 4 reales + 1 falso positivo marcado | 32 | Fetch de Actions activo (20 art. el 2026-08-24); 1 falso positivo por colisión de siglas MIDA(PA)/MIDA(MY) |

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
