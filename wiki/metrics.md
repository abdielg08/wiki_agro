---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-01
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos reales ingestados | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 77 / ~45 estimadas | 45 (2015→hoy) — **rango base ya superado** |
| Días sin artículos nuevos | 5 (último: 2026-08-27) | máx 3 antes de diagnosticar — **⚠ excedido** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-09-01
Resultado               : 0 artículos nuevos (Actions corrió correctamente, sin errores de conexión)
Último artículo nuevo   : 2026-08-27 (1 artículo) → 5 días consecutivos sin artículos nuevos
Ventanas GDELT          : 77 completadas (supera el estimado de 45 para cobertura 2015→hoy)
Causa identificada      : el rango de fechas GDELT disponible parece ya recorrido (77 > 45
                          ventanas estimadas); no hay evidencia de bloqueo/timeout puntual en
                          esta corrida. El estancamiento es consistente con un backfill GDELT
                          cercano a agotarse, no con una falla transitoria.
Fuentes RSS             : sin evidencia de fallos específicos revisada en esta sesión
Recomendación           : revisar scripts/fetch.py (generación de ventanas GDELT) para confirmar
                          cobertura real 2015-02-19→hoy y decidir: (a) expandir ventanas /
                          re-intentar ventanas con 0 resultados, (b) reforzar fuentes RSS como
                          canal principal de artículos nuevos diarios, o (c) aceptar backfill
                          GDELT como mayormente completo y enfocar en ingesta del backlog (33
                          pendientes) y fetch incremental diario.
Estado                  : Sin corregir en esta sesión — documentado para próxima routine/sesión interactiva
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
| 2026-09-01 | 4 reales + 1 falso positivo | 33 | Falso positivo: artículo sobre MITI/Malasia (colisión de sigla "MIDA"); fetch corrió pero 0 artículos nuevos desde 2026-08-27 (5 días); GDELT en 77/45 ventanas — posible rango agotado |

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
