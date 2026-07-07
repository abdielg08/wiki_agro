---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-07
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (7 previos + 6 esta sesión) | **0 nuevos** desde el fix |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / ~54 estimadas (faltan 2015-01→2017-03) | 2015 → hoy |
| Días sin commit nuevo en sources/ | 2 (07-05, 07-06 corrieron pero 0 resultados) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-07-06 (conclusion=success, pero 0 commits)
Resultado                    : 0 artículos nuevos 3 corridas seguidas (07-04 a 07-06)
Causa identificada           : api.gdeltproject.org devuelve ConnectTimeoutError / 403-429
                                para TODAS las ventanas en el run del 07-06 (ver job
                                85394933293). Afecta las 9 ventanas históricas nunca
                                completadas (2015-01 -> 2017-03) y la ventana de cola actual.
Causa raiz falsos positivos   : fetch_ddg_search() no validaba dominio real ni aplicaba
                                _is_blocked_domain()/_is_panama_related() -- 6 falsos
                                positivos (Utah "MIDA", NY Farm Bureau, Arabia Saudita)
                                marcados ingested=true sin entrar al wiki.
Fix aplicado esta sesion      : fetch_ddg_search() ahora valida dominio contra `site` y
                                aplica los mismos filtros que fetch_rss(). mark_ingested()
                                corregido (crasheaba con la clave _gdelt_windows).
Estado post-fix               : Pendiente validacion en proxima corrida Actions.
Pendiente sin resolver        : ventana de cola GDELT se recalcula y re-descarga entera
                                cada dia (fecha de fin cambia diariamente) -- ineficiente.
Nota operativa                : ~30+ PRs abiertos (claude/modest-galileo-*, claude/loving-
                                lovelace-*) ya contienen este mismo fix de forma
                                independiente, nunca fusionados a main. Se recomienda
                                consolidar y cerrar duplicados.
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
| 2026-07-07 | 0 | 0 | 6 falsos positivos rechazados (colisión "MIDA" Utah/Malasia, agro Arabia Saudita/NY) + fix causa raíz en fetch_ddg_search() + fix bug mark_ingested() |

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
