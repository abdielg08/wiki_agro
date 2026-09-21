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
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados (ingestados) | 7 | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 25 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 (`_gdelt_windows` en processed.json) | cobertura 2015→hoy |
| Días sin artículos nuevos en sources/ | 15 (última descarga: 2026-09-06) | máx 3 antes de diagnosticar |

⚠️ **Alerta**: 15 días sin artículos nuevos en `sources/` — supera el umbral de 3 días. Ver
diagnóstico en "Estado del Fetch" abajo.

⚠️ **Alerta de calidad de datos**: de los 39 artículos pendientes, un análisis de esta sesión
estima que **~17 (≈44%)** son falsos positivos claros — no tratan sobre agro panameño (p. ej.
"MIDA" de Malasia/Utah en vez del Mida de Panamá, agricultura de Aragón/España, Mozambique, Brasil,
Arabia Saudita, papers de IEEE, noticias de data centers en Utah, etc.), todos etiquetados
incorrectamente con `source: prensa.com`. Ver diagnóstico completo en `wiki/log.md`
(entrada 2026-09-21). **No fueron ingestados** — deben filtrarse manualmente artículo por artículo
en cada sesión de `ingest`, no confiar en el campo `source`.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-09-06 (commit 24cfc3c, sources/ sin cambios desde entonces)
Resultado               : 6 artículos nuevos en esa corrida; 0 en las corridas previas registradas
Días sin artículos      : 15 (2026-09-06 → 2026-09-21)
Causa por confirmar     : no se puede determinar desde esta sesión si Actions dejó de correr o si
                          corrió y devolvió 0 artículos nuevos — requiere revisar el historial de
                          runs de GitHub Actions directamente (fuera del alcance de esta sesión CLI)
Hallazgo nuevo          : contaminación de falsos positivos en source=prensa.com (ver alerta arriba)
                          sugiere que el fetch (GDELT y/o RSS) está capturando resultados fuera de
                          Panamá por colisión de palabras clave (p. ej. "MIDA", "agro", "farm")
Recomendación           : (1) revisar logs de Actions para confirmar si corrió en los últimos 15
                          días; (2) endurecer el filtro de relevancia Panamá en fetch_gdelt/RSS
                          antes de guardar en sources/articles/ (país=PA, dominio .gob.pa/.pa, o
                          keywords geográficas panameñas) para reducir el ruido en pending_ingest
```

---

## Progreso del Backfill GDELT (2015 → hoy)

`processed.json._gdelt_windows` reporta **79 ventanas completadas** en total (no desglosadas por
trimestre en el registro actual). La tabla trimestral detallada de abajo quedó desactualizada desde
la sesión semilla y no pudo reconstruirse con los datos disponibles en esta sesión (el script no
expone el desglose por ventana, solo el conteo agregado). Se mantiene como referencia de formato;
requiere que una sesión futura con acceso a `processed.json._gdelt_windows` en detalle la rellene.

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2016 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2017 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2018 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2019 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2020 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2021 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2022 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2023 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2024 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2025 Q1-Q4 | ?/4 | ? | Ver nota arriba |
| 2026 Q1-Q2 | ?/2 | ? | Ver nota arriba |
| **TOTAL** | **79 ventanas (agregado)** | 57 artículos en sources/ | **En progreso** |

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-21 | 5 | 39 | Sesión programada. 0 falsos positivos ingestados. Detectada contaminación de ~17 falsos positivos (source=prensa.com mal etiquetado) en la cola de pendientes — ver alerta arriba y wiki/log.md |

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
