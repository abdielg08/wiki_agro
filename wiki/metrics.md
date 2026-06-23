---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-06-23
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
| Ventanas GDELT completadas | 21 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 4+ (último: 2026-06-19) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-23 13:37–14:02 UTC
Resultado              : 0 artículos nuevos
Corridas recientes     : 2026-06-23, 2026-06-21, 2026-06-19, 2026-06-17... (cada 2 días)
Causas identificadas   :
  1. GDELT rate-limiting: ~50% de las ~46 ventanas reciben 403/429
     Las restantes devuelven 0 artículos relevantes sobre agro panameño
  2. DDG búsquedas: todas retornan "No results found" (posible bloqueo de IP del runner)
  3. RSS IICA y La Prensa: 0 entradas en ambos feeds
Estado del pipeline    : Actions corre correctamente cada 2 días pero sin yield de artículos
Recomendación          : Explorar scraping directo de mida.gob.pa, Google News RSS,
                         o curación manual de artículos históricos
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos GDELT | Estado |
|---------|----------|-----------------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | Parcial — varias ventanas rate-limited (403/429) |
| 2016 Q1-Q4 | 0/4 | 0 | Parcial — varias ventanas rate-limited |
| 2017 Q1-Q4 | 0/4 | 0 | Parcial — varias ventanas rate-limited |
| 2018 Q1-Q4 | 4/4 | 0 | Completado — 0 artículos agro panameño |
| 2019 Q1-Q4 | 4/4 | 0 | Completado — 0 artículos agro panameño |
| 2020 Q1-Q4 | 3/4 | 0 | Parcial — 1 ventana rate-limited |
| 2021 Q1-Q4 | 3/4 | 0 | Parcial — 1 ventana rate-limited |
| 2022 Q1-Q4 | 3/4 | 0 | Parcial — 1 ventana rate-limited |
| 2023 Q1-Q4 | 4/4 | 0 | Completado — 0 artículos agro panameño |
| 2024 Q1-Q4 | 3/4 | 0 | Parcial — 1 ventana rate-limited |
| 2025 Q1-Q4 | 2/4 | 0 | Parcial — 2 ventanas rate-limited |
| 2026 Q1-Q2 | 2/2 | 0 | Completado — 0 artículos agro panameño |
| **TOTAL** | **~21/46** | **0** | **GDELT no está rindiendo artículos reales** |

> **Diagnóstico crítico (2026-06-23)**: 21 ventanas completadas, todas con 0 artículos agropecuarios
> de Panamá. GDELT/DocSearch no indexa suficiente contenido de medios panameños en español.
> El backfill histórico real requiere una estrategia alternativa (ver Estado del Fetch).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-06-23 | 0 | 0 | Diagnóstico: GDELT rate-limit + DDG bloqueado + RSS vacíos; 21/46 ventanas completadas |

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
