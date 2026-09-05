---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-05
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
| Páginas en wiki/ | 26 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial 2017-2024) | 2015 → hoy real |
| Ventanas GDELT completadas (trimestrales) | 37 / 46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos en sources/ | **9** (última descarga real: 2026-08-27) | máx 3 antes de diagnosticar ⚠️ |

**⚠️ ALERTA ACTIVA**: han pasado 9 días sin artículos nuevos reales en `sources/articles/` (última descarga con contenido nuevo: 2026-08-27, +1 artículo). Las corridas de GitHub Actions de 2026-09-01, 2026-09-03 y 2026-09-04 reportaron 0 artículos nuevos. Esto excede el umbral de 3 días definido como falla del sistema — ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Últimas corridas Actions : 2026-09-01, 2026-09-03, 2026-09-04 → 0 artículos nuevos cada una
Última corrida con datos : 2026-08-27 (+1 artículo) | 2026-08-24 (+20 artículos, lote grande)
Causa identificada (nueva, 2026-09-05):
  sources/processed.json → _gdelt_windows contiene 79 entradas:
    - 37 son ventanas trimestrales de backfill histórico real, cubriendo de forma
      continua 2017-03-30 → 2026-06-17 (ver tabla de progreso abajo)
    - 42 son ventanas ANÓMALAS con formato "20260618_2026MMDD": inicio FIJO en
      2026-06-18 y fin avanzando día a día hasta 2026-09-03. Esto indica que el
      fetch diario de GitHub Actions está registrando una ventana nueva de
      "hoy" en cada corrida en lugar de continuar el backfill retroactivo hacia
      2015-2016. Como esas ventanas casi no contienen artículos agro-Panamá
      nuevos, el resultado observado es 0 artículos/día.
  Además no existe NINGUNA ventana registrada para 2015 ni 2016 — el backfill
  real hacia el objetivo (2015-02-19) no ha avanzado desde que se resetearon
  las ventanas en 2026-06-22; todo el progreso posterior (37 ventanas) avanzó
  HACIA ADELANTE desde 2017-03-30 en vez de hacia atrás desde esa fecha.
Fix aplicado anteriormente (2026-06-22) : fetch_gdelt_historical() limita end a
                                          datetime.utcnow()-1d
Estado                                  : el fix de fechas futuras funcionó,
                                          pero la lógica de selección de la
                                          PRÓXIMA ventana a procesar parece
                                          priorizar ventanas cercanas a "hoy"
                                          en vez de las ventanas 2015-2016
                                          pendientes. Requiere revisión de
                                          scripts/fetch_historical.py
                                          (función que decide qué ventana
                                          procesar a continuación).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | Pendiente |
| 2016 Q1-Q4 | 0/4 | ? | Pendiente |
| 2017 Q1-Q4 | 3/4 | ? | Parcial (falta Q1: ene-mar 2017) |
| 2018 Q1-Q4 | 4/4 | ? | Completado |
| 2019 Q1-Q4 | 4/4 | ? | Completado |
| 2020 Q1-Q4 | 4/4 | ? | Completado |
| 2021 Q1-Q4 | 4/4 | ? | Completado |
| 2022 Q1-Q4 | 4/4 | ? | Completado |
| 2023 Q1-Q4 | 4/4 | ? | Completado |
| 2024 Q1-Q4 | 4/4 | ? | Completado |
| 2025 Q1-Q4 | 4/4 | ? | Completado |
| 2026 Q1-Q2 | 2/2 | ? | Completado (hasta 2026-06-17) |
| **TOTAL** | **37/46** | **—** | **9 ventanas pendientes, todas en 2015–2016 (+ Q1 2017)** |

> Nota: además de las 37 ventanas de backfill arriba, `_gdelt_windows` registra 42
> ventanas adicionales anómalas de "hoy" (20260618_2026MMDD) que NO forman parte
> de esta tabla y no contribuyen al backfill histórico — ver "Estado del Fetch".
> El conteo de artículos por ventana no se registra actualmente en processed.json;
> columna "Artículos" queda pendiente de instrumentación.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Falsos positivos | Pendientes restantes | Nota |
|-------|---------------------|-------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 (auditoría) | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-05 | 4 reales | 1 nuevo (total 8) | 33 | Backfill 2022-2024 (arroz, transición MIDA, inundaciones Veraguas); detectada alerta de 9 días sin fetch nuevo y anomalía en ventanas GDELT |

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

**Estado actual de la alarma (2026-09-05)**: ACTIVA — 9 días sin artículos nuevos.
Diagnóstico documentado en `wiki/log.md` (entrada 2026-09-05): el fetch de
GitHub Actions está generando ventanas GDELT de "hoy" repetidamente en vez de
continuar el backfill retroactivo hacia 2015-2016, lo que probablemente explica
la falta de artículos nuevos relevantes. Recomendación: revisar la función de
selección de ventanas en `scripts/fetch_historical.py`.
