---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-29
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (processed.json) | 18 | = total sin falsos positivos |
| Artículos reales ingestados al wiki | 10 | 18 ingestados − 8 falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** salvo el detectado en esta sesión |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 25 (9 topics, 3 entities, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (parcial; huecos en 2015-2016) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 (ver detalle abajo) | 45+ (2015→hoy) — **meta numérica superada** |
| Última corrida Actions con artículos nuevos | 2026-08-27 (1 artículo) | — |
| Días sin artículos nuevos | 2 (28 y 29 de agosto sin commit de sources/) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit         : 2026-08-27 (1 artículo nuevo)
Corridas sin commit posteriores   : 2026-08-28, 2026-08-29 (sin registro en git log de sources/)
Cadencia configurada              : cron diario "0 11 * * *" (6:00 AM Panamá) — .github/workflows/wiki_daily.yml
Observación                       : el historial de commits de sources/ muestra huecos irregulares incluso en
                                     semanas previas (p. ej. 2026-08-18, 08-11, 08-09, 08-08, 08-06 sin commit),
                                     lo que sugiere que el workflow no corre o falla silenciosamente algunos días
                                     (el commit solo ocurre si `git diff --staged` no está vacío).
Pendiente de revisar              : logs de GitHub Actions del workflow "Wiki Agropecuario — Fetch Diario" para
                                     confirmar si las corridas faltantes fallaron o simplemente no produjeron diff.
Estado backfill GDELT              : 76 ventanas completadas registradas en processed.json (_gdelt_windows),
                                     concentradas en 2017-2025 (4 c/u) y 2026 (40 — granularidad distinta,
                                     posiblemente semanal en vez de trimestral). 2015 y 2016 sin ventanas registradas.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | 0 | **Pendiente — sin ventanas registradas** |
| 2016 | 0 | **Pendiente — sin ventanas registradas** |
| 2017 | 4 | Completo (trimestral) |
| 2018 | 4 | Completo (trimestral) |
| 2019 | 4 | Completo (trimestral) |
| 2020 | 4 | Completo (trimestral) |
| 2021 | 4 | Completo (trimestral) |
| 2022 | 4 | Completo (trimestral) |
| 2023 | 4 | Completo (trimestral) |
| 2024 | 4 | Completo (trimestral) |
| 2025 | 4 | Completo (trimestral) |
| 2026 | 40 | Ventanas de granularidad distinta (revisar) |
| **TOTAL** | **76** | **2015-2016 son el hueco real pendiente de backfill** |

> Conteo derivado de `sources/processed.json → _gdelt_windows` (2026-08-29). El bajo número de artículos
> ingestados (18) frente a 76 ventanas completadas sugiere que GDELT devuelve pocos resultados relevantes
> por ventana para Panamá agro, o que hay falsos positivos filtrados aguas abajo (ver sección de falsos positivos).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-29 | 4 reales (5 procesados, 1 falso positivo) | 33 | Reinstalación de dependencias Python; 1 falso positivo detectado (artículo sobre MITI/Malasia mal etiquetado como Panamá) |

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
