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
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos** ⚠️ 7 nuevos hoy |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~46 estimadas | 45 (2015→hoy) — **rango agotado** |
| Días sin artículos reales nuevos | — (sin dato histórico) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-10 13:11 UTC — SÍ corrió hoy
Resultado               : 1 artículo descargado, 0 artículos reales (falso positivo)
Causa raíz confirmada   : fetch_ddg_search() en scripts/fetch_news.py (línea 244) usa
                          `site:{site} {query}` con DDGS().news() — el operador site:
                          no restringe confiablemente el dominio, y el único filtro
                          aplicado es is_agro_relevant() (exige término agro, NO exige
                          Panamá). A diferencia de fetch_gdelt_historical(), que sí
                          exige Panamá (_gdelt_query_string + _is_panama_related),
                          fetch_ddg_search() nunca llama _is_panama_related().
                          Además `source` se asigna desde la config (p.ej. "prensa.com"),
                          no desde el dominio real de la URL devuelta.
Impacto                 : 7 falsos positivos ingresados por esta vía en el último mes
                          (ver wiki/log.md 2026-07-10 para el detalle y el fix sugerido).
GDELT windows           : 48 ventanas completadas (>45) → el rango histórico 2015→hoy
                          ya fue recorrido por GDELT; necesita expansión de ventanas
                          o confirmación de que 2015-2026 quedó realmente cubierto.
Fix sugerido (pendiente): aplicar _is_panama_related(title, url) en fetch_ddg_search()
                          y derivar `source` del dominio real de la URL, no de config.
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
| 2026-07-10 | 0 reales (7 falsos positivos descartados) | 0 | Root-cause: fetch_ddg_search() no exige Panamá, solo agro-término. Ver log.md |

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
