---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-05
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 19 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 13 (6 hoy: 5 sobre Utah/MIDA-EE.UU. + 1 sobre Arabia Saudita) | **0 nuevos** (fix aplicado hoy, ver diagnóstico) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (solo semilla manual — 0 artículos reales por fetch automático) | 2015 → hoy real |
| Ventanas GDELT completadas | 45 (2017-2025 completos; 2015-2016 **no iniciados**) | ~53 (2015→hoy) |
| Días sin artículos nuevos reales (no-falso-positivo) | 42+ (desde la semilla del 2026-05-24, ningún fetch automático ha producido un artículo real) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : ~2026-06-24 (6 archivos nuevos en sources/, TODOS falsos positivos)
Resultado sesión 2026-07-05         : 6/6 pendientes eran falsos positivos → 0 páginas nuevas de wiki

Causa raíz identificada (esta sesión):
  fetch_ddg_search() (scripts/fetch_news.py) arma la query como
  `site:prensa.com agropecuario OR agricultura OR ... OR MIDA OR cosecha Panamá`
  pero el operador site: de DuckDuckGo NO se aplica de forma estricta por el backend,
  y la función nunca validaba el dominio del resultado — a diferencia de fetch_rss()
  y fetch_gdelt_historical(), que sí llaman _is_blocked_domain()/_is_panama_related().
  Resultado: cualquier artículo que mencione "MIDA" en cualquier país (Utah "Military
  Installation Development Authority", agencias malasias, etc.) o que matchee otro
  término ambiguo, se cuela etiquetado con fuente "prensa.com" aunque venga de
  sltrib.com, nyfb.org, spa.gov.sa, etc. Esto explica el 100% de los 13 falsos
  positivos acumulados hasta ahora (todos vía la búsqueda "prensa_agro").

Fix aplicado (2026-07-05): fetch_ddg_search() ahora valida que el dominio del
  resultado coincida con el `site` configurado (o subdominio) antes de aceptar
  el artículo, más _is_blocked_domain() como defensa adicional.
Estado post-fix: pendiente validar en la próxima corrida real de GitHub Actions
  que ya no aparezcan artículos fuera de dominio bajo fuente "prensa.com".

GDELT (backfill histórico, sourcecountry:PA):
  45 ventanas completadas (2017–2025 llenas en trimestres, 2026 en curso) pero
  0 artículos reales han resultado de GDELT hasta ahora — el filtro sourcecountry:PA
  es correcto (mantiene 0% falsos positivos desde ese canal) pero sugiere que GDELT
  tiene poca cobertura indexada de medios panameños, o que faltan términos de
  búsqueda relevantes. 2015 y 2016 aún NO tienen ninguna ventana procesada — son la
  prioridad siguiente del backfill.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos reales | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — no iniciado** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — no iniciado** |
| 2017 Q1-Q4 | 4/4 | 0 | Completo |
| 2018 Q1-Q4 | 4/4 | 0 | Completo |
| 2019 Q1-Q4 | 4/4 | 0 | Completo |
| 2020 Q1-Q4 | 4/4 | 0 | Completo |
| 2021 Q1-Q4 | 4/4 | 0 | Completo |
| 2022 Q1-Q4 | 4/4 | 0 | Completo |
| 2023 Q1-Q4 | 4/4 | 0 | Completo |
| 2024 Q1-Q4 | 4/4 | 0 | Completo |
| 2025 Q1-Q4 | 4/4 | 0 | Completo |
| 2026 (parcial, día a día) | 9 ventanas diarias hasta 2026-07-03 | 0 | En curso |
| **TOTAL** | **45 ventanas** | **0 vía GDELT** | **2015-2016 sin iniciar; resto sin resultados** |

> GDELT con `sourcecountry:PA` no ha producido ningún artículo real todavía — mantiene
> 0% falsos positivos por ese canal, pero indica cobertura escasa de medios panameños
> en el índice de GDELT, o que faltan términos de búsqueda. Los 6 artículos reales del
> wiki siguen siendo 100% datos semilla manuales (ver historial abajo).
> Próximo paso de backfill: completar ventanas de 2015 y 2016 (actualmente en 0/4 cada uno).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-05 | 0 reales (6 falsos positivos rechazados) | 0 | Fix de causa raíz en fetch_ddg_search() (validación de dominio); ver wiki/log.md |

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
