---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-01
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 18 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 42 / 46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 1 (sin commit el 2026-06-30) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit : 2026-06-29 14:50 UTC (1 artículo nuevo)
Corrida esperada 06-30    : sin commit registrado — el cron corre a las 11:00 UTC
                             (06:00 Panamá); desde este entorno no se puede
                             diferenciar "no corrió" de "corrió sin cambios"
Corrida de hoy (07-01)    : aún no ocurre (programada 11:00 UTC, hora actual 00:03 UTC)
Causa raíz reincidente    : colisión de sigla "MIDA" (Utah Military Installation
                             Development Authority) sigue generando falsos positivos
                             vía GDELT/RSS — 5 nuevos el 2026-07-01, mismo patrón que
                             la auditoría del 2026-06-22 (7 falsos positivos previos)
Backfill GDELT            : 42/46 ventanas completas. Cobertura real: 2017 Q1 → 2026 Q2.
                             GAP: 2015 (Q1-Q4) y 2016 (Q1-Q4) — 8 ventanas nunca
                             ejecutadas. El objetivo "2015-02-19 → hoy" del CLAUDE.md
                             AÚN NO se cumple; falta correr wiki_historical.yml
                             (workflow_dispatch, mode=gdelt, years=2015-2016)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — GAP sin cubrir** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — GAP sin cubrir** |
| 2017 Q1-Q4 | 4/4 | ? | Completo |
| 2018 Q1-Q4 | 4/4 | 1 (gusano cogollero) | Completo |
| 2019 Q1-Q4 | 4/4 | ? | Completo |
| 2020 Q1-Q4 | 4/4 | ? | Completo |
| 2021 Q1-Q4 | 4/4 | 1 (BDA crédito) | Completo |
| 2022 Q1-Q4 | 4/4 | 1 (IICA Fusarium) | Completo |
| 2023 Q1-Q4 | 4/4 | 1 (MIDA arroz) | Completo |
| 2024 Q1-Q4 | 4/4 | 1 (MIDA política) | Completo |
| 2025 Q1-Q4 | 4/4 | 3 (falsos positivos MIDA-Malasia) | Completo |
| 2026 Q1-Q2 | 6/6 | 9 (4 reales + 5 falsos positivos MIDA-Utah/otros) | Completo |
| **TOTAL** | **42/46** | **18 descargados / 6 reales al wiki** | **Faltan 2015-2016 (8 ventanas)** |

> Fuente: `sources/processed.json` → `_gdelt_windows` (42 entradas, mapeadas por trimestre).
> Próximo paso recomendado: correr `wiki_historical.yml` con `years=2015-2016` para cerrar el gap
> y cumplir el objetivo de cobertura "2015-02-19 → hoy" del CLAUDE.md.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-01 | 0 (5 falsos positivos detectados y descartados) | 0 | Colisión "MIDA" Utah/Panamá persiste; GAP 2015-2016 identificado en backfill |

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
