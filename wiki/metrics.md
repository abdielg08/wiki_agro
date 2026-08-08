---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-08
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 63 / ~45 estimadas | 45 (2015→hoy) — rango agotado |
| Días sin artículos nuevos reales | ≥4 corridas de Actions | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-07 (0 artículos nuevos)
Resultado               : 4 corridas consecutivas (08-07, 08-04, 08-02, 07-31) con 0
                          artículos nuevos reales. La corrida de 07-30 trajo 3 "nuevos"
                          que resultaron ser falsos positivos (ver diagnóstico abajo).
Causa identificada      : scripts/fetch_news.py::fetch_ddg_search() (búsqueda DDG
                          "prensa_agro" con site:prensa.com) no aplicaba _is_panama_related()
                          ni verificaba que el dominio devuelto coincidiera con el `site`
                          pedido — a diferencia de fetch_rss() y fetch_gdelt_batch(), que sí
                          lo hacían. Resultado: 16/16 artículos pendientes eran de dominios
                          ajenos a Panamá (Utah, Malasia, Arabia Saudita, España, Brasil,
                          etc.), coincidiendo por match genérico de "MIDA" u otros términos.
                          Además, ventanas GDELT ya en 63 (>45) → rango histórico
                          2015–2027 prácticamente agotado, así que el único fetch que
                          seguía trayendo "resultados" era la búsqueda DDG rota.
Fix aplicado (2026-08-08): fetch_ddg_search() ahora exige que el dominio de la URL
                          devuelta coincida con `site`, aplica _is_blocked_domain(), y
                          exige _is_panama_related() — igual que RSS/GDELT. Ver
                          wiki/log.md 2026-08-08 08:10 para el diagnóstico completo.
Estado post-fix          : Pendiente validación en la próxima corrida de GitHub Actions.
                          Si sigue en 0 artículos reales tras el fix, revisar si RSS de
                          IICA/La Prensa siguen activos y considerar ampliar
                          web_searches hacia dominios .gob.pa.
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
| 2026-08-08 | 0 | 0 | 16 falsos positivos detectados y rechazados (0 ingestados al wiki) + fix de bug raíz en fetch_ddg_search() (faltaba filtro _is_panama_related y verificación de dominio) |

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
