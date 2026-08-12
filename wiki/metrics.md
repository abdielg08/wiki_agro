---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-12
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (7 previos + 5 hoy) | **0 nuevos** |
| Pendientes de ingesta | 11 (inspeccionadas manualmente hoy: las 11 son falsos positivos) | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 65 / ~45 estimadas | 45 (2015→hoy) — meta superada, ver nota |
| Días sin artículos nuevos | 12 (último real: 2026-08-07; hoy 2026-08-12 sigue en 0) | máx 3 antes de diagnosticar → **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-12 (corrió correctamente, commit 0405017)
Resultado              : 0 artículos nuevos (5ta corrida consecutiva en 0: 08-02, 08-04, 08-07, 08-10, 08-12)
Ventanas GDELT          : 65 completadas — supera el estimado de 45. El backfill temporal
                          2015→hoy ya no está limitado por rango de fechas.
Causa raíz identificada: el fetch SÍ trae artículos (16 se acumularon en las últimas semanas)
                         pero el matching es por acrónimo suelto ("MIDA" y similares) SIN exigir
                         contexto Panamá. Resultado: 16/16 de los pendientes de esta sesión son
                         falsos positivos (Malasia, Utah, España, Brasil, Arabia Saudita, papers
                         IEEE, UNESCO, archive.org — detalle completo en wiki/log.md 2026-08-12).
Estado                  : pipeline trae "ruido" pero ningún artículo real de agro panameño
                         desde 2026-07-30.
Acción recomendada      : revisar la query de búsqueda en scripts/ (GDELT y/o ddgs) y exigir
                         relevancia geográfica Panamá (dominio .pa, o "Panamá"/"panameñ*" en el
                         texto) antes de guardar candidatos en sources/articles/. Sin este fix,
                         cada sesión de routine seguirá gastando su cupo de ingesta descartando
                         el mismo tipo de ruido.
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
| 2026-08-12 | 0 (5/5 falsos positivos, no ingestados) | 11 (todos falsos positivos confirmados) | Colisión de acrónimo "MIDA" (Malasia/Utah/etc.) — pipeline de fetch necesita filtro de relevancia geográfica Panamá |

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
