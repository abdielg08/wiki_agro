---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-22
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 25 (8 topics, 3 entidades, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal (artículos en sources/) | 2007-11-04 → 2026-08-21 | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | 45+ (2015→hoy) |
| Días sin artículos nuevos en sources/ | **16** (último commit: 2026-09-06) | máx 3 antes de diagnosticar |

**ALERTA — sistema en falla**: 16 días consecutivos sin artículos nuevos en `sources/articles/`, muy por encima
del umbral de 3 días definido en CLAUDE.md. Ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit exitoso : run #103, 2026-09-06 13:50 UTC
                                     "chore(sources): 0 artículos nuevos descargados" — conclusion=success, ~6 min
Corridas desde entonces            : runs #104-#118 (2026-09-07 → 2026-09-21), 15 corridas CONSECUTIVAS con
                                      conclusion=failure, ninguna generó commit nuevo
Duración de las corridas fallidas  : 3-70 segundos (vs. ~6-7 min en corridas exitosas)
Causa identificada                 : la duración extremadamente corta indica que el job falla ANTES de que el
                                      runner llegue a ejecutar los pasos del workflow (checkout/pip install/fetch)
                                      — no es un bug en fetch_news.py ni en las fuentes RSS/GDELT, ya que el
                                      código no cambió desde la última corrida exitosa (mismo head_sha 24cfc3c
                                      en las 15 corridas fallidas). Patrón consistente con un problema de
                                      aprovisionamiento de runner a nivel de cuenta/organización (p. ej. minutos
                                      de Actions agotados, límite de gasto, o política que bloquea la ejecución)
                                      — no se pudo confirmar el mensaje exacto porque los logs de job no están
                                      disponibles para descarga (HTTP 404 vía API — normal cuando el runner
                                      nunca llegó a iniciarse).
Verificación local                 : `pip install -r requirements.txt` se probó localmente con Python 3.11.15
                                      (misma versión que especifica el workflow) y completó sin errores,
                                      descartando una regresión de dependencias como causa.
Acción requerida                   : el propietario del repositorio debe revisar en GitHub
                                      (Settings → Billing/Actions, o la pestaña Actions del run) el motivo
                                      exacto por el que el runner no se aprovisiona — está fuera del alcance de
                                      esta sesión (sin acceso a facturación/configuración de cuenta).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — hueco de cobertura** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — hueco de cobertura** |
| 2017 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2018 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2019 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2020 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2021 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2022 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2023 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2024 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2025 Q1-Q4 | 4/4 | ver sources/ | Completado |
| 2026 (ventanas variables) | 43 | ver sources/ | En curso (año actual) |
| **TOTAL** | **79** | **57 artículos en sources/** | **2017-2026 cubierto; 2015-2016 pendiente** |

> Cifras derivadas de `sources/processed.json` → `_gdelt_windows` (conteo por año del prefijo `YYYY` de cada
> ventana `YYYYMMDD_YYYYMMDD`). **Hallazgo clave**: no hay ninguna ventana completada para 2015-2016 — el
> backfill histórico aún no cubre el inicio del rango objetivo (2015-02-19). Esto debe priorizarse una vez que
> el fetch automático (Actions) se restablezca (ver "Estado del Fetch" arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-22 | 5 (arroz, políticas, MIDA) | 39 | Routine automatizada. Diagnóstico: 16 días sin fetch nuevo — Actions falla en <70s desde run #104 (2026-09-07) |

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
