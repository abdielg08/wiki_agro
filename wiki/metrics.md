---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-06-26
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 13 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2017-2026 (real GDELT) | 2015 → hoy |
| Ventanas GDELT completadas | 36 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 1 (hoy 0 artículos) | máx 3 antes de diagnosticar |
| Yield GDELT (calidad) | 6/13 = 46% | >80% |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-26
Resultado              : 0 artículos nuevos (commit 4c2d15b)
Ventanas completadas   : 36 (incluyendo 20260618_20260624, cobertura hasta ayer)
Causa baja calidad     : GDELT retorna artículos de MIDA Malasia, IEEE robotics, World Bank
                         genérico — el término "MIDA" matchea la agencia malaya no la panameña
Problema de cobertura  : ventanas desde 20170330; faltan 2015 y 2016
Fix recomendado        : refinar query GDELT con "Panamá" AND (maíz OR arroz OR ganadería
                         OR agropecuario) para filtrar resultados no panameños
Estado                 : Actions funcional pero yield bajo (54% falsos positivos)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | Pendiente (no hay ventanas desde 2015) |
| 2016 Q1-Q4 | 0/4 | 0 | Pendiente (no hay ventanas desde 2016) |
| 2017 Q2-Q4 | 1/3 | ? | Parcial (20170330_20170628 completada) |
| 2018 Q1-Q4 | 4/4 | ? | Completado |
| 2019 Q1-Q4 | 4/4 | ? | Completado |
| 2020 Q1-Q4 | 4/4 | ? | Completado |
| 2021 Q1-Q4 | 4/4 | ? | Completado |
| 2022 Q1-Q4 | 4/4 | ? | Completado |
| 2023 Q1-Q4 | 4/4 | ? | Completado |
| 2024 Q1-Q4 | 4/4 | ? | Completado |
| 2025 Q1-Q4 | 4/4 | ? | Completado |
| 2026 Q1-Q2+ | 4/2 | ? | Completado (hasta 20260624) |
| **TOTAL** | **36/46** | **13 descargados / 6 reales** | **En progreso** |

> GDELT ha procesado 36 ventanas (2017-2026). Faltan ventanas de 2015-2016 y posiblemente
> algunos trimestres de 2017. El rendimiento real es bajo (54% falsos positivos) por
> ambigüedad del término "MIDA".

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-06-26 | 0 | 0 | Diagnóstico: 36 ventanas GDELT completadas, yield 46%, 0 artículos nuevos hoy |

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
