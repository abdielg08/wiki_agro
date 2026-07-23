---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 13 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (7 previos + 11 hoy) | **0 nuevos** ⚠️ ver nota |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 52 (primera: 2017-03-30) | ~47 (2015→hoy) |
| Días sin artículos nuevos | 2 (07-21, 07-22) + hoy pendiente | máx 3 antes de diagnosticar |

> ⚠️ **Nota sobre "0 nuevos" falsos positivos**: la meta de 0% se refiere a **contenido incorrecto publicado
> en el wiki** (páginas creadas para artículos no relacionados con Panamá) — esa meta se mantiene en 100%
> de cumplimiento; nunca se ha creado una página de wiki para un falso positivo. Los 18 falsos positivos
> acumulados son artículos correctamente **rechazados antes de llegar al wiki**. El problema real es que
> la fuente `web_searches.prensa_agro` (búsqueda DDG) está generando un volumen alto de ruido — ver
> diagnóstico de causa raíz en `wiki/log.md` (2026-07-23 08:03 y 08:10).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-22T12:22:07Z — completed / success
Resultado               : 0 artículos nuevos (07-21 y 07-22 también 0 nuevos; corrida de hoy 07-23
                          aún no dispara, cron es 11:00 UTC y son las 08:08 UTC)
Salud del workflow      : SANA — corre diariamente sin errores desde 2026-07-14 (única falla: 2026-07-13,
                          autorresuelta al día siguiente, no investigada esta sesión por ser un evento aislado)
Causa de "0 nuevos"     : no es una falla del workflow — simplemente no hay artículos nuevos que pasen el
                          filtro is_agro_relevant() esos días. Probable por: (a) ventanas GDELT ya cerca del
                          rango cubierto (52 completadas, ver abajo) y (b) las únicas fuentes RSS activas
                          (IICA, La Prensa) no publican contenido agro todos los días.
GAP HISTÓRICO DETECTADO : la ventana GDELT completada más antigua es 2017-03-30 — el rango 2015-01-01 a
                          2017-03-29 (config/sources.yaml date_range.start) NO aparece en
                          sources/processed.json["_gdelt_windows"]. O bien esas ventanas fallan
                          consistentemente (error de red/API para fechas tan antiguas) y nunca se marcan
                          completas, o el histórico 2015-2017 simplemente no se ha intentado aún en el fetch
                          diario (que solo agrega ventanas nuevas de forma incremental). Recomendación:
                          correr manualmente el workflow "Wiki Agropecuario — Crawl Histórico 15 Años"
                          (wiki_historical.yml, modo gdelt, years=2015-2017) para confirmar y llenar el hueco.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | **Pendiente — ver GAP HISTÓRICO arriba** |
| 2016 Q1-Q4 | 0/4 | ? | **Pendiente — ver GAP HISTÓRICO arriba** |
| 2017 Q1-Q4 | 4/4 | ? | Completo (desde 2017-03-30) |
| 2018 Q1-Q4 | 4/4 | ? | Completo |
| 2019 Q1-Q4 | 4/4 | ? | Completo |
| 2020 Q1-Q4 | 4/4 | ? | Completo |
| 2021 Q1-Q4 | 4/4 | ? | Completo |
| 2022 Q1-Q4 | 4/4 | ? | Completo |
| 2023 Q1-Q4 | 4/4 | ? | Completo |
| 2024 Q1-Q4 | 4/4 | ? | Completo |
| 2025 Q1-Q4 | 4/4 | ? | Completo |
| 2026 (parcial) | 1 ventana base + 15 variantes de una sola ventana en crecimiento diario | ? | Ver anomalía abajo |
| **TOTAL** | **52 registradas / ~38-40 ventanas únicas reales 2017-2026** | **?** | **Backfill 2017→hoy avanzado; 2015-2017 sin iniciar** |

> ANOMALÍA detectada en las ventanas de 2026: en vez de una ventana trimestral fija, el log muestra 16 claves
> del tipo `20260618_<fecha-creciente>` (una por cada día que corrió el fetch, con el extremo final avanzando
> un día a la vez: ...0623, 0624, 0626, 0627, 0628, 0701...). Esto ocurre porque `fetch_gdelt_historical()`
> calcula `end = min(config_end, utcnow()-1)`, que cambia cada día — como la ventana "actual" (2026-06-18 en
> adelante) nunca llega a los 90 días completos antes de que `end` la trunque, cada corrida genera una
> `window_key` nueva y la marca completa, sin nunca "cerrar" un trimestre real. No es incorrecto (no duplica
> artículos gracias al `url` como clave real de dedupe) pero infla el contador de ventanas y no refleja
> trimestres reales. No se modificó el código esta sesión — queda documentado para una futura sesión de fix.
> Una vez que se cubra el rango 2015-2017 (ver GAP arriba), actualizar esta tabla con los datos reales
> por artículo. El rendimiento real de GDELT (artículos/trimestre) determinará la duración del backfill.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-23 | 0 (11/11 revisados fueron falsos positivos) | 0 | Ver diagnóstico completo en wiki/log.md. Fix aplicado: `mark_ingested()` crasheaba por clave interna `_gdelt_windows` no filtrada (scripts/ingest.py). Bug documentado (no corregido): `mark-all-ingested` puede marcar artículos distintos a los revisados por Claude — usar `mark-ingested '<url>'` por artículo en su lugar. |

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
