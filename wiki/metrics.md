---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** (regla innegociable — ver nota abajo) |
| Pendientes de ingesta | 12 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 70 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, ver diagnóstico** |
| Días sin artículos nuevos | 1 (último: 2026-08-19, 1 artículo) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con resultado : 2026-08-19 (commit e9d45e6) → 1 artículo nuevo
Corridas previas              : 9 de las últimas 10 corridas revisadas devolvieron 0 artículos
Resultado de esta sesión      : 5 artículos revisados de pending_ingest.md → 0 ingestados,
                                 5 falsos positivos (0% tasa de aceptación)

Causa raíz identificada (2026-08-20):
  El query GDELT usa `sourcecountry:PA` (scripts/fetch_historical.py:73) para filtrar
  por país de origen. En FIPS 10-4 (el estándar que usa GDELT para sourcecountry),
  el código "PA" corresponde a Paraguay, no a Panamá — el código FIPS de Panamá
  es "PM". Esto sugiere que el filtro de país probablemente NO está limitando los
  resultados a medios panameños, y la búsqueda cae de vuelta a los términos genéricos
  de la query ("MIDA", "cosecha", "cultivo", etc.), que colisionan con acrónimos y
  palabras homónimas de otros países (Malaysian Investment Development Authority,
  Utah Military Installation Development Authority, agro de Aragón/España, etc.).
  Esto es consistente con el patrón observado: los 5 artículos revisados hoy y los
  7 falsos positivos previos (12 en total) mencionan 0 veces "Panamá" en su texto
  completo.

  Ventanas GDELT completadas (70) también superan el umbral de ~45 estimadas para
  2015→hoy — el rango de fechas configurado puede estar agotado o mal calculado.

Recomendación (NO aplicada aún — requiere confirmación del usuario, fuera del
alcance de una routine de ingesta):
  1. Corregir sourcecountry:PA → sourcecountry:PM en fetch_gdelt_window()
     (scripts/fetch_historical.py:73)
  2. Revisar el cálculo de ventanas trimestrales dado que ya hay 70 registradas
     vs. ~45 esperadas
  3. Agregar un filtro post-fetch que descarte artículos sin mención de "Panamá"
     en el texto antes de agregarlos a pending_ingest, como red de seguridad
     adicional al filtro de país
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
| 2026-08-20 | 0 (5 revisados, 5 falsos positivos) | 12 | Causa raíz identificada: posible bug `sourcecountry:PA` vs `PM` en GDELT — ver "Estado del Fetch" |

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
