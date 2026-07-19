---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-19
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 | **0 nuevos** ⚠️ +9 esta sesión |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 50 / ~46 estimadas | 45 (2015→hoy) — backfill histórico esencialmente completo |
| Días sin artículos nuevos | 4 (2026-07-16 → 2026-07-19) | ⚠️ supera el máx. de 3 días |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-18 (0 artículos nuevos)
Resultado              : 4 días consecutivos sin artículos NUEVOS reales en
                         sources/articles/ (último artículo real: 2026-07-15)

Causa raíz identificada (sesión 2026-07-19):
  1. GDELT: 50 ventanas trimestrales completadas (~46 esperadas para
     2015→hoy) → el backfill histórico está esencialmente agotado. Esto es
     esperado, no un bug; de aquí en adelante GDELT solo aportará ventanas
     nuevas a medida que avance el calendario (~1 cada pocos meses).
  2. RSS (IICA, La Prensa): 0 entradas nuevas calificantes en los últimos
     días — posible agotamiento temporal de contenido publicado, no error
     de fetch.
  3. BUG ENCONTRADO Y CORREGIDO: fetch_ddg_search() (búsqueda DuckDuckGo
     News) no aplicaba los filtros _is_blocked_domain()/_is_panama_related()
     que sí usa fetch_rss(). Resultado: colaba artículos globales relevantes
     solo por keyword ("MIDA", "agriculture", etc.) sin verificar que fueran
     de Panamá, etiquetándolos incorrectamente con source="prensa.com" y
     country="PA". Esto explica los 9 pendientes de esta sesión — 100%
     falsos positivos: la sigla "MIDA" colisionó con el Ministry of
     Investment, Trade and Industry de Malasia y con la Military
     Installation Development Authority de Utah, más 3 artículos genéricos
     de agricultura de Irán/EE.UU./Arabia Saudita. Probablemente explica
     también varios de los "1 artículo nuevo" reportados en sesiones previas
     (2026-07-10, 07-14, 07-15).
Fix aplicado            : scripts/fetch_news.py — fetch_ddg_search() ahora
                         aplica _is_blocked_domain(url) y
                         _is_panama_related(title, url), igual que
                         fetch_rss(). También se corrigió un bug en
                         scripts/ingest.py::mark_ingested() que crasheaba al
                         iterar la clave interna _gdelt_windows (lista, no
                         dict), impidiendo marcar artículos como ingestados.
Estado post-fix         : Pendiente validación en próxima corrida Actions —
                         debería reducir drásticamente los falsos positivos
                         provenientes de DDG.
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
| 2026-07-19 | 0 | 0 | 9 pendientes revisados = 9 falsos positivos (colisión "MIDA" Malasia/Utah + 3 genéricos) descartados sin ingestar. Fix de bug en fetch_ddg_search() (sin filtro Panamá) y en mark_ingested() (crash con _gdelt_windows). ⚠️ 4 días sin artículos reales nuevos |

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
