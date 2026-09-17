---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-17
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
| Falsos positivos acumulados | 7 | **0 nuevos** (0 nuevos esta sesión) |
| Páginas en wiki/ | 26 (9 topics, 3 entidades, 11 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (semilla + 5 artículos 2022-2025) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | ~45-46 estimadas → **rango agotado, backfill detenido por falla de Actions (ver abajo)** |
| Días sin artículos nuevos en sources/articles/ | **11** (último: 2026-09-06) | máx 3 antes de diagnosticar — **UMBRAL SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA           : run #103, 2026-09-06 (commit "6 artículos nuevos descargados",
                                    duración normal ~5.5 min)
Corridas fallidas consecutivas   : runs #104 a #114 (2026-09-07 → 2026-09-17), 11 de 11 con
                                    conclusion=failure
Patrón de la falla                : cada corrida falla en 3-6 segundos, SIN runner asignado
                                    (runner_id: 0) y sin logs (HTTP 404 al pedir logs del job) →
                                    el job nunca llega a ejecutar `pip install` ni el script Python.
                                    NO es un error del código de fetch_news.py / fetch_historical.py.
Causa más probable                : límite de gasto/minutos de GitHub Actions agotado en la cuenta,
                                    o cambio en permisos/configuración de Actions del repositorio
                                    abdielg08/wiki_agro. Ninguna de las dos se puede corregir desde
                                    una sesión de ingesta (requiere acceso a Settings del repo/cuenta).
Acción recomendada (dueño repo)   : revisar GitHub → Settings → Actions → General (permisos) y
                                    Settings → Billing → Plans and usage (minutos/gasto incluidos).
Impacto                           : 11 días consecutivos sin artículos nuevos; backfill histórico
                                    GDELT (79 ventanas completadas) detenido en el mismo punto.
Estado                             : Reportado al usuario en esta sesión (2026-09-17). Pendiente de
                                    acción externa — la próxima sesión debe re-verificar si las
                                    corridas de Actions volvieron a `conclusion: success`.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| **TOTAL** | **79 completadas** | **57 descargados (todas las fuentes)** | **Detenido desde 2026-09-07 por falla de Actions (ver "Estado del Fetch")** |

> 79 ventanas completadas ya supera la estimación original de ~45-46 ventanas para cubrir 2015→hoy,
> por lo que el rango de fechas configurado está agotado — el siguiente paso normal sería expandir
> el rango o pasar a otras fuentes (CDX/sitemap/FAO/WorldBank vía `wiki_historical.yml`). Sin
> embargo, esto es secundario mientras el fetch diario (`wiki_daily.yml`) siga fallando: no tiene
> sentido expandir rango si ni siquiera el job arranca. Resolver primero el problema de Actions.
> Desglose por período no disponible en `processed.json` — solo se registra el conteo agregado de
> ventanas (`_gdelt_windows`).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-17 | 5 | 39 | 0 falsos positivos nuevos; diagnosticado fetch de Actions caído desde 2026-09-07 (11 corridas fallidas consecutivas) |

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
