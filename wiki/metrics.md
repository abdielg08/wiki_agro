---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-09
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados (con página wiki) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 37 / ~46 estimadas (limpiado de 63 — 26 eran duplicados por bug, ver log 2026-08-09) | 46 (2015→hoy) |
| Días sin artículos nuevos reales | ≥15 (último ingreso real: semilla 2026-05-24; todo lo descargado desde entonces fue falso positivo) | máx 3 antes de diagnosticar |

**⚠️ Señal de alarma activa**: 0 artículos nuevos *reales* desde la semilla del 2026-05-24.
Los 23 artículos descargados desde entonces resultaron ser 100% falsos positivos.
Diagnóstico de causa raíz y fixes aplicados hoy — ver "Estado del Fetch" abajo.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions        : 2026-08-07 (commit ff8157d, 0 artículos nuevos)
Artículos reales desde semilla : 0 — el pipeline solo producía falsos positivos
Causas identificadas hoy (2026-08-09):
  1. fetch_ddg_search() armaba "site:prensa.com <query>" pero el backend
     de noticias de `ddgs` no respeta `site:` de forma confiable →
     devolvía artículos de dominios ajenos (heraldo.es, nyfb.org,
     spa.gov.sa, sltrib.com, paultan.org, ebc.com.br, whc.unesco.org,
     msn.com) que solo coincidían por palabra clave ("MIDA",
     "agriculture"), etiquetados incorrectamente como source=prensa.com /
     country=PA sin verificar el dominio real.
     FIX: se descarta cualquier resultado cuyo dominio no contenga el
     `site` configurado.
  2. fetch_gdelt_historical() marcaba como "completa" la ventana de cola
     (la más reciente, sin llegar aún a 90 días) usando un límite
     superior móvil (utcnow()-1d) → generaba una ventana casi duplicada
     nueva cada corrida (26 entradas basura acumuladas desde 2026-06-18)
     sin avanzar nunca al siguiente trimestre real.
     FIX: solo se marca completa una ventana de 90 días exactos.
  3. Sin confirmar (requiere red real de Actions): las ventanas GDELT de
     2015-01-01 a 2017-03-29 (~8 trimestres) nunca se completaron — podría
     ser fallo de red recurrente o límite real de cobertura del GDELT DOC
     API (~2017). Pendiente de investigar con acceso real a internet.
Estado post-fix                : pendiente validar en la próxima corrida real de Actions
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — ver diagnóstico abajo** |
| 2016 Q1-Q4 | 0/4 | 0 | **Pendiente — ver diagnóstico abajo** |
| 2017 Q1-Q4 | 4/4 | 0 (todos 0 resultados de GDELT) | Cerrado |
| 2018 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2019 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2020 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2021 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2022 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2023 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2024 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2025 Q1-Q4 | 4/4 | 0 | Cerrado |
| 2026 Q1-Q2 (parcial: 2026-03-19→2026-06-17) | 1/2 | 0 | En curso — cola abierta desde 2026-06-18 |
| **TOTAL** | **37/46** | **0 vía GDELT** | **2017→2026 cerrado, 2015-2017 sin cubrir** |

> Todas las ventanas GDELT cerradas (2017–2026) devolvieron 0 artículos hasta ahora —
> ningún artículo del wiki actual proviene de GDELT; todos son de RSS (IICA, La Prensa)
> o de la búsqueda DDG `site:prensa.com` (esta última corregida hoy, ver log 2026-08-09).
> Esto sugiere que la query GDELT (`sourcecountry:PA` + `sourcelang:spa` + términos
> agro) puede ser demasiado estricta — investigar en próxima sesión si vale la pena
> relajarla (p. ej. quitar `sourcelang:spa`, ya que medios en inglés también cubren
> Panamá).
> Las ventanas 2015-2017 Q1 nunca se han completado exitosamente — diagnóstico
> pendiente de confirmar con red real de GitHub Actions (ver log 2026-08-09).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-09 | 0 reales (16 falsos positivos descartados) | 0 | Routine automatizada. 16/16 artículos del backlog eran falsos positivos (colisión "MIDA" con Malasia/Utah/EE.UU. + búsqueda DDG sin scope de dominio). Diagnóstico de causa raíz: (1) fix a `fetch_ddg_search()` para validar dominio real del resultado, (2) fix a `fetch_gdelt_historical()` que generaba ventanas de cola duplicadas cada corrida, (3) fix a 2 bugs en `mark_ingested`/`mark_all_ingested` (crash por `_gdelt_windows` y desalineación de batches), (4) limpieza de 26 ventanas GDELT basura en `processed.json`. Ver `wiki/log.md` para detalle completo. |

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
