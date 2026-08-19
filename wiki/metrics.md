---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** |
| Pendientes de ingesta (sin revisar) | 11 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal (contenido wiki) | 6 páginas semilla, años 2015-2024 dispersos | 2015-02-19 → hoy real |
| Cobertura temporal (raw fetch GDELT) | 2017-2026 completo; 2015-2016 sin datos (bloqueado) | 2015-02-19 → hoy real |
| Ventanas GDELT completadas | 70 (2017 Q1 → 2026 Q3 catch-up) | 2015 Q1 → hoy |
| Ventanas GDELT bloqueadas | 8/8 de 2015-2016 (403/429 persistente) | 0 |
| Días sin artículos nuevos | ~20 (desde 2026-07-30) | máx 3 antes de diagnosticar |

**🔴 ALARMA ACTIVA**: 20 días sin artículos nuevos reales — supera el umbral de 3 días. Ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-18 (run 32130922392) — status: success, 0 artículos guardados
Racha sin novedad       : 2026-08-01 → 2026-08-18, 20/20 corridas con "0 artículos nuevos"
Última corrida con datos: 2026-07-30 (3 artículos)

Causa identificada (diagnóstico 2026-08-19, ver wiki/log.md para detalle completo):
  1. GDELT: bloqueado en el 100% de las ventanas intentadas —
     "GET blocked (403/429): https://api.gdeltproject.org/api/v2/doc/doc"
     Afecta tanto los reintentos de 2015-2016 (nunca completados) como la
     ventana de catch-up 2026-06-18→hoy. NO es agotamiento de rango de fechas
     (70 ventanas ya completadas, por encima de las ~45 estimadas) — es
     bloqueo activo de la IP del runner de GitHub Actions.
  2. RSS: IICA y LaPrensaGeneral devuelven "0 entradas en el feed" en cada
     corrida — feeds vacíos o rotos, no solo sin noticias nuevas ese día.
  3. Búsqueda DDG: 6 de 7 queries fallan con "No results found" (oirsa,
     mida.gob.pa, idiap.gob.pa, bda.gob.pa, fao.org, bancomundial.org,
     iica.int) — ddgs también bloqueado/limitado desde el runner.
  4. World Bank API: corre sin error pero no aporta artículos nuevos.

Conclusión: las 3 fuentes de fetch están simultáneamente bloqueadas o vacías.
Requiere intervención humana (no resuelto en esta sesión — fuera de alcance
de una routine de ingesta): revisar bloqueo de IP en GDELT (posible necesidad
de proxy/rotación de user-agent) y validar manualmente si las URLs RSS de
IICA/La Prensa siguen vigentes.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | 🔴 Bloqueado (403/429 en cada intento) |
| 2016 Q1-Q4 | 0/4 | 🔴 Bloqueado (403/429 en cada intento) |
| 2017 Q1-Q4 | 4/4 | ✅ Completo |
| 2018 Q1-Q4 | 4/4 | ✅ Completo |
| 2019 Q1-Q4 | 4/4 | ✅ Completo |
| 2020 Q1-Q4 | 4/4 | ✅ Completo |
| 2021 Q1-Q4 | 4/4 | ✅ Completo |
| 2022 Q1-Q4 | 4/4 | ✅ Completo |
| 2023 Q1-Q4 | 4/4 | ✅ Completo |
| 2024 Q1-Q4 | 4/4 | ✅ Completo |
| 2025 Q1-Q4 | 4/4 | ✅ Completo |
| 2026 Q1 | 1/1 | ✅ Completo (20260319-20260617) |
| 2026-06-18 → hoy | ventana rolante diaria | 🔴 Bloqueado desde ~2026-08-01 |
| **TOTAL histórico** | **37/45 ventanas trimestrales** | **8 pendientes, todas 2015-2016** |

> Nota: las 33 "ventanas" adicionales que aparecen en `_gdelt_windows` para
> 2026 son reintentos diarios de la misma ventana rolante (20260618→fecha
> actual), no ventanas trimestrales nuevas — no se cuentan en el total.
> Prioridad de backfill: desbloquear GDELT para completar 2015-2016 (los
> únicos años con cobertura real 0%).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados (reales) | Falsos positivos rechazados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-19 | 0 | 5 | 11 | Falsos positivos MIDA-Malasia/Utah (bug en fetch_ddg_search, ver log.md) + diagnóstico de fetch caído (GDELT bloqueado, RSS vacío, DDG bloqueado) desde 2026-07-30 |

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
