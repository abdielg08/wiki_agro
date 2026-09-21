---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ (descargados) | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 summaries, 2 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (38 trimestres únicos, algunos con reintentos) | ~45 trimestres (2015→hoy) |
| Días sin artículos nuevos en sources/ | **15 días** (último commit de fetch: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA        : 2026-09-06 (run #103, conclusion: success, 0 artículos nuevos)
Última corrida con commit     : 2026-09-06 (run #103, head_sha 24cfc3c, 6 artículos — commit previo)
Corridas desde entonces       : 14 corridas diarias programadas (run #104 → #117, 2026-09-07 → 2026-09-20)
Resultado                     : TODAS fallando — conclusion: failure, en ~3 segundos cada una
Diagnóstico                   : El job "Fetch artículos → Commit a sources/" termina en ~3s
                                 (created_at ≈ completed_at), tiempo insuficiente para siquiera
                                 completar actions/checkout + setup-python. Los logs del job
                                 devuelven HTTP 404 (no disponibles / nunca se generaron).
                                 Patrón consistente con: runner no asignado, límite de minutos/
                                 gasto de GitHub Actions agotado, o Actions deshabilitado a nivel
                                 de repositorio/organización — NO es un bug de fetch_gdelt.py ni
                                 de las fuentes RSS, porque el job nunca llega a ejecutar ese código.
Acción requerida               : Revisar en GitHub → Settings → Actions (general / billing) si
                                 Actions está habilitado y si hay minutos/gasto disponibles.
                                 Esto requiere acceso a la configuración del repositorio/cuenta,
                                 fuera del alcance de esta sesión de Claude Code.
Ventanas GDELT                 : 79 ventanas registradas mapean a solo 38 trimestres únicos
                                 (2017-Q1 → 2026-Q2), es decir, hay reintentos/duplicados.
                                 Los trimestres 2015-Q1 a 2017-Q1 (~8 trimestres, 2015-02-19 a
                                 2017-03-29) AÚN NO tienen ninguna ventana registrada — el
                                 backfill histórico real está incompleto en su tramo más antiguo,
                                 aunque el conteo bruto de "ventanas" ya supere el estimado de 45.
                                 El estancamiento de los últimos 15 días es 100% atribuible a la
                                 falla del runner de Actions descrita arriba, no a GDELT en sí.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1 – 2017 Q1 (~8 trimestres) | 0/8 | **Pendiente — sin cobertura** |
| 2017 Q1 – 2026 Q2 (38 trimestres) | 38/38 (con reintentos, 79 registros) | Completado |
| **TOTAL estimado** | **38/~46** | **Backfill histórico incompleto en el tramo 2015-2017** |

> Fuente: `sources/processed.json._gdelt_windows` (79 registros → 38 fechas de inicio únicas, todas ≥ 2017-03-30).
> Nada en processed.json cubre 2015-02-19 a 2017-03-29; ese tramo requiere ventanas GDELT nuevas una vez
> que el runner de Actions vuelva a funcionar (ver "Estado del Fetch" arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-21 | 5 | 39 | Routine automatizada. Diagnóstico: Actions falla 100% desde 2026-09-07 (14 corridas, conclusion=failure en ~3s); logs 404; requiere revisión de billing/permisos de Actions fuera de esta sesión |

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
