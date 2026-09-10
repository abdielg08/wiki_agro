---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-10
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 11 | = total sin falsos positivos |
| Falsos positivos acumulados (confirmados) | 7 | **0 nuevos** |
| Falsos positivos sospechosos aún en cola pendiente | ≥13 (sin confirmar/marcar) | 0 |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 2 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (con solapamiento en ventanas recientes) | 45 (2015→hoy) |
| Días sin artículos nuevos | **4** (última descarga real: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa (con artículos) : 2026-09-06 (run #103, 6 artículos nuevos)
Últimas 3 corridas (#104 07-sep, #105 08-sep, #106 09-sep) : conclusion=failure
Duración de las corridas fallidas      : ~3 segundos (created_at ≈ completed_at)
Causa identificada     : Falla ocurre antes de completar steps básicos (checkout/pip
                         install no alcanzan a correr en 3s) → probable límite de
                         cuota/concurrencia de Actions o problema de runner, NO un
                         error de código en fetch_news.py/fetch_historical.py.
                         Logs de los jobs fallidos no disponibles (HTTP 404, expirados).
Fix aplicado            : Ninguno — requiere revisar configuración/cuota de GitHub
                         Actions del repositorio (fuera del alcance de esta sesión).
Estado post-fix         : Pendiente — recomendado ejecutar workflow_dispatch manual
                         para confirmar si el fallo persiste.
Ventanas GDELT          : 79 completadas, pero con solapamiento en el rango reciente
                         (ventanas repetidas tipo "20260618_2026xxxx" con distinto fin) →
                         el conteo ya no refleja backfill histórico neto; revisar lógica.
Cola contaminada        : ≥13 artículos en pendientes con `source` mal etiquetado como
                         "prensa.com" pero de dominios no-Panamá (Mozambique, Utah,
                         Aragón/España, Brasil, Arabia Saudita, etc.) — bug de
                         etiquetado en fetch_news.py, ver wiki/log.md 2026-09-10 00:05.
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
| 2026-09-10 | 5 (arroz/MIDA, La Prensa) | 39 | 0 falsos positivos en el lote; diagnóstico: Actions falla 3 días consecutivos (07-09 sep) + ≥13 falsos positivos sospechosos detectados en la cola pendiente (no ingestados) |

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
