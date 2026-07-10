---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-10
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 47 / ~45-46 estimadas | 45-46 (2015→hoy) — **rango agotado** |
| Días sin artículos nuevos (reales) | 8 (desde 2026-07-02) | máx 3 antes de diagnosticar — **⚠ ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-09 (completed/success — el workflow SÍ corre bien)
Resultado               : 0 artículos nuevos reales desde 2026-07-02 (8 días)
Causa identificada       :
  1. GDELT: 47 ventanas completadas (≥45 estimadas) → rango histórico
     2015-2027 agotado. No debe esperarse más contenido nuevo de GDELT
     sin expandir config/sources.yaml → gdelt.date_range.
  2. web_search "prensa_agro" (site: prensa.com, query con "MIDA" OR
     "agricultura" sin exigir "Panamá"): está devolviendo resultados de
     dominios ajenos a prensa.com (sltrib.com, spa.gov.sa, nyfb.org) y
     guardándolos con source="prensa.com". Confirmado el 2026-07-10:
     6/6 artículos pendientes eran falsos positivos, todos por colisión
     del acrónimo "MIDA" (Utah: Military Installation Development
     Authority) o por temas agrícolas de otros países.
Fix aplicado esta sesión : ninguno al pipeline de fetch (fuera de alcance
                            de la rutina); solo bugfix de
                            scripts/ingest.py::mark_ingested (ver log.md).
Pendiente para próxima sesión de mantenimiento:
  - Auditar por qué resultados fuera de site:prensa.com se etiquetan como
    fuente "prensa.com" (revisar función de web_search / ddgs en scripts/).
  - Excluir "MIDA" como término aislado; exigir "Panamá" en la misma
    consulta o en el resultado.
  - Decidir si expandir gdelt.date_range o declarar cerrado el backfill
    GDELT y depender solo de RSS/web_search seguros para adelante.
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
| **TOTAL** | **47/46** | **~6 reales (13 falsos positivos)** | **Ventanas agotadas — backfill de fechas completo, pero rendimiento pésimo (~13% señal)** |

> Ventanas GDELT completadas = 47 (`sources/processed.json → _gdelt_windows`), cubriendo
> ya todo el rango 2015-01-01 → 2027-12-31 configurado. El desglose por trimestre no está
> instrumentado en el script (las ventanas se guardan como rangos de fecha sueltos, no
> etiquetadas por período); pendiente de un script de mantenimiento que lo calcule si se
> necesita el detalle por trimestre. Lo urgente no es más ventanas GDELT — es la altísima
> tasa de falsos positivos del web_search (ver "Estado del Fetch" arriba).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-10 | 0 (6 falsos positivos rechazados) | 0 | 0% ingesta real; GDELT agotado (47 ventanas); alarma: 8 días sin artículos reales; bugfix mark_ingested |

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
