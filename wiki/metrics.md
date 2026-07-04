---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-04
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (7 previos + 6 nuevos 2026-07-04) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 / 47 estimadas | 47 (2015→2026-07-03) |
| Días sin artículos nuevos | 2 (2026-07-03, 2026-07-04) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-04 (corrió correctamente, 0 artículos nuevos)
Resultado              : 0 artículos nuevos los últimos 2 días (07-03, 07-04)
                         1 artículo nuevo el 07-02, 1 el 06-29
Causa identificada     : NO es una falla — el backfill GDELT (2015→hoy) está
                         prácticamente agotado: 45/47 ventanas trimestrales
                         completadas (fetch_gdelt_historical usa end =
                         min(config_end=2027-12-31, utcnow()-1d), por lo que
                         la ventana final avanza sola cada día — no requiere
                         expansión manual de config/sources.yaml).
                         El bajo volumen reciente (0-1 art/día) es esperado:
                         quedan ~2 ventanas GDELT por completar y las fuentes
                         RSS activas (IICA, La Prensa) publican agro-Panamá
                         con poca frecuencia.
Riesgo detectado        : el fetch de prensa.com (RSS/GDELT genérico) sigue
                         capturando falsos positivos por colisión de la
                         palabra "MIDA" con entidades no panameñas (Military
                         Installation Development Authority, Utah, EE.UU.) y
                         por coincidencias genéricas de "agriculture" (ej.
                         programa "Reef Saudi" de Arabia Saudita). Ver
                         wiki/log.md 2026-07-04 para detalle — 6/6 artículos
                         pendientes de esta sesión fueron falsos positivos.
Fix aplicado (previo)   : fetch_gdelt_historical() limita end a datetime.utcnow()-1d
Fix aplicado (hoy)      : bug en scripts/ingest.py mark_ingested() — iteraba
                         processed.items() sin filtrar la clave interna
                         "_gdelt_windows" (una lista), causando AttributeError
                         en cada llamada. Corregido para usar article_entries().
Recomendación pendiente : evaluar si vale la pena filtrar dominios no
                         panameños (sltrib.com, nyfb.org, thestar.com.my,
                         spa.gov.sa) o exigir "Panamá"/"Panama" en el texto
                         del fetch de prensa.com para bajar la tasa de
                         falsos positivos futuros.
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
| 2026-07-04 | 0 | 0 | 6/6 pendientes eran falsos positivos (colisión "MIDA"/"agriculture" genérico) — 0 ingestados, 0% falsos positivos ingestados al wiki. Fix de bug en `mark_ingested()` (scripts/ingest.py). |

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
