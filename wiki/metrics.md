---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-04
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos reales ingestados (con página en wiki) | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 (8 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2017-2026 real (backfill 2015-2016 bloqueado) + semilla 2015-2016 manual | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (ver desglose abajo — incluye duplicados de wavefront) | cobertura densa 2015→hoy |
| Días sin artículos nuevos | **8** (desde 2026-08-27) | máx 3 antes de diagnosticar ⚠️ ALARMA ACTIVA |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-09-04 (commits diarios confirmados, corre normalmente)
Resultado              : 0 artículos nuevos (igual que 2026-09-03 y 2026-09-01; último real: 2026-08-27)
Causa identificada     : Bug en fetch_gdelt_historical() (scripts/fetch_news.py):
                         1) Ventanas GDELT de 2015 y 2016 (8 trimestres) NUNCA completan exitosamente
                            — 0/8 en _gdelt_windows pese a ser el rango de arranque configurado.
                            La corrida diaria las reintenta desde cero cada vez sin avanzar.
                         2) La ventana más reciente (2026, trimestre en curso) genera una window_key
                            nueva cada día porque su fin = hoy-1 (siempre cambia), por lo que nunca
                            "cierra" — se re-descarga el mismo período una y otra vez (43 entradas
                            distintas solo para 2026 en _gdelt_windows).
                         RSS IICA y La Prensa: sin artículos nuevos evidentes en commits recientes.
Fix aplicado            : Ninguno en esta sesión (fuera de alcance de la rutina de contenido).
                         Requiere sesión dedicada a scripts/fetch_news.py — ver wiki/log.md 2026-09-04
                         16:30 para el diagnóstico completo con evidencia.
Estado post-fix         : Pendiente — recomendado para próxima sesión de mantenimiento de scripts/
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Datos reales extraídos de `sources/processed.json` → `_gdelt_windows` el 2026-09-04.

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 Q1-Q4 | **0/4** | ⚠️ Bloqueado — nunca completa (ver diagnóstico) |
| 2016 Q1-Q4 | **0/4** | ⚠️ Bloqueado — nunca completa (ver diagnóstico) |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (en curso) | 43 entradas (1 trimestre re-descargado repetidamente) | ⚠️ Wavefront duplicado — nunca cierra |
| **TOTAL** | **79** | 2017-2025 completo; 2015-2016 y wavefront 2026 requieren fix de código |

> El backfill de contenido (2017-2025) está técnicamente completo en cobertura de ventanas GDELT, pero
> eso no garantiza que cada ventana haya traído artículos relevantes — solo que la consulta HTTP tuvo
> éxito. 2015-2016 requieren un fix en `fetch_gdelt_historical()` antes de poder completarse.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-04 | 4 reales + 1 falso positivo detectado y rechazado | 33 | Diagnóstico: 8 días sin artículos nuevos; bug de ventanas GDELT 2015-2016 y wavefront 2026 identificado (ver Estado del Fetch) |

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
