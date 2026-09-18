---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 (incluye falsos positivos sin ingestar, ver diagnóstico) | 0 |
| Falsos positivos acumulados (detectados, no ingestados) | 7 previos + 14 nuevos detectados hoy (ver log 2026-09-18) | **0 ingestados** |
| Páginas en wiki/ | 29 (12 topics, 3 entidades, 11 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45 (2015→hoy) — ✅ superado |
| Días sin artículos nuevos en sources/ | **12** (última descarga real: 2026-09-06) | máx 3 antes de diagnosticar — 🔴 excedido |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa      : 2026-09-06 (run #103) — 0 artículos nuevos, job de ~6 min
Última corrida programada   : 2026-09-17 (run #114) — FALLIDA, job de solo 3 segundos
Corridas fallidas seguidas  : 11 (runs #104 a #114, 2026-09-07 → 2026-09-17)
Causa identificada          : falla temprana en el job (checkout/setup-python), NO en el
                               fetch en sí — el step de fetch tiene continue-on-error:true,
                               así que un fallo del fetch no puede tumbar el job entero.
                               Duración de ~3-6s es incompatible con llegar siquiera al
                               paso de "pip install".
Logs                        : no disponibles vía API (HTTP 404) para ninguna corrida
                               fallida — se requiere revisión manual en la UI de GitHub:
                               https://github.com/abdielg08/wiki_agro/actions/runs/35239772952
Hipótesis                   : expiración/permiso de GITHUB_TOKEN, cambio de política de
                               Actions en el repo/organización, o billing/quota de Actions.
Estado                      : SIN RESOLVER — requiere acceso humano al panel de Settings
                               → Actions del repositorio. Usuario notificado 2026-09-18.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **79 ventanas completadas** | **57 descargados** | Backfill activo — 79 > 45 (umbral CLAUDE.md ya superado) |

> `sources/processed.json → _gdelt_windows` reporta 79 ventanas completadas, pero el
> desglose por período/trimestre no está expuesto en el JSON en su formato actual
> (es una lista plana, no un dict por año). No se puede reconstruir la tabla por año
> sin acceso a los metadatos originales de cada ventana. Dado que 79 ≥ 45, y el fetch
> diario está roto (ver "Estado del Fetch"), la prioridad inmediata es reparar el
> fetch automático antes de seguir expandiendo el backfill histórico.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-18 | 5 | 39 | Ingesta manual del backlog (57 descargados, fetch diario roto desde 2026-09-07); se detectaron 14 falsos positivos adicionales en la cola, no ingestados |

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
