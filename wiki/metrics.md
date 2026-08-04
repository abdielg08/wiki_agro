---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-04
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** (todos colisión de keyword "MIDA") |
| Pendientes de ingesta | 11 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 61 | 45 (2015→hoy) — meta superada, ver hueco abajo |
| Días sin artículos nuevos (fetch) | 2 (última corrida 2026-08-02) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit  : 2026-08-02 (0 artículos nuevos)
Corridas recientes         : 07-28(0) 07-29(2) 07-30(3) 07-31(0) 08-02(0)
                              Sin commit el 08-01 y el 08-03 → posible falla o
                              cron aún no dispara para 08-04 (job corre ~12:00 UTC).
                              Aún NO llega a 3 días consecutivos sin artículos —
                              vigilar próxima sesión; si el 08-05 sigue sin commit,
                              escalar a diagnóstico de Actions (revisar logs del
                              workflow en GitHub).
Ventanas GDELT              : 61 completadas, cubren 2017-03-30 → 2026-08-01.
                              HUECO DE COBERTURA: 2015-02-19 → 2017-03-30 aún sin
                              ventanas generadas — el backfill no ha llegado al
                              inicio del rango objetivo (ver tabla de progreso).
Falsos positivos "MIDA"     : 12 acumulados (7 previos + 5 en sesión 2026-08-04).
                              Causa: GDELT/RSS indexan cualquier artículo con la
                              sigla "MIDA" sin filtrar por relevancia a Panamá —
                              colisiona con MIDA de Malasia (Ministry of Investment,
                              Trade and Industry) y MIDA de Utah, EE.UU. (Military
                              Installation Development Authority). Recomendación:
                              agregar filtro de país/contexto (p.ej. exigir mención
                              de "Panama"/"Panamá" o dominio .pa) en el fetcher antes
                              de guardar el artículo en sources/articles/.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — hueco de cobertura, no iniciado** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — hueco de cobertura, no iniciado** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (ventanas irregulares, mayormente diarias jun-ago) | 25 | En progreso, cobertura hasta 2026-08-01 |
| **TOTAL** | **61 ventanas completadas** | **Cobertura real: 2017-03-30 → 2026-08-01. Falta 2015-02-19 → 2017-03-30.** |

> El backfill avanzó bien 2017→hoy pero AÚN NO cubre el rango objetivo completo
> (2015-02-19 → hoy). Próxima prioridad: generar ventanas GDELT para 2015-2016.
> Fuente de estos datos: `sources/processed.json` → clave `_gdelt_windows`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-04 | 0 reales (5 marcados como falsos positivos "MIDA") | 11 | Colisión de keyword "MIDA" (Malasia/Utah); se detectó y corrigió bug en `mark-all-ingested` (marcaba artículos distintos a los revisados) — ver log.md |

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
