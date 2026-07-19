---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** (9 detectados y rechazados hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 trimestres limpios / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 4 (desde 2026-07-15) | máx 3 antes de diagnosticar → **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con push  : 2026-07-18 (0 artículos nuevos)
Última corrida con datos : 2026-07-15 (1 artículo nuevo)
Sin commits en sources/  : 2026-07-16, 2026-07-17 (Actions no corrió o no hubo push)
Días sin nuevos           : 4 → excede umbral de 3 (CLAUDE.md) → señal de alarma

Causas identificadas hoy (sesión 2026-07-19):
  1. Bug de re-marcado diario en fetch_gdelt_historical(): la ventana
     trimestral en curso se re-marcaba como "completada" bajo una clave
     nueva cada día (13 entradas duplicadas de 2026-06-18 en _gdelt_windows)
     → CORREGIDO en scripts/fetch_news.py (solo se marca completa una
     ventana de ≥90 días; la parcial se re-consulta sin ensuciar el registro)
  2. Faltan por completo 9 trimestres del backfill histórico: 2015 Q1–Q4,
     2016 Q1–Q4, 2017 Q1 (2015-01-01 → 2017-03-29) — nunca aparecen en
     _gdelt_windows, ni como error ni como éxito. Causa raíz no confirmada
     (sin acceso de red saliente a GDELT desde este entorno para
     reproducir) — pendiente revisar logs reales de GitHub Actions.
  3. mark_ingested() en scripts/ingest.py crasheaba con AttributeError al
     iterar la clave interna _gdelt_windows sin filtrar → CORREGIDO
     (usa article_entries()).
  4. mark_all_ingested() usaba un orden de selección (alfabético por
     nombre de archivo) distinto al de ingest/run_prepare() (por score de
     relevancia), pudiendo marcar como ingestados artículos que Claude
     Code nunca revisó → CORREGIDO (ahora usa el mismo prioritize()).
Estado post-fix          : Pendiente validación en próxima corrida Actions
                            (2026-07-16 y 2026-07-17 sin explicación aún —
                            requiere revisar logs del workflow)
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | ? | **Faltante — nunca completado, causa por confirmar** |
| 2016 Q1-Q4 | 0/4 | ? | **Faltante — nunca completado, causa por confirmar** |
| 2017 Q1 | 0/1 | ? | **Faltante — nunca completado, causa por confirmar** |
| 2017 Q2-Q4 | 3/3 | ver sources/ | Completo |
| 2018 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2019 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2020 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2021 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2022 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2023 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2024 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2025 Q1-Q4 | 4/4 | ver sources/ | Completo |
| 2026 Q1-Q2 | 2/2 | ver sources/ | Completo |
| 2026 Q3 (parcial, hasta 2026-07-17) | en curso | ver sources/ | Se re-consulta a diario (ver fix del 2026-07-19) |
| **TOTAL** | **37/46 trimestres completos** | — | **9 trimestres faltantes (2015-01-01 → 2017-03-29)** |

> Conteo real extraído de `sources/processed.json` → `_gdelt_windows` el 2026-07-19.
> El artículo-count por trimestre no se registra por ventana; ver `sources/articles/` para el detalle.
> PRÓXIMO PASO: investigar por qué 2015 Q1–2017 Q1 nunca se completan (posible rate-limit
> de GDELT para rangos muy antiguos, o error silencioso) — requiere logs reales de Actions.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-19 | 0 (9/9 revisados eran falsos positivos) | 0 | Colisión de sigla "MIDA" (Malasia/Utah, no Panamá); fix de 3 bugs de código (re-marcado diario GDELT, mark_ingested crash, mark_all_ingested orden incorrecto); diagnóstico de 9 trimestres GDELT faltantes (2015–2017 Q1) y 4 días sin artículos nuevos |

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
