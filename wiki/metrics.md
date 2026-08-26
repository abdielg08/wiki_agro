---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-26
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados (sources/) | 50 | ↑ continuo |
| Artículos ingestados | 17 | = total sin falsos positivos |
| Pendientes de ingesta | 33 | 0 |
| Falsos positivos acumulados | 8 (+1 hoy: MITI/Malasia vía paultan.org) | **0 nuevos idealmente** |
| Páginas en wiki/ | 27 (11 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (mezcla semilla + backfill) | 2015 → hoy real |
| Ventanas GDELT completadas | 75 / ~45-46 estimadas | rango agotado — necesita expansión |
| Días sin artículos nuevos | 1 (última corrida con 0 nuevos: 2026-08-25; última con nuevos: 2026-08-24, +20) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-25 (corre casi a diario; ver git log de sources/)
Resultado              : 0 artículos nuevos el 08-25; 20 nuevos el 08-24; mayoría de
                         días recientes (08-04 a 08-22) con 0 nuevos, salvo 08-19 (+1)
Causa identificada     : _gdelt_windows en sources/processed.json ya tiene 75 ventanas
                         completadas — muy por encima del umbral de 45 definido en
                         CLAUDE.md. El rango de fechas cubierto por GDELT está agotado
                         y necesita expandirse (nuevas ventanas 2026 en adelante, o
                         re-chequeo de ventanas ya "completadas" que puedan tener
                         artículos adicionales).
                         Fuentes RSS (IICA, La Prensa) siguen activas y aportan la
                         mayoría de artículos nuevos cuando GDELT no rinde.
Acción recomendada     : revisar scripts de fetch GDELT para expandir/generar nuevas
                         ventanas más allá de las 75 ya marcadas, y confirmar que no
                         se estén re-marcando ventanas ya agotadas sin fruto.
Estado                 : Pendientes = 33 (no en 0), por lo que aún no aplica la
                         señal de alarma de "3 días sin artículos nuevos" en wiki/;
                         el cuello de botella real está en fetch, no en ingesta.
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
| 2026-08-26 | 4 | 33 | Ingesta rutina programada. 1 falso positivo detectado y excluido (MITI/Malasia, paultan.org, colisión de sigla "MIDA"). Fix de bug en `mark_ingested()` (usaba `processed.items()` en vez de `article_entries()`, fallaba con clave interna `_gdelt_windows`). Diagnóstico: GDELT con 75 ventanas completadas (rango agotado, necesita expansión). |

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
