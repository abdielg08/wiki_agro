---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-10
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 | **0 nuevos** (0 en esta sesión) |
| Páginas en wiki/ | 26 (9 topics, 3 entities, 11 summaries, resto overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos en sources/ | **4** (último commit sources/: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ umbral superado** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit en sources/ : 2026-09-06 (6 artículos nuevos)
Días sin nuevos artículos              : 4 (sin commits en sources/ del 07 al 10 de sep)
Ventanas GDELT completadas             : 79 — supera el umbral de ~45 estimadas
Diagnóstico (CLAUDE.md Paso 4)         : con 45+ ventanas completadas, la causa más probable
                                          es que el rango de fechas GDELT disponible ya fue
                                          recorrido y necesita expansión, no un bloqueo/timeout
Fuentes RSS activas                    : IICA y La Prensa (no se puede confirmar desde este
                                          entorno si devolvieron artículos en 07-10 sep, ya que
                                          no hubo commits nuevos en sources/ para verificarlo)
Acción recomendada                     : revisar el workflow de GitHub Actions (fetch_historical.py)
                                          para confirmar si corrió en 07-10 sep; si las ventanas
                                          GDELT están agotadas, ampliar rango/estrategia de backfill
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
| 2026-09-10 | 5 | 39 | Todos sobre arroz/MIDA (importaciones, subsidios, inundaciones, compensaciones, transición ministerial); 0 falsos positivos. Detectado: 4 días sin nuevos artículos en sources/ y 79 ventanas GDELT (rango agotado) |

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
