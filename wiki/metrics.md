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
| Artículos descargados (sources/) | 51 | ↑ continuo |
| Artículos marcados como ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 33 | 0 |
| Falsos positivos acumulados (documentados en log.md) | 8 (+1 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial: semilla + artículos reales) | 2015-02-19 → hoy real |
| Ventanas GDELT completadas | 79 / ~45-46 estimadas | rango agotado, requiere expansión |
| Días sin artículos nuevos en sources/ (commits) | 2 (sin commit 09-05, 09-06 al momento de esta sesión) | máx 3 antes de diagnosticar |
| Racha de corridas con 0 artículos nuevos | 3 consecutivas (09-01, 09-03, 09-04) | **señal de alarma activada** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit en sources/ : 2026-09-04 (0 artículos nuevos)
Sin commits en sources/               : 2026-09-05, 2026-09-06 (hasta esta sesión)
Racha de 0 nuevos antes del corte     : 2026-09-01, 2026-09-03, 2026-09-04 (3 corridas)
Ventanas GDELT completadas            : 79 (muy por encima de las ~45-46 estimadas
                                         para cubrir 2015-02-19 → hoy)
Diagnóstico                           : rango de fechas GDELT probablemente agotado
                                         (regla CLAUDE.md: 45+ ventanas → expandir rango).
                                         Tamaños de ventana inconsistentes observados
                                         (~3 meses y ~1.5 meses) sugieren posible
                                         regeneración/duplicación de rangos en el script
                                         de fetch, no solo agotamiento simple.
Acción pendiente                      : (1) revisar por qué GitHub Actions no corrió/
                                         no generó commit en 09-05 y 09-06;
                                         (2) revisar y depurar generación de ventanas
                                         GDELT en scripts/ (posible expansión hacia
                                         atrás o corrección de duplicados).
Estado                                 : Pendiente de intervención — documentado aquí y
                                         en wiki/log.md (2026-09-06) para seguimiento.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | Pendiente |
| 2016 Q1-Q4 | 0/4 | ? | Pendiente |
| 2017 Q1-Q4 | 0/4 | ? | Pendiente |
| 2018 Q1-Q4 | 0/4 | ? | Pendiente |
| 2019 Q1-Q4 | 0/4 | ? | Pendiente |
| 2020 Q1-Q4 | 0/4 | ? | Pendiente |
| 2021 Q1-Q4 | 0/4 | ? | Pendiente |
| 2022 Q1-Q4 | 0/4 | ? | Pendiente |
| 2023 Q1-Q4 | 0/4 | ? | Pendiente |
| 2024 Q1-Q4 | 0/4 | ? | Pendiente |
| 2025 Q1-Q4 | 0/4 | ? | Pendiente |
| 2026 Q1-Q2 | 0/2 | ? | Pendiente |
| **TOTAL** | **0/46** | **0** | **Backfill no iniciado** |

> Una vez que Actions corra con el código corregido, actualizar esta tabla con los datos reales.
> El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-06 | 4 (+1 falso positivo detectado y no ingestado) | 33 | Routine: arroz/MIDA (x3) + inundaciones Veraguas (arroz/maíz/ganadería); creada topics/ganaderia_bovina.md; falso positivo por colisión de acrónimo "MIDA" con Malasia; diagnóstico de fetch documentado |

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
