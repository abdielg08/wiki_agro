---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-28
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 (7 previos + 11 esta sesión) | **0 nuevos ingestados al wiki** (mantenido: 0 de 18 llegó al wiki) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 56 (36 en 2017–2025 + 20 en 2026; **0 en 2015–2016**) | cobertura completa 2015→hoy |
| Pendientes de ingesta | 0 | 0 |
| Días sin artículos nuevos reales | ver diagnóstico abajo | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-27 (13:32 UTC) — completed / success
Corridas recientes     : diarias y exitosas (verificado vía API, sin fallas de infraestructura)
Resultado reciente     : la mayoría de corridas descargan 0-3 artículos/día;
                         de los descargados en las últimas semanas, el 100%
                         resultaron ser falsos positivos (ver abajo)

Causa raíz identificada (falsos positivos):
  1. config/sources.yaml → web_searches.prensa_agro usa DuckDuckGo
     `site:prensa.com`, pero DDG no siempre respeta el operador `site:`.
     Resultados de dominios no relacionados (paultan.org, sltrib.com,
     nyfb.org, spa.gov.sa, whc.unesco.org, ieeexplore.ieee.org, archive.org)
     se colaron y fueron guardados con metadatos falsos
     (source="prensa.com", country="PA", trust_level=3).
  2. "MIDA" está en search_terms.primary como acrónimo suelto — coincide
     con Malaysian Investment Development Authority, Utah's Military
     Installation Development Authority, etc., sin exigir contexto Panamá.

Fix aplicado (2026-07-28): scripts/fetch_news.py::fetch_ddg_search() ahora
  valida que el dominio real de la URL devuelta coincida con `site` (o un
  subdominio) antes de aceptar el resultado. Aplica a los 8 web_searches
  configurados. Pendiente de validar en la próxima corrida de Actions.

Gap de cobertura detectado: 0 ventanas GDELT completadas para 2015 y 2016
  (todas las demás años 2017-2025 tienen 4/4). No se pudo diagnosticar la
  causa exacta desde este sandbox (egress bloqueado hacia api.gdeltproject.org
  — 403 del proxy). Recomendado: revisar logs de Actions de corridas que
  intentaron ventanas 2015xxxx_2015xxxx / 2016xxxx_2016xxxx para ver si
  GDELT devuelve error o 0 resultados reales para ese rango.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | ⚠️ Bloqueado — ver diagnóstico arriba |
| 2016 Q1-Q4 | 0/4 | ⚠️ Bloqueado — ver diagnóstico arriba |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (parcial, hasta ayer) | 20 ventanas cortas | En progreso (avanza ~1 ventana/día cerca del presente) |
| **TOTAL** | **56** | **2015-2016 pendiente; 2017-2026 cubierto** |

> 2015-2016 son las dos únicas brechas reales de cobertura histórica. Cada
> corrida diaria las reintenta primero (nunca se marcaron completas) antes
> de continuar con ventanas posteriores — confirmar en logs de Actions si
> fallan por error de red/HTTP o simplemente no producen resultados.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados (reales) | Falsos positivos rechazados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-28 | 0 | 11 | 0 | Ver wiki/log.md — colisión de acrónimo "MIDA" + fuga del operador `site:` en búsqueda DDG. Fix aplicado en fetch_news.py. Bug adicional corregido en ingest.py (mark_ingested crash + mark_all_ingested desincronizado con pending_ingest.md; 3 artículos no revisados fueron revertidos a pendiente y luego procesados correctamente). |

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
