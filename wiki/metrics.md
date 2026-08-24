---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 50 | ↑ continuo |
| Artículos reales ingestados | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Páginas en wiki/ | 25 | ↑ continuo |
| Cobertura temporal | 2017–2026 (backfill trimestral) | 2015 → hoy real |
| Ventanas GDELT trimestrales completadas | 37 / ~46 estimadas | 46 (2015→hoy) |
| Ventanas GDELT recientes (rolling, jun–ago 2026) | 37 | cobertura de últimos meses |
| Días sin artículos nuevos | 0 (última corrida: 2026-08-24, 20 artículos) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-24 (commit a8ccd35, "20 artículos nuevos descargados")
Resultado               : OK — 20 artículos nuevos en esta corrida
Fix de 2026-06-22       : sigue funcionando correctamente (ventanas futuras limitadas)
Estado                  : Fetch automático operando con normalidad
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente** — límite real de GDELT API v2 (2015-02-19) |
| 2016 Q1-Q4 | 0/4 | **Pendiente** |
| 2017 Q1-Q4 | 3/4 | En curso (falta Q1) |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 Q1-Q3 | 1/3 | En curso (Q2-Q3 cubiertos por ventanas rolling recientes, ver abajo) |
| **TOTAL (trimestral)** | **37/~46** | **Falta solo 2015-2016 + Q1 2017** |

> Además de las 37 ventanas trimestrales históricas, hay **37 ventanas "rolling"** con inicio fijo en 2026-06-18
> y fin variable (una por cada corrida diaria de Actions desde esa fecha) que cubren jun-ago 2026 día a día.
> Próximo paso del backfill: extender las ventanas trimestrales hacia atrás para cubrir 2015-2016 y cerrar Q1 2017.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-24 | 4 (+1 falso positivo documentado) | 32 | Fix bug `mark-ingested` (crash con `_gdelt_windows`); backfill trimestral en 37/46 |

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
