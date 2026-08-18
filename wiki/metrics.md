---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-18
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 el 2026-06-22 + 16 el 2026-08-18) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 70 / ~45 estimadas | 45 (2015→hoy) — **rango agotado, ver nota** |
| Días sin artículos nuevos genuinos | 12+ (2026-08-06 → hoy) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con contenido : 2026-08-17 (0 artículos nuevos genuinos)
Resultado                    : Pendientes de ingesta llegaron a 16 — LOS 16 eran
                                falsos positivos (0% eran sobre agro de Panamá)
Causa identificada           : web_search "prensa_agro" en config/sources.yaml usa
                                site:prensa.com vía DDG, pero el operador site: no
                                se respeta de forma confiable → colaban artículos
                                de dominios ajenos (heraldo.es, sltrib.com, etc.)
                                etiquetados incorrectamente source="prensa.com".
                                Además "MIDA" colisiona con Malaysia/Utah MIDA.
Fix aplicado (2026-08-18)    : fetch_ddg_search() ahora verifica que el dominio
                                real del resultado coincida con el `site` pedido.
                                fetch_gdelt_window() (fetch_historical.py) ahora
                                aplica el mismo filtro _is_panama_related() que
                                ya usaba fetch_gdelt_batch (fetch_news.py).
Estado post-fix               : Pendiente validación — revisar en la próxima
                                sesión si aparecen artículos genuinos o si el
                                conteo de nuevos se mantiene en 0 (en ese caso
                                el problema sería falta de contenido, no un bug).
Nota GDELT                    : 70 ventanas completadas > ~45 estimadas → el
                                query de fetch_gdelt_historical ya cubrió el
                                rango 2015→hoy varias veces sin encontrar más
                                artículos nuevos con los términos actuales;
                                considerar ampliar search_terms o aceptar que
                                esa vía está saturada por ahora.
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
| 2026-08-18 | 0 | 0 | 16 pendientes revisados = 16 falsos positivos (0 ingestados). Fix de raíz: `fetch_ddg_search()` sin verificación de dominio real + `fetch_gdelt_window()` sin filtro Panamá. Ambos corregidos. |

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
