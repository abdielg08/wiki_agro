---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-13
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 (7 previos + 7 hoy) | **0 nuevos** desde el fix de hoy |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 / ~46 trimestres | 46 (2015→hoy) |
| Días sin artículos nuevos | 3 (2026-07-11, 07-12, 07-13) | máx 3 antes de diagnosticar — **alarma activa** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions      : 2026-07-12 (verde/success) — Actions SÍ corre a diario
Última descarga real nueva  : 2026-07-10 (1 artículo)
Resultado 07-11, 07-12      : 0 artículos nuevos (ambas corridas "success" pero sin cambios)
Causa identificada          : GDELT bloquea/timeout (403/429) las 8 ventanas trimestrales
                               de 2015-01-01→2016-12-28 (inicio del rango objetivo) y la
                               ventana móvil "hoy" (2026-06-18→hoy) en TODAS las corridas
                               recientes. RSS (IICA, La Prensa) = 0 entradas. DDG de sitios
                               oficiales = "No results found". Confirmado vía logs del job
                               29191567085 (2026-07-12).
Fix aplicado hoy            : Ninguno sobre GDELT (bloqueo de red externo, no bug de código).
                               Sí se corrigieron 2 bugs de código no relacionados con el
                               fetch diario: fetch_ddg_search() sin guard de Panamá (causaba
                               falsos positivos) y mark_all_ingested() marcando artículos
                               distintos a los revisados (ver wiki/log.md 2026-07-13).
Recomendación pendiente      : agregar backoff/jitter en fetch_gdelt_historical() para las
                               ventanas de 2015-2016, que llevan semanas sin poder completar.
Estado post-fix              : Falsos positivos de fetch_ddg_search deberían desaparecer en
                               la próxima corrida; bloqueo GDELT sigue activo, pendiente de
                               reintento/backoff.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Bloqueado — GDELT 403/timeout todos los días** |
| 2016 Q1-Q4 | 0/4 | 0 | **Bloqueado — GDELT 403/timeout todos los días** |
| 2017 Q1-Q4 | 4/4 | ? | Completado |
| 2018 Q1-Q4 | 4/4 | ? | Completado |
| 2019 Q1-Q4 | 4/4 | ? | Completado |
| 2020 Q1-Q4 | 4/4 | ? | Completado |
| 2021 Q1-Q4 | 4/4 | ? | Completado |
| 2022 Q1-Q4 | 4/4 | ? | Completado |
| 2023 Q1-Q4 | 4/4 | ? | Completado |
| 2024 Q1-Q4 | 4/4 | ? | Completado |
| 2025 Q1-Q4 | 4/4 | ? | Completado |
| 2026 Q1 | 1/1 | ? | Completado |
| 2026 (ventana móvil "hoy") | avanzó hasta 07-09, detenida desde 07-10 | 1 (07-10) | **Bloqueada desde 2026-07-11** |
| **TOTAL** | **37/~46 trimestres** | ? | **9 ventanas bloqueadas por GDELT (2015-2016 + ventana móvil)** |

> Las 8 ventanas trimestrales de 2015-01-01→2016-12-28 y la ventana móvil
> "hoy" fallan con 403/429/timeout de GDELT en cada corrida (ver Estado del
> Fetch arriba) — no han podido completarse nunca, no es que no se hayan
> intentado. El resto del backfill (2017→2026 Q1) sí está completo.
> Conteo de "Artículos" por trimestre pendiente de instrumentar — el script
> actual no lo registra por ventana, solo el total acumulado en `stats`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-13 | 0 (7 revisados, 7 falsos positivos) | 0 | Fix de fetch_ddg_search() (guard Panamá) + fix de mark_all_ingested() (desalineado con `ingest`) + diagnóstico: GDELT bloqueado en ventanas 2015-2016 y ventana móvil desde 07-11 |

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
