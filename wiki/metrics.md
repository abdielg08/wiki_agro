---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-27
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 50 | ↑ continuo |
| Artículos reales ingestados | 10 | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** ⚠️ ver nota |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2015-2026 | 2015 → hoy real |
| Ventanas GDELT completadas | 75 / ~45 estimadas | rango agotado, necesita expansión |
| Días sin artículos nuevos | **3** ⚠️ ALARMA | máx 3 antes de diagnosticar |

> ⚠️ **Falso positivo nuevo (2026-08-27)**: 1 registro (dominio `paultan.org`, sobre
> el MITI de Malasia) coló el filtro de relevancia por coincidencia de siglas
> (MIDA/MARii/MITI). Tasa de falsos positivos NO es 0% este período — ver
> `wiki/log.md` 2026-08-27 para el detalle y la recomendación de mejorar el
> filtro de clasificación en el pipeline de fetch.
>
> ⚠️ **Alarma de días sin artículos nuevos**: el último commit con artículos
> realmente nuevos en `sources/` fue **2026-08-24** (20 artículos). Los días
> 2026-08-25 (commit con 0 nuevos), 2026-08-26 y 2026-08-27 (sin commits de
> `sources/` en absoluto) suman **3 días consecutivos sin artículos nuevos**,
> el umbral de falla definido en `CLAUDE.md`. Ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit en sources/ : 2026-08-25 11:25 UTC (0 artículos nuevos)
Última corrida con artículos reales   : 2026-08-24 11:24 UTC (20 artículos nuevos)
Commits de sources/ 2026-08-26/27     : NINGUNO encontrado en git log
Causa identificada     : (1) Bug real en fetch_gdelt_historical() (scripts/fetch_news.py):
                          las ventanas 2015-2016 nunca logran completarse (se
                          reintentan y fallan cada día sin persistir avance), y
                          la ventana final cerca de "hoy" se regenera con una
                          clave nueva cada día en vez de cerrarse — ver detalle
                          y causa raíz completa en "Progreso del Backfill GDELT"
                          más abajo.
                          (2) Las fuentes RSS activas (IICA, La Prensa) son
                          intermitentes — solo 1-20 artículos en corridas
                          puntuales, 0 en la mayoría de los días.
                          (3) Ausencia total de commits en sources/ el 26 y 27
                          de agosto sugiere que el workflow de GitHub Actions
                          pudo no haberse ejecutado esos días (a diferir de
                          "corrió y encontró 0", que sí genera commit).
Diagnóstico             : con el backfill GDELT atascado por el bug descrito y
                          RSS intermitente, el ritmo de ingreso de artículos
                          nuevos depende casi exclusivamente de RSS. Se recomienda
                          (a) corregir el bug en fetch_gdelt_historical() (ver abajo);
                          (b) verificar en GitHub Actions si el workflow programado
                          corrió el 26-27/08 (posible fallo silencioso o cron
                          deshabilitado); (c) expandir fuentes RSS o añadir nuevos
                          medios de Nivel 3 (Panamá América, TVN, La Estrella) para
                          sostener el flujo diario objetivo de ~15 artículos/día.
Estado                  : PENDIENTE — requiere revisión manual del workflow de
                          Actions (no verificable desde esta sesión de wiki).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | 0/4 | ⚠️ **Pendiente — no cubierto** |
| 2016 | 0/4 | ⚠️ **Pendiente — no cubierto** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 | 39 | ⚠️ **Anómalo — muy por encima de lo esperado (~2)** |
| **TOTAL** | **75** | Ver hallazgo abajo |

> **Recalculado el 2026-08-27** a partir de `sources/processed.json → _gdelt_windows`
> (75 entradas, formato `YYYYMMDD_YYYYMMDD`, agrupadas por año de inicio).
>
> ⚠️ **Causa raíz identificada** (revisado `scripts/fetch_news.py::fetch_gdelt_historical`,
> la función que corre a diario vía `wiki_daily.yml` con `mode=all`):
>
> 1. **2015-2016 nunca se completan.** La función siempre reinicia `current = start`
>    (2015-01-01) en cada ejecución y solo avanza el puntero local sin marcar la
>    ventana como completada cuando `fetch_gdelt_batch()` devuelve `None` (error de
>    red/HTTP). Como ese avance es **local a la llamada** y no se persiste en
>    `processed["_gdelt_windows"]`, si las ventanas de 2015-2016 fallan
>    consistentemente (posible rechazo de GDELT para rangos tan antiguos, o
>    rate-limit), se reintentan — y fallan — en cada corrida diaria, sin nunca
>    quedar marcadas como completas ni avanzar el backfill real para esos años.
> 2. **La ventana final (2026) se duplica cada día.** `end = min(config_end,
>    datetime.utcnow() - timedelta(days=1))` cambia un día cada vez que corre el
>    workflow. Como el `window_key` incluye la fecha de fin exacta, la ventana
>    final (`20260618_<ayer>`) genera una clave **distinta cada día**
>    (`20260618_20260623`, `20260618_20260720`, `20260618_20260814`, `20260618_20260809`,
>    `20260618_20260816`, …), por lo que nunca se "cierra" un trimestre real —
>    solo se acumulan decenas de ventanas solapadas para el mismo período reciente.
>
> **Recomendación**: en `fetch_gdelt_historical()`, (a) registrar los intentos
> fallidos por ventana (con conteo/backoff) en vez de reintentar 2015-2016 desde
> cero cada día indefinidamente, y (b) anclar el límite superior de la ventana
> final a un corte de trimestre fijo (o al menos a medianoche UTC del día,
> constante durante ese trimestre) en vez de `utcnow()-1d`, para que dicha
> ventana pueda completarse y dejar de regenerarse a diario.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-27 | 4 reales + 1 falso positivo excluido | 32 | Rutina programada; ver diagnóstico de fetch arriba |

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
