---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-21
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos ingestados (processed.json) | 30 | = total, 0 pendientes |
| Artículos reales en wiki (no falsos positivos) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 24 (7 previos + 17 hoy) | **0 nuevos** — en riesgo, ver diagnóstico |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 72 / ~45 estimadas | 45 (2015→hoy) — **excedido, ver nota** |
| Días sin artículos nuevos reales | ≥2 (2026-08-20, 2026-08-21: 0 nuevos; 2026-08-19: 1 nuevo pero falso positivo) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-21 (corre a diario, incl. 2026-08-20: 0 nuevos)
Resultado              : Actions SÍ corre regularmente, pero:
                         - Ventanas GDELT: 72 completadas (> 45 estimadas) →
                           rango de fechas agotado, backfill histórico
                           efectivamente estancado sin expansión de ventanas.
                         - Única fuente activa produciendo artículos "nuevos":
                           web_searches.prensa_agro (DDG site:prensa.com).
Causa identificada (2026-08-21) : fuente DDG "prensa.com" está ROTA —
  17/17 artículos pendientes evaluados hoy (100%) fueron falsos positivos:
  DDG no respeta el filtro `site:prensa.com`, el query permite coincidencia
  sin mención de Panamá (términos unidos con OR), y fetch_ddg_search()
  hardcodea source=prensa.com/country=PA/language=es sin validar el
  resultado real. Detalle completo en wiki/log.md (entrada 2026-08-21 16:45).
Fix aplicado            : Ninguno esta sesión (cambio de código fuera del
                          alcance de la routine automática) — documentado
                          como recomendación en wiki/log.md.
Estado                  : REQUIERE ACCIÓN DEL USUARIO — revisar
                          scripts/fetch_news.py::fetch_ddg_search() e
                          is_agro_relevant(), y config/sources.yaml
                          (web_searches.prensa_agro query).
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
| 2026-08-21 | 0 al wiki (17/17 falsos positivos) | 0 | Fuente DDG "prensa.com" identificada como rota (100% FP). Bugs de `mark-ingested`/`mark-all-ingested` documentados y evitados con workaround manual. Ver wiki/log.md. |

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
