---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (7 previos + 11 hoy) | **0 nuevos** desde el fix de hoy |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 (8 topics, 3 entities, 6 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 53 / ~45 estimadas | rango agotado — ver nota abajo |
| Días sin artículos nuevos (útiles) | 4 (último real: 2026-07-20) | máx 3 antes de diagnosticar — **alarma activa** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions       : 2026-07-23 (commits diarios "chore(sources)" confirman que
                                Actions SÍ está corriendo)
Resultado                    : 0 artículos nuevos en 07-21 y 07-23; último real: 07-20 (2 nuevos)
Causa identificada (hoy)     : 11/11 artículos "nuevos" del batch pendiente eran falsos positivos,
                                todos vía fetch_ddg_search() (config web_searches: prensa_agro).
                                Query DDG "agropecuario OR ... OR MIDA OR cosecha Panamá" no
                                aplica "Panamá" a todos los términos (precedencia de OR), y el
                                prefijo site:prensa.com no es respetado por ddgs.news() — llegaron
                                artículos de Malasia, Utah, Arabia Saudita, Irán y Nueva York.
Fix aplicado (hoy)           : fetch_ddg_search() ahora usa las mismas guardas
                                _is_blocked_domain() + _is_panama_related() que ya tenían
                                fetch_rss() y fetch_gdelt_batch(). _is_panama_related() ampliado
                                para aceptar ccTLD .pa (mida.gob.pa, bda.gob.pa, etc).
                                Ver wiki/log.md 2026-07-24 08:20 para detalle y backtest.
Ventanas GDELT               : 53/45 estimadas — rango históricamente agotado. El fetch diario
                                de GDELT probablemente ya no aporta artículos nuevos por ventanas;
                                la fuente activa remanente es RSS (IICA, La Prensa) + web_searches.
Estado post-fix              : Pendiente validar en próxima corrida Actions (mañana) que
                                fetch_ddg_search ya no produzca falsos positivos.
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
| 2026-07-24 | 0 | 0 | 11/11 falsos positivos detectados y rechazados (0% mantenido); root cause corregido en fetch_ddg_search() |

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
