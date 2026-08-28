---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-28
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos ingestados (total, incl. falsos positivos marcados) | 18 | = total sin falsos positivos |
| Artículos pendientes de ingesta | 33 | 0 |
| Falsos positivos acumulados | 8 | **0 nuevos hoy** (1 detectado y documentado esta sesión) |
| Páginas en wiki/ | 24 (8 topics, 3 entidades, 10 resúmenes, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 | 45+ ya alcanzado — rango agotado, necesita expansión |
| Días sin artículos nuevos | 0 (último fetch: 2026-08-27, +1 artículo) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-27 (commit 2e30165, "1 artículos nuevos descargados")
Resultado               : Fetch está funcionando (no hay 3+ días consecutivos sin nuevos artículos)
Ritmo reciente          : irregular — varias corridas con 0 nuevos, una con 20, la más
                          reciente con 1. Volumen bajo respecto a la meta de ~15/día.
Ventanas GDELT          : 76 completadas — supera el estimado original de ~45.
                          El rango de fechas cubierto por GDELT parece agotado o cerca
                          de agotarse; probablemente necesita expandirse el rango objetivo
                          o revisar por qué tantas ventanas devuelven pocos/0 artículos.
Falso positivo detectado: 1 artículo indexado como "prensa.com" pero originario de
                          paultan.org (medio automotriz de Malasia), colado por
                          coincidencia de sigla "MIDA" (Malasia vs. Panamá).
                          Ver wiki/log.md 2026-08-28 y recomendación de endurecer
                          el fetcher para validar dominio real vs. campo "source".
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | **0/4** | ⚠️ **Sin cobertura — nunca se generaron ventanas GDELT para 2015** |
| 2016 Q1-Q4 | **0/4** | ⚠️ **Sin cobertura — nunca se generaron ventanas GDELT para 2016** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 Q1 | 1/1 | Completo |
| 2026 Q2 | **39** (esperado 1) | ⚠️ **Anómalo — 39 ventanas registradas para un solo trimestre, probable bug de generación duplicada/reintento** |
| **TOTAL** | **76** | Ver hallazgos abajo |

### Hallazgos del diagnóstico (2026-08-28)

1. **2015 y 2016 sin cobertura GDELT**: la meta declarada en CLAUDE.md es "2015-02-19 → hoy", pero `_gdelt_windows` en `sources/processed.json` no contiene ninguna ventana para esos dos años. Los artículos semilla de 2016 en el wiki (p. ej. sequía Azuero) fueron cargados manualmente, no vía fetch GDELT. **Acción recomendada**: revisar `fetch_gdelt_historical()` — probablemente el rango de inicio configurado no llega hasta 2015-02-19, o esas ventanas fallaron silenciosamente y nunca se reintentaron.
2. **2026 Q2 con 39 ventanas** (vs. 1 esperada): sugiere que el generador de ventanas para el trimestre en curso se está reejecutando y registrando entradas nuevas cada corrida en vez de reutilizar/consolidar la ventana del período. **Acción recomendada**: revisar la lógica que genera ventanas para el trimestre actual (parcial/en curso) en el script de fetch.
3. 2017-2025 están completos a nivel de ventanas (1 ventana ≈ 1 trimestre), lo cual es consistente con el conteo total de 76 ventanas (10 años × 4 + 1 + 1 + 39 - ajustes ≈ 76... revisar breakdown exacto en processed.json si se requiere auditoría fina).

> Nota: el conteo de "artículos por ventana" no está expuesto directamente en `processed.json`; solo se registra si la ventana fue completada. Para depurar el volumen bajo de ingesta reciente, sería útil que el fetcher registre también cuántos artículos devolvió cada ventana.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-28 | 5 (4 reales + 1 falso positivo) | 33 | Routine automática; arroz/maíz/ganadería/inundaciones/transición MIDA; 1 falso positivo (Malasia) documentado |

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
