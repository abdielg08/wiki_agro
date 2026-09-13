---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-13
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Pendientes de ingesta | 39 | 0 |
| Páginas en wiki/ | 26 (9 topics, 3 entidades, 11 resúmenes, 2 overview) | ↑ continuo |
| Cobertura temporal | 2015-2025 (histórico parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 / ~45 estimadas | 45+ (backfill 2015→hoy ~agotado) |
| Días sin artículos nuevos en sources/ | **7** (último commit real: 2026-09-06) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida exitosa (con push)  : 2026-09-06 13:56 UTC (run #103, "0 artículos nuevos")
Corridas consecutivas fallidas     : 7 (runs #104-#110, 2026-09-07 → 2026-09-13)
Duración de las corridas fallidas  : ~3-4 segundos (falla muy temprana, sin logs descargables)
Estado del workflow                : "active" (no deshabilitado por GitHub)
Causa identificada                 : No se pudo confirmar con certeza vía API — el patrón
                                      (fallo casi instantáneo, sin logs, "continue-on-error"
                                      en el step de fetch no debería producir failure del job)
                                      apunta a un problema de infraestructura/cuota de
                                      GitHub Actions en la cuenta (minutos agotados o límite
                                      de runners), no a un bug del script wiki_agro.py.
Acción requerida                   : El usuario debe revisar GitHub → Settings → Actions /
                                      Billing del repositorio abdielg08/wiki_agro, y probar
                                      un workflow_dispatch manual para confirmar si persiste.
Ventanas GDELT                     : 79 completadas, por encima del umbral de ~45 estimadas
                                      para 2015→hoy — el backfill histórico está prácticamente
                                      agotado; las ventanas recientes ya cubren 2026.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> El backfill ya superó las ~45-46 ventanas estimadas originalmente (79 completadas al
> 2026-09-13). El detalle trimestral no se reconstruyó en esta sesión porque
> `sources/processed.json` no almacena el desglose por año/trimestre, solo la lista plana de
> ventanas (`_gdelt_windows`). Pendiente para una sesión de mantenimiento: derivar la tabla
> real a partir de esa lista si se requiere trazabilidad trimestral.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-13 | 5 (0 falsos positivos) | 39 | Ingest de artículos de arroz/MIDA (2022-2025); diagnóstico: fetch diario de GitHub Actions lleva 7 corridas consecutivas fallidas (ver `wiki/log.md`) |

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

> **Esta alarma está activa desde el 2026-09-13** (7 días sin artículos nuevos, ver
> diagnóstico completo en `wiki/log.md`, entrada "DIAGNÓSTICO AVANZADO").
