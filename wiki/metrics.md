---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados (total marcados) | 18 | = total sin falsos positivos |
| Artículos reales en wiki (no falso positivo) | 11 | ↑ continuo |
| Falsos positivos acumulados | 7 | **0 nuevos** (esta sesión: 0) |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 26 (9 topics, 3 entidades, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (artículos reales dispersos, no continuo) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | rango agotado — necesita expansión/revisión |
| Días sin artículos nuevos en sources/ | **≥2 confirmados (09-07, 09-08 fallaron), 09-09 aún sin correr al momento de esta sesión** | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA con artículos : 2026-09-06 (run #103, 6 artículos nuevos)
Últimas 2 corridas programadas        : 2026-09-07 (run #104) y 2026-09-08 (run #105) — FALLARON
Detalle del fallo      : ambos runs completaron (conclusion=failure) en ~3-4 segundos, sin
                         runner asignado (runner_id=0, runner_name vacío) — el job murió antes
                         de ejecutar cualquier step (checkout, pip install, fetch). No es un
                         bug del código de fetch_*; parece un problema de infraestructura de
                         Actions (posible límite de minutos/cuota, o el runner no pudo iniciar).
                         Logs de step no disponibles vía API (HTTP 404 al descargarlos).
Ventanas GDELT          : 79 completadas, muy por encima de las ~45 estimadas para cubrir
                         2015→hoy — el rango histórico ya está agotado con el esquema actual
                         de ventanas; probablemente se están re-visitando ventanas ya cubiertas
                         sin producir artículos nuevos netos. Necesita revisión/expansión del
                         esquema de ventanas GDELT (ver fetch-historical / _gdelt_windows).
Acción recomendada      : (1) Revisar en GitHub → Settings → Actions si hay un límite de minutos
                         alcanzado o el workflow está deshabilitado; (2) revisar manualmente
                         `gh run view <run_id> --log` o la UI de Actions para el run #104/#105
                         ya que la API de logs devolvió 404 desde esta sesión; (3) evaluar si el
                         backfill GDELT necesita nuevas ventanas fuera del rango ya cubierto.
Estado                  : DIAGNOSTICADO — requiere intervención humana en configuración de
                         GitHub Actions (fuera del alcance de esta sesión de Claude Code).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

```
Ventanas registradas en _gdelt_windows : 79 (vs. ~45 estimadas originalmente para 2015→hoy)
```

La tabla trimestral anterior (0/46, "backfill no iniciado") quedó desactualizada: `processed.json`
ya registra 79 claves de ventana bajo `_gdelt_windows`, pero no incluyen fecha de inicio/fin
parseable directamente para reconstruir cobertura por trimestre desde esta sesión sin instrumentar
`fetch-historical`. Con 57 artículos descargados en total (todas las fuentes, no solo GDELT) y
79 ventanas ya visitadas, es probable que el esquema esté re-visitando rangos ya cubiertos sin
producir artículos nuevos — consistente con el estancamiento reciente del fetch.

**Pendiente para próxima sesión**: instrumentar `scripts/fetch_historical.py` (o el módulo GDELT
correspondiente) para loguear explícitamente rango de fechas por ventana, y así reconstruir la
tabla trimestral real en lugar de la placeholder anterior.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-09 | 5 (0 falsos positivos en el lote real) | 39 | Backfill llegó a 57 artículos descargados; se diagnosticó fallo de Actions (runs #104-105, 09-07/09-08); se corrigió un bug en `mark-all-ingested` que había marcado 5 artículos incorrectos (revertido, ver log.md); se confirmó que el top-score de la cola de pendientes está dominado por falsos positivos (Malaysia MIDA/MITI, noticias de Utah) — pendiente auditoría/depuración en próxima sesión |

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
