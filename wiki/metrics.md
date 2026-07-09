---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (+6 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 46 (⚠ ver nota) | 2015→hoy sin huecos |
| Días sin artículos nuevos reales | 7 (último: 2026-07-02) | máx 3 antes de diagnosticar |

**⚠ ALERTA — umbral de falla superado**: 7 días sin ningún artículo nuevo genuino en
`sources/articles/` (último: 2026-07-02). Supera el límite de 3 días consecutivos definido
como falla del sistema en `CLAUDE.md`. Ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-08 (commit b46e6af, "0 artículos nuevos")
Corridas recientes     : 07-08 (0), 07-04 (0), 07-03 (0), 07-02 (1) — hueco sin commits 07-05..07-07
Resultado               : 0 artículos nuevos desde 2026-07-02 (7 días)
Últimos "artículos nuevos" descargados eran en su mayoría falsos positivos
  (5/5 y 1/1 de esta sesión eran de EE.UU./Arabia Saudita, no de Panamá)

Diagnóstico ventanas GDELT (_gdelt_windows en processed.json, 46 total):
  - 2017–2025: 4 ventanas/año completadas (36 total) — patrón limpio, backfill trimestral OK
  - 2015–2016: 0 ventanas completadas — HUECO TOTAL, nunca se ha descargado nada de estos años
  - 2026: 10 ventanas fragmentadas, todas con inicio fijo 2026-06-18 y fin creciente día a día
    (20260618_20260623, _20260624, _20260626, _20260627, _20260628, _20260701, _20260702,
     _20260703, _20260707) — es el "borde" del trimestre en curso (aún no cierra, termina
     2026-09-17), se re-consulta cada día con la fecha de "ayer" como fin. No es necesariamente
     un bug: el trimestre actual no cierra hasta -90 días desde 2026-06-18-, pero SÍ indica que
     el conteo de "46 ventanas completadas" no equivale a cobertura uniforme 2015→hoy.

Causa probable del hueco 2015-2016: fetch_gdelt_historical() (scripts/fetch_news.py) camina
  secuencialmente desde config start=2015-01-01 cada corrida, pero si fetch_gdelt_batch()
  devuelve error de red (batch is None) la ventana se salta SIN marcarse completa y el loop
  avanza igual — es decir, si GDELT falla consistentemente para 2015-2016 (posible límite real
  de cobertura de la GDELT DOC 2.0 API, pese a que el proyecto GDELT existe desde feb-2015),
  esas ventanas nunca se completan ni se reintentan con prioridad; el loop simplemente sigue
  de largo hacia años posteriores donde sí hay respuesta. Esto NO se ha confirmado con logs de
  Actions (no accesibles desde esta sesión) — queda como hipótesis a validar revisando el log
  de la próxima corrida de `wiki_daily.yml`, o corriendo manualmente:
  `python wiki_agro.py fetch --mode gdelt --years 2015-2016` y observando si tira error de red.

Recomendación: no marcar "backfill agotado" solo por ver 45+ ventanas — verificar que las
  ventanas cubran 2015→hoy sin huecos (ver tabla de Progreso del Backfill abajo).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | ⚠ **HUECO — nunca descargado** |
| 2016 Q1-Q4 | 0/4 | ⚠ **HUECO — nunca descargado** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (parcial) | 10 ventanas fragmentadas | En curso — trimestre actual no cierra hasta 2026-09-17 |
| **TOTAL** | **46** | **2015–2016 pendientes; 2017–2025 completo; 2026 en curso** |

> Origen de estos números: conteo directo de `sources/processed.json["_gdelt_windows"]`
> (2026-07-09). El artículo/ventana no se registra por separado — GDELT devuelve 0 o más
> artículos por ventana y todos pasan por el mismo filtro `is_agro_relevant`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-09 | 0 (6/6 rechazados como falsos positivos) | 0 | 0% falsos positivos ingestados; diagnóstico: hueco GDELT 2015-2016, 7 días sin artículos reales nuevos |

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
