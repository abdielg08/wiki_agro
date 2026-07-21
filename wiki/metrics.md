---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-02 → 2026-07 (backfill al día) | 2015 → hoy real |
| Ventanas GDELT completadas | 51 / ~47 estimadas (2015→hoy) | al día, capado a utcnow()-1d |
| Días sin artículos nuevos | 0 (último commit sources/: 2026-07-20) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-20 (2 artículos)
Estado GDELT backfill               : AL DÍA — 51 ventanas completadas cubren
                                       2015-01-01 → hoy (config end=2027-12-31,
                                       capado en código a utcnow()-1d). El umbral
                                       de "45+ ventanas = rango agotado" de CLAUDE.md
                                       era una estimación de referencia, no un techo
                                       real: el fetch sigue avanzando cada ~90 días
                                       según pasa el tiempo. No requiere intervención.
Causa de 0 ingestas reales hoy      : de los 11 artículos pendientes revisados en
                                       esta sesión, 11/11 fueron falsos positivos
                                       (colisión de keywords "MIDA"/"agricultura" sin
                                       contexto Panamá, vía el fetcher DDG con filtro
                                       site: no confiable) — ver wiki/log.md 2026-07-21.
Fix aplicado esta sesión            : scripts/fetch_news.py — has_panama_context()
                                       ahora exige mención explícita de Panamá en
                                       resultados del fetcher DDG. Bugs de
                                       mark-ingested / mark-all-ingested corregidos
                                       en scripts/ingest.py (ver log).
Estado post-fix                     : Pendiente validación en próxima corrida Actions
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Recalculado directamente de `sources/processed.json:_gdelt_windows` (51 ventanas) el
2026-07-21:

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | **0** | ⚠️ Sin cubrir — ver diagnóstico abajo |
| 2016 | **0** | ⚠️ Sin cubrir — ver diagnóstico abajo |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 (a la fecha) | 15 (fragmentadas, ver nota) | En progreso, avanzando a diario |
| **TOTAL** | **51** | — |

**⚠️ Diagnóstico abierto (para próxima sesión) — dos anomalías detectadas al auditar
`_gdelt_windows` esta sesión:**
1. **2015 y 2016 tienen 0 ventanas completadas**, pese a que `fetch_gdelt_historical()`
   siempre empieza su recorrido en `date_range.start = 2015-01-01` y solo salta
   ventanas ya presentes en `completed_windows`. Como el primer año con ventanas
   completas es 2017, algo impide que las 8 ventanas de 2015–2016 lleguen a
   completarse (network error repetido → `batch is None` → nunca se marcan
   "completas" y se reintentan cada corrida sin avanzar; o un `date_range.start`
   distinto estuvo vigente en corridas pasadas). Esto es exactamente el rango que
   `CLAUDE.md` marca como objetivo (`2015-02-19 → hoy`), así que este hueco debe
   cerrarse antes de dar el backfill por completo.
2. **Las ventanas de "2026" no son trimestres limpios**: 15 entradas, todas con el
   mismo inicio (`20260618`) y fin creciente día a día (`20260628` … `20260718`).
   Esto sugiere que, cerca del borde `hoy-1`, el cálculo `next_q = min(current+90d,
   end)` genera una ventana distinta cada día (porque `end` avanza a diario) que
   nunca coincide con una ventana previa — así que se re-consulta casi el mismo
   rango de fechas cada día en vez de avanzar limpiamente. Explica el patrón de
   "0-1 artículos nuevos" en la mayoría de corridas diarias recientes. No es
   bloqueante (sigue trayendo noticias recientes) pero es ineficiente y vale la pena
   revisar la lógica de ventana final en `fetch_gdelt_historical()`.

> Próxima sesión: revisar logs de Actions de las primeras corridas post-reset
> (2026-06-22 en adelante) para confirmar si 2015-2016 fallan por error de red o por
> un `date_range.start` distinto, y considerar una ventana final de tamaño fijo
> (en vez de recalcular contra `utcnow()-1d` cada día) para evitar la fragmentación
> de 2026.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-21 | 0 reales / 11 revisados | 0 | 11/11 falsos positivos (colisión MIDA/agricultura sin contexto Panamá vía DDG). Fix de raíz aplicado (`has_panama_context`) + 2 bugs corregidos en mark-ingested/mark-all-ingested |

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
