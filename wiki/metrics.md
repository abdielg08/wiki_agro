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
| Artículos reales ingestados (wiki) | 13 | = total sin falsos positivos |
| Marcados como procesados (incl. falsos positivos) | 18 | — |
| Pendientes de ingesta | 11 | 0 |
| Falsos positivos acumulados | 12 (7 previos + 5 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 70 | 45 (2015→hoy) — **rango agotado, necesita expansión** |
| Días sin artículos nuevos reales | ~18 (último real: 2026-07-31) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-17 — "0 artículos nuevos descargados"
Racha sin nuevos        : 2026-08-02 → 2026-08-17 (16 corridas, salvo 2026-07-30/31
                          con 2-3 nuevos). Cron diario SÍ está corriendo (commits
                          diarios confirmados en sources/).

Causa raíz encontrada (sesión 2026-08-18):
  1. GDELT: 70 ventanas ya completadas (> 45 esperadas para 2015→hoy) → el rango
     histórico disponible está prácticamente agotado; nuevas corridas de GDELT ya
     no aportan artículos nuevos porque casi todo el período ya fue escaneado.
  2. DDG web_search "prensa_agro" (config/sources.yaml → scripts/fetch_news.py
     fetch_ddg_search): construía la query como `site:prensa.com {keywords}`, pero
     el endpoint ddgs.news() NO respeta el operador `site:` de forma confiable.
     Resultado: devolvía artículos de dominios totalmente ajenos (paultan.org,
     sltrib.com, msn.com, heraldo.es, nyfb.org, spa.gov.sa, whc.unesco.org,
     ieeexplore.ieee.org, archive.org, agenciabrasil.ebc.com.br) etiquetados
     incorrectamente como source="prensa.com", sin verificar el dominio real.
  3. "MIDA" está en search_terms.primary como sigla ambigua (coincide con Malaysian
     Investment Development Authority y con Military Installation Development
     Authority de Utah) — is_agro_relevant() los aceptaba solo por esa coincidencia.
  Resultado combinado: el 100% de los 16 pendientes en processed.json (antes de esta
  sesión) resultaron ser falsos positivos del pipeline "prensa_agro", no del LLM.

Fix aplicado (2026-08-18) : scripts/fetch_news.py fetch_ddg_search() ahora verifica
  que el netloc de la URL devuelta coincida con el `site` solicitado antes de
  aceptar el resultado (urlparse + comparación exacta o subdominio).

Pendiente de seguir revisando: los 11 pendientes restantes probablemente incluyen
  más falsos positivos del mismo pipeline (generados antes del fix) — revisar en
  la próxima sesión de ingesta.

Recomendación siguiente corrida: considerar ampliar el rango de fechas de GDELT o
  reducir su prioridad frente a RSS/DDG (ya corregido) como fuente principal, dado
  que el backfill histórico vía GDELT está cerca de su límite de cobertura real.
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
| 2026-08-18 | 0 | 11 | 5/5 revisados = falsos positivos (colisión sigla "MIDA" + bug `site:` en DDG). Fix aplicado en fetch_ddg_search(). |

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
