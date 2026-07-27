---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-27
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (7 previos + 11 el 2026-07-27) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 56 (9 bloqueadas 2015-01→2017-03, 19 redundantes por bug de clave) | 45-47 (2015→hoy) |
| Días sin artículos nuevos | 7 (último real: 2026-07-20) | máx 3 — **SUPERADO** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-26 (run 30201051693) — exitosa, 0 artículos nuevos
Resultado              : 0 artículos nuevos reales por 7 días consecutivos (2026-07-21 → 2026-07-27)

Causas confirmadas con logs reales de Actions:
  1. RSS IICA y LaPrensaGeneral → "0 entradas en el feed" (feeds vacíos o rotos)
  2. DDG: 7/8 búsquedas configuradas → "No results found"
     (oirsa_alertas, mida_noticias, idiap_investigacion, bda_credito,
     fao_panama, banco_mundial_pa, iica_panama). Solo "prensa_agro" da
     resultados, y hasta hoy el 100% eran falsos positivos (11 documentados
     en wiki/log.md el 2026-07-27).
  3. GDELT bloqueado (403/429) para las 9 ventanas históricas más antiguas
     (2015-01-01 → 2017-03-29) — NO es un problema de rango de fechas.
  4. GDELT ventana "actual" responde 200 OK pero 0 artículos para
     sourcecountry:PA + términos configurados.
  5. Bug de código (sin corregir): la ventana GDELT "actual" usa
     end=utcnow()-1día tanto para el rango como para la clave de ventana →
     genera una clave nueva cada día y nunca se completa de forma estable
     (19 ventanas redundantes acumuladas). Ver wiki/log.md 2026-07-27.

Fix aplicado esta sesión (2026-07-27):
  - fetch_ddg_search() ahora aplica _is_blocked_domain()/_is_panama_related()
    (mismo filtro que fetch_rss/GDELT) — debería eliminar la fuente #2 de
    falsos positivos hacia adelante.
  - mark_ingested() ya no crashea con la clave interna _gdelt_windows.

Pendiente (no corregido, requiere más investigación):
  - Por qué GDELT bloquea específicamente 2015-2017 (¿rate limit acumulado,
    IP compartida de GH Actions, cambio de API?).
  - Por qué 7/8 búsquedas DDG a dominios .gob.pa/.org no devuelven resultados.
  - Bug de clave de ventana GDELT "actual" (ver arriba).
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
| 2026-07-27 | 0 (11 revisados, 11 falsos positivos) | 0 | Fix fetch_ddg_search (filtros domain/Panamá) + fix mark_ingested crash + diagnóstico con logs reales de Actions (GDELT bloqueado 2015-2017, RSS muerto, 7/8 DDG sin resultados) |

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
