---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-03
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 17 | **0 nuevos** (esta sesión: +10, ver log.md) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 61 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos | 4 (desde 2026-07-30) | máx 3 antes de diagnosticar → **⚠ excedido** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-30 (3 artículos)
Corridas posteriores                : 2026-07-31 (0), 2026-08-02 (0) — sin commit el 2026-08-01
Resultado hoy (2026-08-03)          : sin corrida de Actions registrada aún en sources/
Causa identificada     : Ventanas GDELT completadas = 61, por encima del umbral de 45
                         que CLAUDE.md marca como "rango de fechas agotado". El backfill
                         2015→hoy probablemente ya cubrió las ventanas disponibles y
                         necesita expansión (ventanas más finas o nuevo rango).
                         Adicionalmente, de los 11 artículos revisados en esta sesión
                         (2 lotes de 5, vía RSS/GDELT etiquetados fuente "prensa.com"),
                         10/10 fueron falsos positivos: noticias agropecuarias o
                         menciones de "MIDA" de otros países (España/Aragón, EE.UU./Utah,
                         Brasil, Arabia Saudita, Irán) sin relación con Panamá. Esto indica
                         que el scoring/fetch no está filtrando por relevancia geográfica
                         a Panamá — ver detalle y recomendaciones en wiki/log.md
                         (entradas 2026-08-03 08:04 y 08:35).
Fix aplicado           : fetch_gdelt_historical() ahora limita end a datetime.utcnow()-1d
                         Ventanas GDELT reseteadas a [] para backfill real (aplicado 2026-06-22)
Estado post-fix        : Validado — GDELT corrió y completó 61 ventanas, pero el
                         resultado real (0-3 artículos Panamá-relevantes por corrida,
                         mayoría falsos positivos) muestra que el filtro geográfico es
                         insuficiente. Pendiente: ajustar queries GDELT/scoring para
                         exigir co-ocurrencia con "Panamá" y expandir/refinar ventanas.
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
| 2026-08-03 | 0 reales (10 revisados, 10 falsos positivos) | 6 | 2 lotes de 5 revisados, 100% falsos positivos (colisión "MIDA" + noticias agro de otros países). Corregido bug de `mark-all-ingested --limit` (marcaba artículos no revisados) y crash de `mark-ingested`. Ventanas GDELT en 61/45 — rango agotado. 4 días sin artículos nuevos desde 2026-07-30. |

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
