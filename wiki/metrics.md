---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-25
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 50 | ↑ continuo |
| Artículos ingestados (total) | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 32 | 0 |
| Falsos positivos acumulados | 8 (7 previos + 1 el 2026-08-25) | **0 nuevos** |
| Páginas en wiki/ | 25 (9 topics, 3 entidades, 10 resúmenes, ~3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 | 2015 → hoy real |
| Ventanas GDELT completadas | 75 (≥ 45 estimadas → rango agotado) | 45 (2015→hoy) |
| Días sin artículos nuevos | 1 (última corrida con artículos: 2026-08-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-25 (0 artículos nuevos) — corrida previa 2026-08-24 (20 artículos nuevos)
Resultado               : GitHub Actions SÍ está corriendo diariamente (commits "chore(sources): N
                          artículos nuevos descargados [skip ci]" en sources/ el 20, 21, 22, 24 y 25 de agosto)
Causa 0-artículos hoy   : Ventanas GDELT completadas = 75, por encima de las ~45 estimadas para cobertura
                          2015→hoy → el rango de fechas disponible en GDELT está mayormente agotado; los días
                          sin artículos nuevos ya son esperables y no indican una falla del fetch.
Diagnóstico             : 1) Actions corrió hoy → OK. 2) 75 ventanas ≥ 45 → rango de fechas agotado (no bloqueo/timeout).
                          3) RSS IICA/La Prensa: sin evidencia de fallo puntual hoy; volumen de prensa.com (44 artículos)
                          sugiere que RSS de La Prensa sigue activo.
Recomendación           : considerar expandir ventanas GDELT (queries alternativas o fuentes RSS adicionales) si el
                          volumen de artículos nuevos se mantiene en 0 por 3+ días consecutivos.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Datos reales calculados desde `sources/processed.json` → `_gdelt_windows` (2026-08-25).

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | 0/4 | **Pendiente — sin iniciar** |
| 2016 | 0/4 | **Pendiente — sin iniciar** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 | 39 ventanas registradas | ⚠️ Anómalo — muchas más de las ~2-3 trimestres esperados |
| **TOTAL** | **75** | Ver hallazgo abajo |

### ⚠️ Hallazgo — backfill 2015-2016 sin iniciar + churn anómalo en 2026
- **2015 y 2016 tienen 0 ventanas GDELT completadas**, pese a ser la prioridad #1 de cobertura según
  `CLAUDE.md` (objetivo: 2015-02-19 → hoy). El fetch histórico parece estar re-consultando 2017-2026
  repetidamente sin retroceder a los años más antiguos.
- **2026 acumula 39 ventanas** (vs. ~2-3 trimestres esperables para un año en curso), lo que sugiere que
  `fetch_gdelt_historical()` está generando/reintentando ventanas del año actual en lugar de avanzar hacia
  2015-2016. Posible bug en la lógica de selección de la siguiente ventana pendiente.
- **Acción recomendada para próxima sesión de mantenimiento**: revisar `scripts/fetch*.py` (lógica de
  selección de ventana GDELT) para confirmar por qué no avanza hacia 2015-2016 y corregir el orden de
  backfill (probablemente debe priorizar ventanas cronológicamente ascendentes desde 2015-02-19 en vez de
  repetir el rango reciente).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-25 | 4 (+1 falso positivo excluido) | 32 | Routine automática; creada topics/subsidios_programas.md; fix bug mark-ingested() |

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
