---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-14
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 21 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 | **0 nuevos** ⚠️ meta incumplida esta sesión |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~45 estimadas | 45 (2015→hoy) — **rango agotado** |
| Días sin artículos nuevos ÚTILES | ≥52 (desde 2026-05-24) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-14 (commit 8c765c0) — SÍ corrió, trajo 1 artículo nuevo
Resultado              : 1 artículo nuevo, pero es FALSO POSITIVO (ver wiki/log.md 2026-07-14)
                         → 0 artículos ÚTILES nuevos hoy
Causa identificada     : Bug en web_searches.prensa_agro (config/sources.yaml) — ddgs.news()
                         no respeta el operador site:prensa.com y devuelve resultados de
                         dominios arbitrarios (paultan.org, sltrib.com); fetch_ddg_search()
                         etiqueta country="PA"/language="es"/source=site sin verificar que
                         la URL real pertenezca al dominio esperado. "MIDA" como término de
                         búsqueda colisiona con acrónimos homónimos de otros países
                         (Malaysian Investment Development Authority, Utah Military
                         Installation Development Authority).
                         Ventanas GDELT: 48/~45 completadas → rango de fechas agotado.
                         RSS IICA y La Prensa no aportaron artículos nuevos hoy.
Fix aplicado           : Ninguno esta sesión — requiere cambio de código en
                         scripts/fetch_news.py (validar dominio real vs. site: esperado) y
                         config/sources.yaml (ajustar search_terms). Se notifica al usuario.
Estado post-fix        : Pendiente — 3 artículos más en cola con el mismo patrón
                         (revisar en próxima sesión de ingesta)
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
| 2026-07-14 | 0 (5 revisados, 5/5 falsos positivos) | 3 | Bug identificado: DDG `site:` no filtra dominio real (ver log.md) |

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
