---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-15
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 23 | **0 nuevos** |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 36 útiles / ~46 estimadas (+32 entradas corruptas, ver abajo) | 46 (2015→hoy) |
| Días sin artículos nuevos | 16 (última descarga real: 2026-07-30) | máx 3 antes de diagnosticar — EXCEDIDO |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-15 — 0 artículos nuevos (9na corrida consecutiva en 0)
Última descarga real   : 2026-07-30 (3 artículos) → 16 días sin avance real

CAUSA RAÍZ #1 (crítica, corregida hoy):
  fetch_gdelt_historical() en scripts/fetch_news.py truncaba la ventana final
  con `next_q = min(current + 90d, end)`, donde `end` = ayer. Como `end` avanza
  un día en cada corrida, la clave de esa ventana final (embebe la fecha de
  fin) nunca se repite, así que nunca se marca completa — la routine reintentaba
  una ventana "cola" cada vez más grande desde 2026-06-18 sin avanzar nunca el
  backfill real. Evidencia en processed.json["_gdelt_windows"]: 32 entradas
  "20260618_2026XXXX" con fecha de fin distinta cada día, en vez de una sola
  ventana trimestral limpia.
  FIX: ahora solo se procesan ventanas completas de 90 días
  (`while current + 90d <= end`), dejando el tramo reciente (menos de 90 días)
  a los fetchers RSS/DDG diarios, que sí cubren noticias recientes.

CAUSA RAÍZ #2 (falsos positivos, corregida hoy):
  fetch_ddg_search() no verificaba que el dominio del resultado coincidiera con
  el `site:` solicitado ni aplicaba _is_blocked_domain(). El query "prensa_agro"
  (agropecuario OR agricultura OR ganadería OR MIDA OR cosecha) devolvía noticias
  agrícolas globales de cualquier país, etiquetadas como prensa.com/PA por
  defecto. 23/29 artículos descargados en total tenían esta etiqueta falsa.
  FIX: fetch_ddg_search() ahora exige que el dominio real contenga el `site`
  configurado y aplica _is_blocked_domain(). Ver wiki/log.md 2026-08-15.

GAP SIN EXPLICAR (pendiente de investigar — no se pudo verificar desde este
  sandbox porque el proxy de red bloquea api.gdeltproject.org, error 403):
  Ninguna ventana GDELT de 2015-01-01 a 2017-03-29 (9 trimestres) aparece como
  completada en processed.json, pese a que la routine corre 3x/día desde hace
  meses. O GDELT no tiene cobertura sourcecountry:PA para ese rango (plausible:
  CLAUDE.md ya documenta "2015-02-19 → hoy" como límite real de GDELT v2), o
  las llamadas fallan silenciosamente (network error, no se marcan completas y
  se reintentan cada corrida sin éxito). Requiere revisar logs reales de
  GitHub Actions para diferenciar ambos casos.

Estado post-fix         : Pendiente validación en la próxima corrida real de Actions.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas completadas | Estado |
|---------|----------------------|--------|
| 2015 Q1 – 2017 Q1 | 0/9 | **Sin cobertura — causa por confirmar (ver Estado del Fetch)** |
| 2017 Q2 – 2026 Q2 | 36/36 | Completo (ventanas trimestrales limpias, verificado en processed.json) |
| 2026 Q3 (parcial, <90 días) | 0/1 | Pendiente — se completará automáticamente cuando pasen 90 días (fix de hoy) |
| **TOTAL** | **36/46** | **Backfill activo; bloqueado en 2015–2017 y sin avance desde 2026-07-30 por el bug de ventana-cola (corregido hoy)** |

> 32 entradas corruptas "20260618_2026XXXX" en processed.json (previas al fix de hoy)
> quedan como residuo inofensivo — el nuevo código nunca las reutiliza porque calcula
> claves alineadas a límites fijos de 90 días desde 2015-01-01, no desde `end`.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Falsos positivos | Pendientes restantes | Nota |
|-------|---------------------|-------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 7 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-15 | 0 | 16 | 0 | Cola 100% contaminada por bug de fetch_ddg_search (corregido). Diagnosticado y corregido bug de ventana-cola GDELT (0 artículos nuevos desde 2026-07-30). |

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
