---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-27
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 50 | ↑ continuo |
| Artículos ingestados (processed.json) | 18 | = total sin falsos positivos |
| Artículos reales en wiki (con página propia) | 10 | ↑ continuo |
| Pendientes de ingesta | 32 | 0 |
| Falsos positivos acumulados | 8 | **0 nuevos por sesión** |
| Páginas en wiki/ | 27 (11 topics, 3 entities, 10 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + fetch) | 2015 → hoy real |
| Ventanas GDELT completadas | 75 / ~45 estimadas | 45 (2015→hoy) — **estimado superado, ver diagnóstico** |
| Días sin artículos nuevos | **3** (última descarga real: 2026-08-24) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVADA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit a sources/ : 2026-08-25 (0 artículos nuevos)
Última corrida con artículos nuevos  : 2026-08-24 (20 artículos)
Hoy                                  : 2026-08-27 → 3 días sin artículos nuevos ⚠

Diagnóstico (2026-08-27, routine automatizada):
  1. ¿Actions corrió? No hay commit de sources/ el 2026-08-26 (falta un día en el
     historial de commits diarios) — indicio de que la corrida de ese día no
     produjo commit (falló o no se ejecutó). El 2026-08-25 sí corrió pero con
     0 artículos nuevos.
  2. Ventanas GDELT completadas: 75 (según sources/processed.json._gdelt_windows),
     muy por encima de la estimación original de ~45 ventanas para cubrir
     2015→hoy. Esto indica que el rango de fechas ya fue recorrido varias veces
     (posible reprocesamiento de las mismas ventanas) y el backfill histórico
     real necesita que se audite/expanda la lógica de generación de ventanas
     en el workflow de fetch — no está claro que las 75 ventanas cubran
     efectivamente todo 2015→hoy sin duplicados.
  3. Fuentes RSS (IICA, La Prensa): sin visibilidad directa desde esta sesión
     (no hay log de Actions accesible aquí); recomendado revisar el log de la
     última corrida en GitHub Actions directamente.

Acción recomendada para la próxima sesión / mantenedor humano:
  - Verificar en GitHub Actions si el workflow corrió el 2026-08-26 y por qué
    no generó commit.
  - Auditar la lista de _gdelt_windows en processed.json para detectar
    duplicados o solapamientos que expliquen 75 vs ~45 estimadas.
  - Confirmar que las fuentes RSS (IICA, La Prensa) siguen respondiendo.
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
| 2026-08-27 | 4 (1 falso positivo excluido) | 32 | Routine automatizada; fix de bug en `mark_ingested` (crasheaba con `_gdelt_windows`); alarma: 3 días sin artículos nuevos |

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
