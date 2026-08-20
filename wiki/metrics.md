---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 25 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 70 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 1 (último fetch: 2026-08-19, 1 artículo) | máx 3 antes de diagnosticar |
| Pendientes de ingesta | 0 | 0 |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con contenido : 2026-08-19 (1 artículo nuevo — resultó falso positivo)
Corridas recientes           : mayormente 0 artículos/día desde 2026-08-04
Ventanas GDELT completadas   : 70 (superó la meta de ~46) — pero muchas se
                                solapan en fechas recientes (ej. 20260618_20260626,
                                20260618_20260727, 20260618_20260806 aparecen todas)
                                en vez de expandir cobertura histórica 2015-2018.
Causa identificada (2026-08-20): la fuente etiquetada "prensa.com" (24/30 = 80%
                                del total descargado) resultó ser 100% falsos
                                positivos en esta sesión — 18/18 pendientes no
                                mencionaban Panamá. El fetch parece buscar por
                                palabras clave genéricas de agro (o la sigla
                                "MIDA") sin exigir mención explícita de
                                "Panamá"/"Panama", capturando noticias de
                                Malasia, Utah (EE.UU.), Brasil, Irán, España,
                                Arabia Saudita y Maine (EE.UU.).
Acción recomendada     : agregar filtro de relevancia geográfica ("Panamá" o
                          "Panama" en título/texto) antes de guardar el
                          artículo como candidato, y/o revisar por qué domina
                          la fuente "prensa.com" con dominios no panameños.
Estado                  : 0 pendientes tras esta sesión; el problema no es
                          volumen de fetch sino precisión — ver wiki/log.md
                          2026-08-20 08:35 para detalle completo.
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
| 2026-08-20 | 0 | 0 | 18 falsos positivos (100% de pendientes) — colisión "MIDA" y fetch sin filtro geográfico; fix de bug en `mark_ingested()` |

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
