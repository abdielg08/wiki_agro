---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos ingestados (total, incl. falsos positivos documentados) | 24 | = total sin pendientes |
| Artículos reales ingestados al wiki | 12 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (7 previos + 5 esta sesión) | **0 nuevos ingestados al contenido del wiki** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 26 | ↑ continuo |
| Cobertura temporal | 2007–2026 (mezcla semilla + fetch real) | 2015 → hoy real |
| Ventanas GDELT completadas | 79 | ~45+ (2015→hoy; ya superado el estimado original) |
| Días sin artículos nuevos (fetch automático) | **12** (última corrida exitosa: 2026-09-06) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA  : 2026-09-06 (run #103), commit "6 artículos nuevos descargados"
Corridas fallidas       : #104-#114, 2026-09-07 → 2026-09-17 (11 corridas diarias
                          programadas consecutivas, TODAS conclusion=failure)
Duración de cada falla  : 3-6 segundos (insuficiente para pip install; el job nunca
                          llegó a ejecutar sus steps — falla en "Set up job")
Causa identificada      : logs de job no disponibles (404), consistente con un job
                          que nunca inició. Hipótesis más probable: límite de gasto/
                          cuota de GitHub Actions alcanzado en la cuenta/repositorio.
Acción requerida        : el propietario (abdielg08) debe revisar GitHub → Settings →
                          Billing → Actions (o Settings → Actions → General) y
                          restablecer/ampliar el límite de gasto.
Detalle completo        : ver wiki/log.md, entrada "2026-09-18 09:15"
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Estado real verificado en `sources/processed.json` → `_gdelt_windows` (2026-09-18): **79 ventanas** registradas, de dos tipos distintos:

- **37 ventanas históricas trimestrales contiguas**, cubriendo `2017-03-30 → 2026-06-17` (formato `YYYYMMDD_YYYYMMDD` secuencial, ~90 días cada una).
- **42 ventanas "diarias"** con inicio fijo `20260618` y fin variable (una nueva por cada corrida diaria exitosa desde esa fecha) — estas son el mecanismo de fetch incremental, no backfill histórico, y no deben sumarse al conteo de progreso del backfill.

**Cobertura histórica real**: `2017-03-30 → hoy`. **Brecha pendiente**: `2015-02-19 → 2017-03-29` (~2 años, ~8 ventanas trimestrales) aún sin cubrir por el backfill histórico — falta ejecutar `wiki_historical.yml` (workflow manual) para ese rango, p. ej. `years: 2015-2017`.

> Nota: la meta original de "45 ventanas" en este archivo asumía trimestres calendario
> (2015 Q1 → 2026 Q2 = 46). El backfill real usa ventanas móviles de ~90 días, por lo
> que el conteo no es 1:1 comparable, pero la brecha 2015-2017 sigue siendo válida.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-09-18 | 6 reales + 5 falsos positivos documentados | 33 | Fix de 2 bugs en scripts/ingest.py (mark_ingested crash + desincronización mark_all_ingested/ingest); diagnóstico: fetch Actions sin corridas exitosas desde 2026-09-06 (ver "Estado del Fetch") |

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
