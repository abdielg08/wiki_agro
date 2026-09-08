---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-09-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 57 | ↑ continuo |
| Artículos reales ingestados | 18 | = total sin falsos positivos |
| Pendientes de ingesta | 39 | 0 |
| Falsos positivos acumulados (lote actual) | 0 nuevos | **0 nuevos** |
| Páginas en wiki/ | 27 (10 topics, 3 entidades, 11 resúmenes, resto overview) | ↑ continuo |
| Cobertura temporal real (sources/) | ~2017-03 → 2026-06 | 2015-02-19 → hoy |
| Ventanas GDELT en processed.json | 79 (~35 backfill histórico + ~44 ventana incremental duplicada) | 45 (2015→hoy), sin duplicados |
| Días sin artículos nuevos | 2 (último fetch con resultados: 2026-09-06) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-09-06 (+6 artículos)
Corridas recientes (sources/)       : 09-06(+6) 09-04(0) 09-03(0) 09-01(0) 08-27(+1) 08-24(+20)
Resultado                           : Fetch activo, no en falla (2 días sin nuevos, < umbral de 3)
Diagnóstico ventanas GDELT          : 79 ventanas registradas en processed.json
                                       - ~35 ventanas de backfill histórico (2017-03 → 2026-06)
                                       - ~44 ventanas con prefijo fijo "20260618_" y fin variable día a día:
                                         patrón de ventana "incremental" (últimos ~90 días) que se re-registra
                                         en cada corrida en vez de consolidarse en una sola entrada
Causa identificada                  : (1) backfill histórico aún no llega a 2015-02-19 — arranca en 2017-03,
                                         faltan 2015-2016 completos
                                       (2) el conteo de "ventanas completadas" (79) está inflado por duplicados
                                         de la ventana incremental — no es una señal limpia de agotamiento
Fuentes RSS (IICA, La Prensa)       : activas, siguen aportando artículos (prensa.com = 51/57 del total)
Fix recomendado (no aplicado)       : revisar generación de ventanas incrementales en el script de fetch para
                                         que actualice/reemplace la ventana existente en vez de crear una nueva
                                         cada corrida; y reanudar backfill histórico desde 2015-02-19
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
| 2026-09-08 | 5 (0 falsos positivos) | 39 | Lote de arroz/MIDA (2022, 2024×3, 2025); creó topics/precios_mercados.md y topics/subsidios_programas.md (enlaces rotos preexistentes en index.md) |

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
