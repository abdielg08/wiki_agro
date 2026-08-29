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
| Artículos reales ingestados | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** (1 nuevo detectado y excluido esta sesión) |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 25 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 / ~45 estimadas | 45 (2015→hoy) — **superado, revisar lógica** |
| Días sin artículos nuevos | 2 (último: 2026-08-27) | máx 3 antes de diagnosticar |

---

## ⚠️ Alerta: contaminación de la cola con falsos positivos no panameños

Al 2026-08-29, de los 33 artículos aún pendientes, una revisión manual encontró que
**una parte sustancial (~20 de 38 antes de este lote) no son sobre agro panameño**:
noticias de MIDA Malasia (Malaysian Investment Development Authority), data centers en
Utah, política regional española (Aragón), Mozambique, Brasil, Arabia Saudita, papers
académicos genéricos, etc. Causa probable: términos de búsqueda ambiguos (p.ej. "MIDA",
"agriculture") sin filtro de país suficientemente estricto en el fetch. Ver detalle en
`wiki/log.md` (entrada 2026-08-29). **Pendiente**: revisar y endurecer `scripts/fetch*.py`
en una sesión dedicada; no se tocó el pipeline de fetch en esta rutina de ingesta.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-08-27 (1 artículo nuevo)
Corridas recientes                  : 2026-08-21 (0), 2026-08-22 (0), 2026-08-24 (20),
                                       2026-08-25 (0), 2026-08-27 (1)
Observación                         : el lote de 20 artículos del 2026-08-24 es la fuente
                                       principal de los falsos positivos detectados (ver alerta arriba)
Ventanas GDELT                      : 76 completadas, supera la estimación de ~45 de CLAUDE.md
                                       → revisar si el rango histórico se agotó o si el crawler
                                       re-visita ventanas ya cubiertas
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
| 2026-08-29 | 4 reales + 1 falso positivo excluido | 33 | Fix bug mark_ingested; alerta contaminación cola (~20 falsos positivos no panameños) |

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
