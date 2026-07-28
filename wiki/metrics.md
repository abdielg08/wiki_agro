---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-28
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** — ver `log.md` 2026-07-28 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 57 / ~45 estimadas | 45 (2015→hoy) — **excede estimado, ver nota** |
| Días sin artículos nuevos | 8 (desde 2026-07-20) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-28 (corre diariamente — commits "chore(sources)" existen
                         casi todos los días, incluido hoy; Actions SÍ está corriendo)
Resultado reciente      : 0 artículos nuevos en 8 de los últimos 8 días hábiles
                         (último día con artículos nuevos: 2026-07-20, +2 artículos)
Causa raíz identificada : Ventanas GDELT completadas = 57, ya por encima de las ~45
                         estimadas para el backfill 2015→hoy → el backfill histórico
                         está esencialmente agotado (2017-2025 = 4/4 trimestres c/u,
                         100% completos). Las únicas fuentes activas para artículos
                         NUEVOS son ahora RSS (IICA, La Prensa), que aportan de forma
                         esporádica (0-2 artículos cada varios días).
Hallazgo adicional      : scripts/fetch_news.py::fetch_gdelt_historical() tiene un bug
                         de ventana final — el tramo 2026-06-18→hoy nunca alcanza los
                         90 días completos porque `end` (=ayer) avanza 1 día en cada
                         corrida, así que cada día genera una ventana final distinta
                         (20260618_20260623, _0624, _0626... 21 ventanas "completadas"
                         solo en 2026, cada una re-consultando casi el mismo rango).
                         Esto desperdicia cuota de la API sin avanzar cobertura real.
                         NO se modificó fetch_news.py en esta sesión (fuera del alcance
                         del routine de ingesta; requiere validación contra la API
                         real de GDELT antes de tocar el workflow diario en producción).
Hallazgo adicional 2    : Los años 2015 y 2016 tienen 0/4 ventanas completadas (todos
                         los demás años 2017-2025 están 4/4). Sugiere que esas ventanas
                         fallan consistentemente (posible límite real de cobertura de
                         GDELT DOC 2.0 antes de cierta fecha, o error de red repetido)
                         y nunca se marcan como completas — requiere investigación con
                         acceso a la API real (fuera del alcance de esta sesión).
Recomendación           : (1) corregir el bug de ventana final en fetch_news.py para
                         evitar duplicados, (2) investigar por qué 2015-2016 no
                         completan, (3) considerar agregar más fuentes RSS/scrape
                         para no depender solo de GDELT una vez agotado el backfill.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — falla consistente, ver diagnóstico** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — falla consistente, ver diagnóstico** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (parcial, hasta hoy) | 21 ventanas (con solapamiento — ver bug en Estado del Fetch) | En curso, duplicado |
| **TOTAL** | **57 ventanas registradas** | **2017-2025 completo; 2015-2016 bloqueado; 2026 en curso con duplicados** |

> El backfill real de contenido (2017-2025) está esencialmente completo — los "0 artículos
> nuevos" recientes son el resultado esperado de un backfill agotado, no una falla del fetch.
> Pendiente: desbloquear 2015-2016 y corregir la duplicación de ventanas en 2026 (ver
> hallazgos en "Estado del Fetch" arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-28 | 0 (11/11 falsos positivos) | 0 | Cola vaciada tras colisión de keyword "MIDA" (Malasia/Utah) y artículos genéricos de agricultura sin relación a Panamá. Fix de bug en `mark_ingested`/`mark_all_ingested` (scripts/ingest.py). Diagnóstico: backfill GDELT 2017-2025 completo, 2015-2016 bloqueado, ventana final de 2026 duplicada — ver "Estado del Fetch". |

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
