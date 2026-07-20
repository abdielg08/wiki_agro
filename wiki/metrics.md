---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 (7 previos + 9 el 2026-07-20) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 51 | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos | 5 (último fetch: 2026-07-15) | máx 3 antes de diagnosticar — **⚠ ALARMA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions      : sin confirmar desde este entorno (último artículo
                               guardado en sources/ es del 2026-07-15; hoy 2026-07-20)
Resultado                   : 5 días consecutivos sin artículos nuevos → ALARMA (máx 3)
Ventanas GDELT completadas  : 51 (≥ 45 estimadas para 2015→hoy)
Causa identificada          : rango de fechas GDELT probablemente agotado — necesita
                               expansión (nuevas ventanas 2015→hoy) en vez de más reintentos
                               del mismo rango
Calidad del fetch reciente  : las últimas ~10 descargas (guardadas 2026-06-19 a 2026-07-15)
                               son 100% falsos positivos: ruido internacional por
                               coincidencia de palabra clave "MIDA" (Malasia, Utah EE.UU.)
                               y artículos genéricos de agricultura sin relación con Panamá
                               (Irán, Arabia Saudita, Nueva York, paper IEEE 6G/IoT)
Recomendación                : (1) expandir/rotar las ventanas GDELT agotadas,
                               (2) endurecer el filtro de keyword para excluir dominios
                               .com de EE.UU. no panameños y exigir co-ocurrencia con
                               "Panamá"/"panameño", (3) verificar si el workflow de
                               GitHub Actions sigue corriendo (no confirmable desde esta sesión)
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
| 2026-07-20 | 0 | 0 | 9 pendientes revisados = 9 falsos positivos (MIDA-Malasia/Utah, agro genérico no panameño). Fix de bug en `mark_ingested()` (scripts/ingest.py). 5 días sin artículos nuevos — ver diagnóstico arriba |

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
