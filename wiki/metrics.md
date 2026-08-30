---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-30
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 51 | ↑ continuo |
| Artículos reales ingestados | 10 (18 marcados − 8 falsos positivos) | = total sin falsos positivos |
| Falsos positivos acumulados | 8 | **0 nuevos** |
| Pendientes de ingesta | 33 | 0 |
| Páginas en wiki/ | 24 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla + backfill parcial) | 2015 → hoy real |
| Ventanas GDELT completadas | 76 / ~45 estimadas (posible duplicación) | 45 (2015→hoy) |
| Días sin artículos nuevos (Actions) | **3** ⚠️ | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida EXITOSA  : Run #93, 2026-08-27 20:51 UTC (sha 4908c54 → produjo 2e30165)
Corridas FALLIDAS       : Run #94 (2026-08-28), #95 (2026-08-29), #96 (2026-08-30)
Duración de las fallas  : 3-4 segundos cada una, SIN runner_id ni steps registrados
Tipo de falla           : startup_failure — el job nunca llegó a ejecutar checkout/pip/fetch
Causa NO es el código   : script de fetch, GDELT ni RSS no llegaron a correr
Causas probables        : cuota de minutos de GitHub Actions agotada, límite de
                          gasto en $0, o Actions restringido a nivel de repo/org
Acción requerida        : usuario debe revisar
                          https://github.com/settings/billing/summary y
                          Settings → Actions → General del repo `wiki_agro`
Log detallado           : ver wiki/log.md, entrada 2026-08-30 16:20

PROBLEMA SEPARADO — Falsos positivos por país mal etiquetado:
  Se detectaron artículos de Brasil (agenciabrasil.ebc.com.br), Mozambique
  (clubofmozambique.com) y Malasia (paultan.org) en sources/articles/, todos
  con source="prensa.com" y country="PA" incorrectamente asignados por el
  fetch. Esto indica que el clasificador de país/fuente del pipeline de fetch
  no está validando el dominio real del artículo. Recomendación: agregar
  validación de dominio contra una lista blanca de medios panameños antes de
  guardar en sources/articles/.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Recalculado el 2026-08-30 a partir de `sources/processed.json._gdelt_windows`
(76 ventanas registradas, agrupadas por año de inicio):

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 | 0/4 | ⚠️ **Pendiente — hueco real, nunca se ha corrido** |
| 2016 | 0/4 | ⚠️ **Pendiente — hueco real, nunca se ha corrido** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 | 40 | ⚠️ **Duplicación — ver nota abajo** |
| **TOTAL** | **76** | 2015-2016 sin cubrir; 2017-2025 completo |

> **Nota sobre 2026**: en vez de 1-2 ventanas trimestrales, hay 40 ventanas
> registradas para 2026, casi todas con inicio `20260618` y fin que avanza un
> día a la vez (ej. `20260618_20260623`, `20260618_20260624`, ...). Esto indica
> que el fetch diario está generando una ventana "nueva" cada día en vez de
> reutilizar o cerrar la ventana del período actual — desperdicia cupo de
> fetch que podría usarse para rellenar 2015-2016. Recomendación: revisar la
> lógica de generación de ventanas GDELT en el fetch diario (probablemente en
> `scripts/fetch` o equivalente) para que priorice huecos históricos (2015-2016)
> antes de generar ventanas del año en curso.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-30 | 4 (+1 falso positivo detectado y excluido) | 33 | Diagnóstico: Actions en falla 3 días consecutivos (startup_failure, revisar billing); hueco real 2015-2016 en GDELT; falsos positivos por país mal etiquetado (Brasil/Mozambique/Malasia) |

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
