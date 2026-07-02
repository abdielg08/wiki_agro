---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-02
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados (detectados y descartados) | 13 | 0% terminan en el wiki (meta cumplida) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 43 / ~45 estimadas | 45 (2015→hoy) |
| Días sin artículos nuevos | 0 (última corrida: 2026-07-02) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-02 — OK, 1 artículo nuevo descargado
Resultado               : Backfill GDELT avanzando: 43/46 ventanas completadas
Problema detectado hoy  : 6/6 artículos pendientes de esta sesión eran falsos
                          positivos (web_search "prensa_agro" sin verificar
                          dominio real ni exigir mención de Panamá — ver
                          wiki/log.md 2026-07-02)
Fix aplicado            : scripts/fetch_news.py fetch_ddg_search() ahora exige
                          coincidencia de dominio con `site:` y
                          _is_panama_related(title, url), igual que RSS/GDELT
Estado post-fix         : Pendiente validación en próxima corrida Actions
Cobertura GDELT pendiente: 2015 completo, 2016 completo, y 2017-Q1 (hasta
                          2017-03-29) — el resto (2017-Q2 → 2026) ya está cubierto
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 completo | 0/4 | Pendiente |
| 2016 completo | 0/4 | Pendiente |
| 2017 Q1 (hasta 03-29) | 0/1 | Pendiente |
| 2017-03-30 → 2026-06-17 | 36/36 | Completo (ventanas trimestrales) |
| 2026-06-18 → 2026-07-01 | 6/6 | Completo (ventanas diarias de alcance) |
| **TOTAL** | **43/~46** | **Falta 2015, 2016 y ene-mar 2017** |

> Ventanas reales según `sources/processed.json._gdelt_windows` (2026-07-02).
> El backfill histórico más antiguo (2015–inicio 2017) sigue sin cubrirse — GDELT
> puede estar limitando resultados muy antiguos o el fetch aún no ha llegado a esas
> fechas. Próxima sesión: verificar por qué las ventanas de 2015-2016 no se han
> generado (revisar `fetch_gdelt_historical()` en scripts/fetch_historical.py).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-02 | 0 | 0 | 6/6 pendientes eran falsos positivos (bug en fetch_ddg_search — corregido); GDELT en 43/46 ventanas |

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
