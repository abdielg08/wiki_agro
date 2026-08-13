---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-13
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (16 nuevos hoy) | **0 nuevos** — no cumplida hasta hoy |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 38 fechas únicas (65 entradas, ver nota) | ~47 (2015→hoy, trimestral) |
| Días sin artículos nuevos | **14** (último: 2026-07-30) | máx 3 antes de diagnosticar — **INCUMPLIDA** |

**⚠️ Alarma activa**: 14 días sin artículos nuevos en `sources/articles/` (último `saved_at`: 2026-07-30).
Muy por encima del umbral de 3 días de CLAUDE.md. Ver diagnóstico abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-12 (corre cada 2-3 días, no diario)
Resultado               : 0 artículos nuevos en las últimas 6 corridas consecutivas
                          (2026-07-31, 08-02, 08-04, 08-07, 08-10, 08-12)
Cola de ingesta          : 16 pendientes acumulados desde 2026-06-22, TODOS falsos
                          positivos (0 relacionados con Panamá) — procesados y
                          descartados en la sesión de hoy (2026-08-13)

Causa raíz #1 (falsos positivos) — CORREGIDA HOY:
  La búsqueda web `prensa_agro` (DuckDuckGo vía scripts/fetch_news.py::fetch_ddg_search)
  no filtraba resultados fuera de dominio (el operador `site:` de ddgs.news() no se
  respeta) ni exigía mención de "Panamá". Capturó ruido global de cualquier país que
  mencionara términos genéricos ("MIDA", "agricultura", "sequía", "riego"). Fix:
  validar dominio real de la URL + exigir "panama"/"panamá" en título+cuerpo.
  Ver wiki/log.md 2026-08-13 08:45 para detalle completo.

Causa raíz #2 (cero artículos nuevos, incluso falsos positivos) — SIN RESOLVER:
  El fetch dejó de encontrar artículos NUEVOS de cualquier tipo desde 2026-07-30.
  Hipótesis a investigar en la próxima corrida de Actions (no verificable desde
  esta sesión — la política de red del sandbox bloquea prensa.com e iica.int):
    1. RSS de IICA/La Prensa sin entradas nuevas o feed caído/cambiado de URL
    2. GDELT: la ventana "actual" (trimestre en curso, inicio 2026-06-18) se
       re-consulta cada corrida con fecha final móvil (hoy-1d) — ver nota de
       ventanas abajo — pero sigue sin producir resultados Panamá-relevantes
       nuevos, lo que sugiere que GDELT simplemente no está indexando noticias
       agro de Panamá recientes bajo `sourcecountry:PA`
  Acción recomendada: revisar logs de la próxima corrida de GitHub Actions
  (no visible desde este repo) para confirmar código de estado HTTP de RSS/GDELT.

Nota sobre ventanas GDELT:
  processed.json["_gdelt_windows"] tiene 65 entradas pero solo 38 fechas de
  inicio únicas — el trimestre más reciente (arranca 2026-06-18) se re-agrega
  con una fecha final distinta en cada corrida (fetch_gdelt_historical usa
  `end = datetime.utcnow() - 1 día`, que avanza cada día), inflando el conteo
  sin representar cobertura real nueva. Además, el rango más antiguo
  (2015-01-01 a 2017-03-29, ~9 trimestres) todavía NO aparece como completado
  — el backfill histórico temprano sigue incompleto pese al conteo alto de
  entradas. No se recomienda tratar "65 ventanas" como señal de rango agotado.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — hueco en el backfill** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — hueco en el backfill** |
| 2017 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2018 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2019 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2020 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2021 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2022 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2023 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2024 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2025 Q1-Q4 | 4/4 | 0 | Completado (0 artículos Panamá-relevantes hallados) |
| 2026 Q1-Q3 | 2/3 + 1 en curso | 0 | En curso (trimestre actual se re-consulta cada corrida) |
| **TOTAL** | **38/47 fechas únicas** | **0 vía GDELT** | **2015-2016 pendientes; 2017-2025 sin hallazgos** |

> Diagnóstico: GDELT completó 2017-2025 sin encontrar NINGÚN artículo que pase el
> filtro `sourcecountry:PA` + mención de Panamá. Esto sugiere que el índice de
> GDELT tiene muy poca cobertura de fuentes panameñas, o que el filtro es
> demasiado estricto (posible sobre-ajuste de `_is_panama_related`/`sourcecountry:PA`).
> Los 6 artículos reales del wiki vinieron todos de la semilla manual (MIDA, IICA,
> TVN, La Prensa, BDA), no de GDELT. 2015-2016 siguen sin cubrirse: cada corrida de
> `fetch_gdelt_historical()` reinicia el barrido desde 2015-01-01, así que esas
> ventanas se reintentan en cada ejecución pero nunca quedan marcadas como
> completadas — indica error de red/HTTP persistente y repetido en esas fechas
> específicas (posible rate-limit temprano de GDELT en cada corrida). Revisar
> logs de Actions para ver el error exacto en las primeras ventanas de cada corrida.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-13 | 0 reales (16 falsos positivos descartados) | 0 | Causa raíz de falsos positivos corregida en `fetch_ddg_search()`; bug de `mark-all-ingested` (desalineado con `ingest --limit`) corregido; alarma de 14 días sin artículos nuevos documentada — ver wiki/log.md |

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
