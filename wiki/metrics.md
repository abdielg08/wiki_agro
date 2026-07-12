---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-12
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 (7 previos + 7 nuevos 2026-07-12) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~47 estimadas | 45+ → rango agotado |
| Días sin artículos nuevos (reales) | 0 (llegó 1 hoy, pero fue falso positivo) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-12 (commit 88389fe, "1 artículos nuevos descargados")
Resultado               : Actions SÍ está corriendo con regularidad (commits chore(sources)
                          diarios visibles en git log), pero el rendimiento neto de
                          artículos REALES es ~0: de los últimos ~15 artículos descargados
                          por el fetcher web_searches "prensa_agro", 14/14 fueron falsos
                          positivos (Utah MIDA, Malasia, Arabia Saudita, Irán/UNESCO, etc.)
Causa raíz identificada : fetch_ddg_search() en scripts/fetch_news.py NO aplicaba los
                          filtros _is_blocked_domain()/_is_panama_related() que sí tienen
                          fetch_rss() y fetch_gdelt_batch(). La búsqueda DDG
                          "site:prensa.com ... OR MIDA OR cosecha Panamá" no respeta el
                          filtro site: de forma confiable, y el término "MIDA" hace match
                          con la agencia estatal de Utah (Military Installation
                          Development Authority), inflando falsos positivos.
Fix aplicado (hoy)      : se agregaron los mismos filtros de dominio/término-Panamá a
                          fetch_ddg_search(), y "source" ahora usa el dominio real de la
                          URL en vez del nombre del sitio buscado (evita mislabeling).
                          Ver wiki/log.md 2026-07-12 00:00 para detalle completo.
Estado post-fix         : Pendiente validación en próxima corrida Actions — debería
                          reducir drásticamente los falsos positivos de la fuente DDG.
GDELT                   : 48 ventanas completadas (~45+ = rango de fechas 2015→hoy
                          esencialmente agotado). El backfill histórico vía GDELT ya no
                          es la fuente principal de artículos nuevos; el flujo diario
                          depende de RSS (IICA, La Prensa) y de las búsquedas DDG ahora
                          corregidas.
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
| 2026-07-12 | 0 (7/7 falsos positivos) | 0 | Root-cause fix: fetch_ddg_search() sin filtro Panama/dominio |

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
