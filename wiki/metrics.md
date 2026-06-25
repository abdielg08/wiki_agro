---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-06-25
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 13 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 36 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos (reales) | **6** (desde 2026-06-19) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-25 (múltiples commits "0 artículos nuevos descargados")
Resultado              : 0 artículos nuevos en últimas 3 corridas
Causa identificada     : GDELT queries no filtran suficientemente por Panamá;
                         "MIDA" devuelve artículos de Malaysian Investment Development Authority,
                         RSS devuelve worldbank.org genérico, IEEE, y medios de EEUU/Malasia.
                         36 ventanas GDELT completadas sin artículos agro-panameños reales.
Fix aplicado (anterior): fetch_gdelt_historical() limitado a datetime.utcnow()-1d — OK
Estado actual          : Actions corre correctamente pero con 0% artículos relevantes.
                         Último artículo real (no semilla): ninguno vía Actions hasta la fecha.
Acción requerida       : Mejorar queries GDELT/RSS con filtros geográficos estrictos:
                         - Añadir "Panama" obligatorio junto a términos agrícolas
                         - Considerar queries como "agricultura Panama", "MIDA gob pa",
                           "ganadería Panamá", "IDIAP Panama", en lugar de términos genéricos
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos reales | Estado |
|---------|----------|------------------|--------|
| 2017 Q1-Q2 | 1/4 | 0 | Parcial (falsos positivos) |
| 2018 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2019 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2020 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2021 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2022 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2023 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2024 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2025 Q1-Q4 | 4/4 | 0 | Completo (falsos positivos) |
| 2026 Q1-Q2 | 3/2 | 0 | Completo (falsos positivos) |
| 2015-2016 | 0/8 | 0 | Pendiente (no procesadas aún) |
| **TOTAL** | **36/46** | **0** | **36 ventanas procesadas, 0% artículos agro-panameños** |

> Problema estructural: queries GDELT no filtran por Panamá — 36 ventanas con 0 artículos reales.
> Las semillas (6 artículos) son reales pero fueron ingresadas manualmente, no vía Actions.
> Próximo paso: corregir queries de fetch para incluir filtros geográficos estrictos.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-06-25 | 0 | 0 | Diagnóstico: 36 ventanas GDELT procesadas, 0% artículos agro-panameños reales; queries no filtran Panamá |

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
