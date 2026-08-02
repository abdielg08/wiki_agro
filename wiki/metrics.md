---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-02
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
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 60 / ~45 estimadas | 45 (2015→hoy) — ver nota |
| Días sin artículos nuevos | 3 (desde 2026-07-30) | máx 3 antes de diagnosticar — **ALARMA** |

> Nota sobre ventanas GDELT: aunque 60 ≥ 45, la cobertura real está
> incompleta — 2015 y 2016 tienen 0 ventanas completadas; las 24 ventanas
> de 2026 son redundantes (ventana rodante que se re-extiende cada día).
> Ver diagnóstico en `wiki/log.md` (2026-08-02 00:15).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit en sources/ : 2026-07-31 (0 artículos nuevos)
Última corrida con artículos nuevos   : 2026-07-30 (3 artículos)
Sin commits de sources/ en 2026-08-01 ni 2026-08-02 (a la hora de esta sesión)
Resultado sesión 2026-08-02           : 5 artículos revisados, 5/5 falsos
                                         positivos (colisión sigla "MIDA"
                                         con Malaysia/Utah) — 0 ingestados
Causa identificada     : el fetch automático quedó atascado desde 2026-06-18
                         re-extendiendo una ventana GDELT "reciente" en vez
                         de avanzar el backfill histórico hacia 2015-2016
                         (0 ventanas completadas en esos dos años). La
                         ventana reciente trae ruido internacional sin
                         relación con Panamá.
Fix aplicado           : ninguno en esta sesión (diagnóstico documentado en
                         wiki/log.md; requiere cambio en la lógica de
                         selección de ventana del script de fetch)
Estado                 : Pendiente de fix en scripts/ (fuera de alcance de
                         esta sesión de routine — solo diagnóstico)
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
| 2026-08-02 | 0 (5/5 revisados = falsos positivos) | 11 | Colisión sigla "MIDA" (Malasia/Utah); corregido bug de mark-all-ingested vs ingest --limit (orden distinto); diagnosticado backfill 2015-2016 estancado |

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
