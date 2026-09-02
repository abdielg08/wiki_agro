---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (total) | 18 | = total sin falsos positivos |
| Artículos reales ingestados en wiki | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2017-2026 (real) | 2015 → hoy real |
| Ventanas GDELT completadas | 77 (ver desglose abajo — no todas son progreso real) | 45 (2015→hoy) |
| Días sin artículos nuevos | 6 (última vez: 2026-08-27, 1 artículo) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-09-01 (0 artículos nuevos) — Actions SÍ está corriendo
Última con artículos   : 2026-08-27 (1 artículo nuevo) → 6 días sin artículos nuevos, supera el máx. de 3

NUEVA CAUSA IDENTIFICADA (2026-09-02): bug en fetch_gdelt_historical()
  (scripts/fetch_news.py:428-477). Dos problemas distintos:

  1. Ventanas 2015-2016 SIEMPRE fallan (0/8 completadas, ver tabla de backfill).
     Cada corrida diaria reintenta esas 8 ventanas trimestrales desde cero
     (nunca se marcan completas porque batch=None en error de red), lo cual
     sugiere que la API GDELT DOC 2.0 simplemente no indexa contenido de
     2015-2016 (su índice de texto completo arranca ~2017), no que sea un
     problema de red transitorio. Esto contradice el supuesto de CLAUDE.md
     de que el límite real de GDELT es 2015-02-19.

  2. Ventana "frontera" duplicada casi a diario: 41 de las 77 ventanas
     GDELT completadas son variantes de "20260618_<fecha_ayer>" (ver
     desglose de backfill). Causa: current arranca en 2015-01-01 en cada
     ejecución, salta rápido las ventanas ya completas y las de 2015-2016
     (fallan pero igual avanzan), y llega a la ventana abierta más reciente
     (arrancando en 2026-06-18) cuyo fin es min(current+90d, ahora-1d).
     Como "ahora" crece 1 día por corrida y aún no alcanza current+90d,
     cada corrida cierra y marca-completa una ventana [20260618, ayer]
     ligeramente distinta a la del día anterior, sin cerrar nunca el
     trimestre real y sin avanzar current más allá de 2026-06-18. Esto
     infla el contador de "ventanas completadas" sin aportar cobertura
     histórica real ni sumar artículos nuevos consistentemente.

Impacto              : el backfill histórico 2015-2026 está efectivamente
                       detenido en 2015-2016 (bloqueado) y en 2026 (dando
                       vueltas sobre la misma ventana en expansión). El
                       progreso real es 2017-2025 completo (36/36 ventanas
                       trimestrales) — ver tabla de backfill.
Recomendación         : (a) ajustar fetch_gdelt_historical para NO reintentar
                       indefinidamente ventanas 2015-2016 si GDELT responde
                       consistentemente vacío/error — considerar marcarlas
                       completas-sin-datos tras N intentos, o mover el
                       `start` de cobertura a 2017-01-01 si se confirma el
                       límite real de la API; (b) cerrar la ventana frontera
                       en un límite fijo (ej. current+90d) en vez de
                       min(current+90d, ahora-1d) para evitar ventanas que
                       crecen un día a la vez.
Estado                : diagnosticado 2026-09-02, sin cambios de código
                       aplicados en esta sesión (requiere sesión de
                       desarrollo dedicada a scripts/fetch_news.py)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Bloqueado** — GDELT falla consistentemente (posible límite real del índice) |
| 2016 Q1-Q4 | 0/4 | **Bloqueado** — mismo problema que 2015 |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (ventana frontera) | 41 registradas | **Bug** — ventana [2026-06-18, ayer] se re-registra casi a diario en vez de cerrar un trimestre fijo; no representa 41 trimestres reales |
| **TOTAL real (trimestres 2017-2025)** | **36/36** | **Completo** |
| **TOTAL 2015-2016** | **0/8** | **Bloqueado — ver diagnóstico arriba** |

> Diagnóstico 2026-09-02: el conteo bruto de `_gdelt_windows` (77) NO refleja progreso
> lineal — ver sección "Estado del Fetch" arriba para el detalle de los dos bugs
> identificados (ventanas 2015-2016 nunca completan; ventana frontera 2026 se duplica
> a diario). Cobertura real confirmada por GDELT: 2017-01 → 2026-06 (trimestres completos).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-02 | 5 (4 reales + 1 falso positivo) | 33 | Routine programada. Diagnóstico: 6 días sin artículos nuevos + bugs en backfill GDELT (2015-2016 bloqueado, ventana 2026 duplicada a diario) + falsos positivos sistémicos por coincidencia de sigla "MIDA" con entidades de Malasia/otros países entre los 33 pendientes restantes |

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
