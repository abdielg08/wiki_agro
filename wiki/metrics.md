---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos descargados en sources/ | 57 | ↑ continuo |
| Artículos ingestados (reales, en wiki) | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados (documentados) | 9 (7 previos + 2 detectados 2026-09-20, aún no ingestados) | **0 nuevos ingestados** |
| Páginas en wiki/ | 27 (10 topics, 3 entities, 11 summaries, 2 overview + 1 metrics) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + fetch) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (`_gdelt_windows` en processed.json) | supera umbral de 45 → rango agotado, revisar expansión |
| Días sin artículos nuevos (commits a sources/) | 14 (última corrida con novedades: 2026-09-06) | máx 3 antes de diagnosticar → **ALERTA: superado** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con nuevos artículos : 2026-09-06 (commit 24cfc3c, "6 artículos nuevos descargados")
Commits a sources/ desde entonces   : ninguno hasta 2026-09-20 (14 días)
Ventanas GDELT completadas          : 79 (por encima del umbral de 45 mencionado en CLAUDE.md)
Causa probable                      : rango de fechas GDELT probablemente agotado para las ventanas
                                       configuradas, o el workflow de GitHub Actions dejó de correr o
                                       está siendo bloqueado. No se puede confirmar el estado exacto del
                                       workflow desde esta sesión (sin acceso a logs de Actions, solo al
                                       historial de commits de sources/).
Riesgo de calidad detectado         : 2 artículos en sources/articles/ (aún NO ingestados) con
                                       country=PA pero contenido real sobre Mozambique y Brasil —
                                       ver wiki/log.md (entrada 2026-09-20) para detalle. Indica que el
                                       filtro de país/idioma del fetch necesita revisión.
Pendientes de ingesta                : 39 artículos en cola (volumen acumulado, no bloqueo de fetch;
                                       a ritmo de ~15/día tomaría ~3 sesiones adicionales vaciar la cola)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | ?/4 | ? | Ver nota |
| 2016 Q1-Q4 | ?/4 | ? | Ver nota |
| 2017 Q1-Q4 | ?/4 | ? | Ver nota |
| 2018 Q1-Q4 | ?/4 | ? | Ver nota |
| 2019 Q1-Q4 | ?/4 | ? | Ver nota |
| 2020 Q1-Q4 | ?/4 | ? | Ver nota |
| 2021 Q1-Q4 | ?/4 | ? | Ver nota |
| 2022 Q1-Q4 | ?/4 | ? | Ver nota |
| 2023 Q1-Q4 | ?/4 | ? | Ver nota |
| 2024 Q1-Q4 | ?/4 | ? | Ver nota |
| 2025 Q1-Q4 | ?/4 | ? | Ver nota |
| 2026 Q1-Q3 | ?/3 | ? | Ver nota |
| **TOTAL** | **79 ventanas registradas** | **57 artículos descargados acumulados** | **En curso, posible agotamiento de rango** |

> Nota: `processed.json._gdelt_windows` registra 79 identificadores de ventana (formato `YYYYMMDD_YYYYMMDD`)
> pero no están agrupados por trimestre/año en el archivo, por lo que no se puede reconstruir aquí la
> tabla período-a-período sin inspeccionar cada entrada individualmente. Se deja pendiente para una sesión
> de mantenimiento dedicada a auditar `scripts/` y reconstruir esta tabla con datos reales.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-20 | 5 | 39 | Routine automatizada; 0 falsos positivos nuevos ingestados; se detectaron 2 falsos positivos nuevos sin ingestar (Mozambique, Brasil) y una alerta de 14 días sin nuevos commits de fetch |

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

**Estado actual de la alarma (2026-09-20)**: 14 días sin nuevos commits de fetch — señal activa.
Ver diagnóstico completo en "Estado del Fetch" arriba y en `wiki/log.md`.
