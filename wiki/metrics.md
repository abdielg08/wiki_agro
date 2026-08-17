---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-17
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 26 (7 previos + 12 de hoy + 7 marcados sin verificar en jun-2026) | **0 nuevos desde el fix** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas (`_gdelt_windows`) | 70 (irregulares, ver nota) | 45 (2015→hoy) |
| Días sin artículos nuevos REALES | >300 (desde 2024-03-05) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-17 (corre diario, "0 artículos nuevos" hace 6+ días seguidos)
Pendientes al iniciar sesión de hoy : 16 → revisados 12 en total, los 12 = falsos positivos

CAUSA RAÍZ IDENTIFICADA (grave, llevaba desde ~2025-03 sin detectarse):
  scripts/fetch_news.py::fetch_ddg_search() arma la query como
  "site:prensa.com {query}" y se la pasa a DDGS().news(). La librería `ddgs`
  NO respeta de forma confiable el operador "site:" en búsqueda de noticias,
  así que devuelve resultados de CUALQUIER dominio del mundo que mencione
  términos agro genéricos (agricultura, MIDA, cosecha, etc). El código
  entonces etiquetaba ciegamente cada resultado con
  source=site="prensa.com" y country="PA" (línea 296 y 299, sin verificar
  el dominio real de la URL) — es decir, TODO resultado de DDG quedaba
  marcado como si fuera de La Prensa Panamá y de Panamá, sin importar su
  origen real.

  Impacto medido: de los 23 artículos con source="prensa.com" en
  sources/articles/, LOS 23 SON FALSOS POSITIVOS. Ejemplos: Utah's
  "Military Installation Development Authority" (coincide con la sigla
  MIDA), Malaysia's "Malaysian Investment Development Authority" (misma
  sigla), agricultura de secano en Arabia Saudita, agricultura familiar en
  Brasil, el sistema de qanats persas (patrimonio UNESCO, Irán), noticias
  agrarias de Aragón (España), New York Farm Bureau (EE.UU.). Ninguno
  menciona a Panamá ni una sola vez en el texto completo.

  Filtro insuficiente adicional: is_agro_relevant() solo exige términos
  agro genéricos (sin exigir mención de Panamá), por lo que cualquier
  artículo agrícola mundial pasa el filtro una vez que ya trae la
  etiqueta country="PA" falsa.

FIX APLICADO (2026-08-17, esta sesión):
  scripts/fetch_news.py::fetch_ddg_search() ahora valida
  urlparse(url).netloc contra `site` antes de aceptar un resultado; si no
  coincide (ni como subdominio), se descarta. Esto detiene la
  contaminación en el punto de origen. NO se tocó is_agro_relevant() ni
  el filtro de GDELT (que sí usa sourcecountry:PA + sourcelang:spa
  correctamente).

  Bugs adicionales corregidos en scripts/ingest.py:
    - mark_ingested() iteraba processed.items() sin filtrar la clave
      interna "_gdelt_windows" (una lista) → AttributeError al llamar
      `python wiki_agro.py mark-ingested <url>`. Ahora usa
      article_entries(processed) igual que mark_all_ingested().
    - mark_all_ingested() usa find_pending() (orden alfabético por
      archivo) mientras que `ingest` usa prioritize() (orden por score)
      para elegir el lote de 5 a mostrar — los conjuntos NO coinciden,
      así que `mark-all-ingested --limit 5` puede marcar artículos
      distintos a los que Claude acaba de procesar. Detectado esta
      sesión (solo 1 de 5 coincidió). Pendiente de fix estructural —
      por ahora, usar `mark-ingested <url>` por cada URL procesada en
      vez de `mark-all-ingested` para evitar desincronización.

Estado post-fix : Validar en la próxima corrida de GitHub Actions que
                   fetch_ddg_search ya no traiga resultados fuera de
                   prensa.com. Si DDG deja de aportar artículos por el
                   filtro más estricto, el fetch dependerá casi
                   enteramente de RSS (IICA, La Prensa) y GDELT.

Nota sobre `_gdelt_windows` (70 entradas): las cadenas no son ventanas
trimestrales limpias — varias comparten el mismo inicio ("20260618_...")
con fin distinto cada día, sugiriendo que el conteo mezcla ventanas de
backfill histórico con re-consultas incrementales diarias. No se pudo
confirmar si el backfill 2015→hoy está realmente agotado o si el contador
está inflado — requiere revisión del código de fetch_historical.py en una
sesión futura (fuera de alcance de esta sesión de rutina).
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
| 2026-08-17 | 0 (12 revisados, 12 falsos positivos) | 0 | Causa raíz encontrada y corregida: DDG ignoraba `site:prensa.com` → fetch_ddg_search() ahora verifica el dominio real. Fix adicional en mark_ingested() (crash por `_gdelt_windows`). Ver Estado del Fetch arriba. |

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
