---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 24 (7 previos + 17 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 70 | 45-46 (2015→hoy) — **rango agotado, ver diagnóstico** |
| Días sin artículos nuevos (reales) | — todos los descargados hasta hoy fueron falsos positivos | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-19 (corre diariamente, [skip ci] — confirmado activo)
Resultado               : 1 artículo nuevo — pero era falso positivo (Maine.gov, agricultura
                          de EE.UU.), causado por bug en fetch_ddg_search()
Causa identificada      : (1) Ventanas GDELT completadas = 70, muy por encima del estimado de
                          45-46 → el backfill histórico 2015-hoy vía GDELT está prácticamente
                          agotado; ya no aporta artículos nuevos por esa vía.
                          (2) La fuente "prensa.com" (búsqueda DDGS.news, config/sources.yaml)
                          NO filtraba por relevancia a Panamá — solo por términos agro
                          genéricos — y el operador `site:prensa.com` no era respetado por
                          DDGS, trayendo resultados de Maine, Brasil, Irán, España, Utah y
                          Malasia. 100% de los artículos de "prensa.com" ingeridos en esta
                          sesión (10 de 10 revisados) fueron falsos positivos.
Fix aplicado (2026-08-19): scripts/fetch_news.py — fetch_ddg_search() ahora aplica
                          _is_panama_related() + chequeo de "panam" en el cuerpo (igual que
                          fetch_rss()), más un nuevo _matches_site() que verifica que el
                          dominio del resultado realmente coincida con el `site` configurado
                          (filtro post-búsqueda, ya que DDGS no lo garantiza). Ver wiki/log.md
                          2026-08-19 16:40 para detalle completo.
Estado post-fix         : Pendiente validación en la próxima corrida de Actions — se espera
                          que "prensa.com" traiga 0 o muy pocos artículos hasta que DDGS
                          indexe contenido real de prensa.com sobre agro panameño. Si en 3+
                          días no llegan artículos nuevos reales, evaluar expandir fuentes
                          (más RSS de medios panameños, o ampliar site: a otros dominios
                          .com.pa / .gob.pa).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Recalculado esta sesión desde `sources/processed.json` → `_gdelt_windows` (70 ventanas).

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 | 0/4 | **Pendiente — gap real, backfill nunca corrió para este año** |
| 2016 | 0/4 | **Pendiente — gap real, backfill nunca corrió para este año** |
| 2017 | 4/4 | Completo |
| 2018 | 4/4 | Completo |
| 2019 | 4/4 | Completo |
| 2020 | 4/4 | Completo |
| 2021 | 4/4 | Completo |
| 2022 | 4/4 | Completo |
| 2023 | 4/4 | Completo |
| 2024 | 4/4 | Completo |
| 2025 | 4/4 | Completo |
| 2026 | 34 ventanas | No es backfill trimestral — es la ventana diaria del fetch normal
(`20260618_<hoy>`), que se re-registra cada día que corre `wiki_daily.yml`. No cuenta para el backfill histórico. |
| **TOTAL histórico (2015-2025)** | **36/44 trimestres** | **2015-2016 son el único gap real** |

**Diagnóstico**: el crawl histórico (`wiki_historical.yml`, solo `workflow_dispatch`, rango
default `2010-2025`) cubrió 2017-2025 completamente pero **nunca completó 2015-2016** —
no hay evidencia de que esas ventanas se hayan siquiera intentado. Dado que la cobertura
objetivo del wiki es "2015-02-19 → hoy", este es el único vacío real en el backfill.
**Acción recomendada** (requiere disparo manual, no lo ejecuta esta rutina): correr
`wiki_historical.yml` con `years: "2015-2016"` y `mode: gdelt` para cerrar el gap.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-19 | 0 (17 falsos positivos: 13 revisados + 4 detectados en auditoría de integridad) | 0 | Bugfix mark_ingested/mark_all_ingested (orden incorrecto); bugfix fetch_ddg_search (sin filtro Panamá, site: no verificado — causa raíz de los FP); hallazgo: gap real de backfill en 2015-2016 (0/8 trimestres) |

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
