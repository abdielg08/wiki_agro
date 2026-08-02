---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** (16 detectados hoy, 0 ingestados al wiki) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 61 (38 distintas) / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos reales en wiki | 70 (desde 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-02 (commit bf0b8e0, "0 artículos nuevos")
Resultado               : el fetch SÍ corre 3x/día, pero el 100% de lo descargado desde
                          el 2026-06-22 son falsos positivos: colisión de la sigla "MIDA"
                          (Utah/EE.UU., Malasia) más contenido agro genérico sin filtro
                          de país (España/Aragón, Brasil, Arabia Saudita, Irán, EE.UU.)
Causa raíz identificada : "MIDA" está en HIGH_PRIORITY_TERMS de scripts/prioritize.py
                          sin verificar que sea el MIDA panameño, así que estos falsos
                          positivos escalan al tope del ranking de score cada sesión.
Backfill histórico      : 2015-01-01 → 2017-03-29 (9 ventanas trimestrales, el tramo
                          más antiguo del objetivo) NUNCA se completa — falla en cada
                          corrida desde el reset del 2026-06-22 sin quedar marcado.
                          Detalle completo en wiki/log.md (entrada 2026-08-02 16:07).
Bugs de herramienta      : 2 bugs encontrados y corregidos hoy en scripts/ingest.py —
                          orden inconsistente en mark_all_ingested() (marcaba artículos
                          distintos a los revisados) y crash en mark_ingested() por la
                          clave interna _gdelt_windows. Detalle en wiki/log.md.
Estado post-fix         : pendiente validar en próxima corrida Actions si el backfill
                          2015-2017 avanza; el problema de falsos positivos por "MIDA"
                          sigue sin mitigar en el fetch/scoring (fuera de alcance hoy).
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
| 2026-08-02 | 0 | 0 | 16 falsos positivos detectados y descartados (0 al wiki); 2 bugs corregidos en scripts/ingest.py; diagnóstico de backfill 2015-2017 estancado |

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
