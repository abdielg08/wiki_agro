---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-05
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos ingestados al wiki** (23 detectados y descartados correctamente) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla, sin backfill real aún) | 2015 → hoy real |
| Ventanas GDELT completadas | 62 (2017-2025 completas, 2026 con churn — ver abajo) | 2015 y 2016 **faltan por completo** |
| Días sin artículos nuevos | 6 (último real: 2026-07-30) | máx 3 antes de diagnosticar — **⚠ alarma activa** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-04 (0 artículos nuevos)
Corridas previas        : 2026-08-02 (0), 2026-07-31 (0), 2026-07-30 (3), 2026-07-29 (2)
Resultado               : 3+ corridas consecutivas sin artículos nuevos → alarma de CLAUDE.md activa

HALLAZGO CRÍTICO DE ESTA SESIÓN (2026-08-05):
  Los 16 artículos que estaban pendientes de ingesta eran 16/16 FALSOS POSITIVOS
  (100%) — ninguno sobre agro de Panamá. Ver detalle en wiki/log.md.

  Causa raíz identificada: `fetch_ddg_search()` en scripts/fetch_news.py (fuente
  "prensa.com" del modo `daily`) NO aplicaba los filtros `_is_blocked_domain()` /
  `_is_panama_related()` que `fetch_rss()` sí tiene. El operador `site:prensa.com`
  de DuckDuckGo no se respeta de forma confiable — el buscador devolvía
  resultados de cualquier dominio (sltrib.com/Utah, paultan.org/Malasia,
  heraldo.es/Aragón España, ebc.com.br/Brasil, spa.gov.sa/Arabia Saudita,
  whc.unesco.org) que coinciden con términos genéricos como "MIDA" o
  "agricultura" pero no tienen relación con Panamá. El código además
  etiquetaba `source` con el sitio configurado (`prensa.com`) sin verificar
  que la URL real perteneciera a ese dominio, ocultando el problema en stats.

Fix aplicado (2026-08-05):
  - scripts/fetch_news.py: fetch_ddg_search() ahora verifica que el dominio
    real de la URL contenga el `site` configurado, y aplica
    _is_blocked_domain()/_is_panama_related() igual que fetch_rss().
  - scripts/ingest.py: mark_ingested() ya no crashea con claves internas
    no-dict de processed.json (ej. _gdelt_windows).
  - scripts/ingest.py: mark_all_ingested() ahora usa el mismo orden por
    score (prioritize()) que `ingest` muestra a Claude, en vez de orden
    alfabético de archivo — antes podía marcar artículos distintos a los
    que realmente se revisaron.
Estado post-fix         : Pendiente validar en la próxima corrida de Actions
                          que ya no entren falsos positivos de dominios
                          no-Panama vía DDG.

Hallazgo adicional — cobertura GDELT incompleta:
  Los años 2015 y 2016 (inicio del rango objetivo del wiki) tienen 0 ventanas
  GDELT completadas — el backfill histórico real nunca los ha cubierto.
  2026 en cambio tiene 26 "ventanas" registradas (vs. las ~4 trimestrales
  esperadas), producto de que cada corrida diaria genera una ventana nueva
  con fecha de fin distinta (ventanas tipo 20260618_2026MMDD) en vez de
  reusar la ventana del trimestre en curso — esto infla el contador sin
  aportar cobertura real y puede estar contribuyendo a que GDELT devuelva
  0 artículos nuevos (ventanas casi idénticas repetidas).
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Estado |
|---------|----------|--------|
| 2015 Q1-Q4 | 0/4 | **Pendiente — sin cubrir** |
| 2016 Q1-Q4 | 0/4 | **Pendiente — sin cubrir** |
| 2017 Q1-Q4 | 4/4 | Completo |
| 2018 Q1-Q4 | 4/4 | Completo |
| 2019 Q1-Q4 | 4/4 | Completo |
| 2020 Q1-Q4 | 4/4 | Completo |
| 2021 Q1-Q4 | 4/4 | Completo |
| 2022 Q1-Q4 | 4/4 | Completo |
| 2023 Q1-Q4 | 4/4 | Completo |
| 2024 Q1-Q4 | 4/4 | Completo |
| 2025 Q1-Q4 | 4/4 | Completo |
| 2026 (parcial) | 26 (con churn, ver diagnóstico) | En curso, posible bug de re-generación de ventanas |
| **TOTAL** | **62** | **2015-2016 son el hueco real; 2017-2025 completos** |

> A pesar de que 2017-2025 muestran ventanas "completas", casi ningún artículo
> real de esos años ha llegado a `sources/articles/` (la mayoría del contenido
> descargado viene de la fuente DDG contaminada, no de GDELT). Recomendación:
> priorizar `fetch-historical --years 2015-2016 --mode gdelt` en la próxima
> sesión de mantenimiento para cerrar el hueco real de cobertura.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-05 | 0 reales / 16 falsos positivos descartados | 0 | Root-cause fix de fetch_ddg_search() + 2 bugs en ingest.py; ver wiki/log.md |

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
