---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-16
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 (7 previos + 16 hoy) | **0 nuevos** ⚠️ ver diagnóstico |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal real | 2016-05 (semilla) — 2024-03 (semilla) | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 68 (37 trimestrales 2017-Q1→2026-Q2 + 31 del trimestre en curso) | 45+ (2015→hoy) |
| Gap de cobertura GDELT | 2015-02-19 → 2017-03-29 **nunca fetcheado** | 0 |
| Días sin artículos nuevos | 17 (último `saved_at`: 2026-07-30; hoy 2026-08-16) | máx 3 antes de diagnosticar ⚠️ |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida con artículos nuevos : 2026-07-30 (saved_at más reciente en processed.json)
Días sin artículos nuevos           : 17 — supera el umbral de alarma (3 días)

Causa raíz #1 (crítica, corregida hoy):
  scripts/fetch_news.py::fetch_ddg_search() no aplicaba el filtro
  _is_panama_related()/_is_blocked_domain() que sí usa fetch_rss().
  El operador "site:prensa.com" de la búsqueda DDG no se respeta de forma
  confiable, así que el fetch traía noticias agro de cualquier país
  (España/Aragón, Utah, Brasil, Arabia Saudita, Malasia) y las etiquetaba
  igual como fuente "prensa.com". Además "MIDA" como término de búsqueda
  primario colisiona con siglas homónimas en Utah y Malasia.
  → Fix aplicado en esta sesión (ver wiki/log.md 2026-08-16 00:45):
    se agregó el mismo guardrail de fetch_rss() a fetch_ddg_search().
    Pendiente de validar en la próxima corrida de GitHub Actions.

Causa raíz #2 (backfill incompleto, sin corregir aún):
  Las ventanas GDELT completadas (_gdelt_windows en processed.json) cubren
  2017-03-30 → 2026-06-17 en trimestres regulares, más 31 ventanas del
  trimestre en curso (2026-06-18 → 2026-08-14, una por cada corrida diaria
  de Actions). El período 2015-02-19 → 2017-03-29 (~2 años, cobertura
  objetivo del wiki) NUNCA fue fetcheado — no hay ventanas para esas
  fechas. Falta investigar scripts/fetch_historical.py para confirmar si
  el backfill arrancó desde 2017 por configuración o si las ventanas de
  2015-2016 fallaron silenciosamente y se perdieron del registro.

Causa raíz #3 (posible, sin confirmar):
  0 artículos nuevos guardados desde 2026-07-30 pese a que sí se siguen
  registrando ventanas GDELT completadas hasta 2026-08-14 — sugiere que
  GDELT está devolviendo 0 resultados relevantes para esas ventanas
  recientes (no necesariamente un fallo del fetch, podría ser que
  simplemente no hay cobertura de noticias agro-Panamá en GDELT para esas
  fechas, o que el filtro de relevancia está siendo demasiado estricto).
  Sin logs de Actions disponibles en esta sesión para confirmar cuál caso
  aplica — revisar el log de la próxima corrida.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

Las ventanas reales en `_gdelt_windows` son de ~91 días corridos (no
trimestres calendario fijos), así que esta tabla refleja el estado real en
vez de la grilla original estimada:

| Rango | Estado |
|-------|--------|
| 2015-02-19 → 2017-03-29 (~2 años, objetivo original del wiki) | ❌ **Nunca fetcheado** — 0 ventanas registradas |
| 2017-03-30 → 2026-06-17 | ✅ 37 ventanas de ~91 días, completadas y registradas |
| 2026-06-18 → 2026-08-14 (trimestre en curso) | 🔄 31 ventanas incrementales (una por corrida diaria de Actions), 0 artículos nuevos guardados desde 2026-07-30 |
| **TOTAL ventanas registradas** | **68** |

> Gap crítico: falta cubrir 2015-02-19 → 2017-03-29. Investigar
> `scripts/fetch_historical.py` para confirmar el punto de arranque
> configurado y, si es necesario, ejecutar el backfill manualmente para
> ese rango con `python wiki_agro.py historical --domain prensa.com`
> (o el comando equivalente) apuntando explícitamente a 2015-2017.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-16 | 0 (16 revisados, 16 falsos positivos) | 0 | Ver wiki/log.md — bug de `mark-all-ingested` corregido + fix de `fetch_ddg_search()` sin filtro Panamá (causa raíz de los 16 falsos positivos) + gap de cobertura 2015-2017 detectado |

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
