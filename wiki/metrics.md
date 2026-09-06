---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-06
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos reales ingestados | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | rango agotado (≥45) — necesita expansión |
| Días sin artículos nuevos (fetch real) | 10 (último fetch con artículos nuevos: 2026-08-27) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit en sources/ : 2026-09-04 (0 artículos nuevos)
Último commit con artículos reales    : 2026-08-27 (1 artículo)
Sin commits en sources/               : 2026-09-05 y 2026-09-06 (hoy) — Actions no corrió
                                         o corrió y falló antes de commitear
Ventanas GDELT completadas            : 79 (>= 45) → rango de fechas agotado, necesita
                                         expansión (ampliar rango histórico o pasar a
                                         ventanas más recientes/futuras válidas)
RSS activas (IICA, La Prensa)         : sin visibilidad directa desde esta sesión;
                                         revisar logs de Actions para confirmar si
                                         devolvieron entradas en los últimos días
Diagnóstico                           : combinación de (a) agotamiento de ventanas GDELT
                                         y (b) posible falla/no-ejecución del workflow de
                                         Actions los días 2026-09-05 y 2026-09-06
Acción sugerida                       : (1) revisar historial de runs del workflow en
                                         GitHub Actions para confirmar si corrió; (2)
                                         expandir el rango de ventanas GDELT más allá de
                                         las 79 ya completadas
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Recalculado a partir de `sources/processed.json._gdelt_windows` (79 ventanas registradas):

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | 0 | **Pendiente — prioridad** (inicio real de cobertura GDELT) |
| 2016 | 0 | **Pendiente — prioridad** |
| 2017 | 4 | Completo |
| 2018 | 4 | Completo |
| 2019 | 4 | Completo |
| 2020 | 4 | Completo |
| 2021 | 4 | Completo |
| 2022 | 4 | Completo |
| 2023 | 4 | Completo |
| 2024 | 4 | Completo |
| 2025 | 4 | Completo |
| 2026 | 43 | Sobre-repetido (ver nota) |
| **TOTAL** | **79** | Ver diagnóstico |

**Diagnóstico**: 2015 y 2016 —los años que definen el arranque real del backfill (2015-02-19)—
tienen **0 ventanas completadas**, mientras que 2026 acumula 43 ventanas (muy por encima de las
~2 esperadas para Q1-Q2, o ~4 si se cuenta el año completo). Esto sugiere que el fetch está
re-procesando o expandiendo ventanas recientes/repetidas en vez de retroceder hacia 2015-2016.
Acción sugerida: revisar la lógica de selección de ventanas en el script de fetch para priorizar
años sin cobertura (2015, 2016) antes de seguir generando ventanas en 2026.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-06 | 4 reales + 1 falso positivo | 33 | Routine automática; falso positivo: artículo de Malasia (MITI/MIDA) mal etiquetado como prensa.com/PA |

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
