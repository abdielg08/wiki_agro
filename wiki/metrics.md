---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-13
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 | **0 nuevos ingestados al wiki** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 36/46 trimestrales + 12 de alcance | 46 (2015→hoy), sin brechas |
| Días sin artículos nuevos | **3 — ⚠ FALLO** | máx 3 antes de diagnosticar |

**⚠ Alerta activa**: 3 días consecutivos sin commits nuevos en `sources/`
(último: 2026-07-10). Ver diagnóstico completo en `wiki/log.md`
(entrada 2026-07-13 16:20) — el workflow `wiki_daily.yml` parece haber
dejado de ejecutarse o de commitear. Requiere revisión del usuario en
GitHub Actions.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con commit  : 2026-07-10 (1 artículo, resultó ser falso positivo)
Días sin commit en sources/: 3 (2026-07-11, 12, 13) — umbral de fallo alcanzado
Causa identificada hoy      : fetch_ddg_search() no aplicaba el filtro "site:"
                              de forma confiable (DDGS news search lo ignora),
                              devolviendo noticias globales no relacionadas con
                              Panamá bajo la etiqueta de fuente "prensa.com".
                              12 de los últimos 14 artículos de esa fuente eran
                              falsos positivos (ver wiki/log.md).
Fix aplicado                : scripts/fetch_news.py — fetch_ddg_search() ahora
                              descarta resultados cuyo dominio no coincida con
                              el "site" configurado, antes del filtro de
                              keywords. scripts/ingest.py — mark_ingested()
                              corregido (crasheaba con _gdelt_windows).
Pendiente de validar        : próxima corrida de wiki_daily.yml (aún no ha
                              corrido desde el fix)
Pendiente de investigar     : por qué wiki_daily.yml no ha generado commits
                              desde 2026-07-10 (revisar Actions run history)
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
| 2026-07-13 | 0 (7 rechazados como falsos positivos) | 0 | Fix de causa raíz (fetch_ddg_search sin filtro site: real) + fix mark_ingested() + alerta de 3 días sin fetch |

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
