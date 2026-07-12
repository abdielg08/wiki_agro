---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-12
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 20 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 14 (7 el 2026-06-22 + 7 el 2026-07-12) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 48 / ~47 estimadas | cobertura completa 2015→hoy |
| Días sin artículos nuevos | 0-2 (última corrida Actions: 2026-07-11, 0 nuevos) | máx 3 antes de diagnosticar |

> **Alerta**: cero artículos genuinos sobre agro panameño desde la carga
> semilla (2026-05-24). Las 20 descargas acumuladas desde entonces se
> dividen en 6 reales (semilla) + 14 falsos positivos. El fetch automático
> lleva 7 semanas sin producir contenido real ingestable. Ver diagnóstico
> completo en `wiki/log.md` (entrada 2026-07-12).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-11 11:45 UTC (exitosa, 0 artículos nuevos)
Resultado              : 0 artículos nuevos guardados
Causa identificada     : GDELT bloqueado (403/429 + timeouts) en CADA ventana
                         intentada ese día: las 8 ventanas más antiguas sin
                         completar (2015-01-01 → 2017-03-29) Y la ventana más
                         reciente (2026-06-18 → 2026-07-10). Las ~39 ventanas
                         intermedias ya estaban completas de corridas previas.
                         RSS (IICA, La Prensa) devolvió 0 entradas ese día.
                         DDG por dominio (mida.gob.pa, idiap.gob.pa, oirsa.org,
                         fao.org, bancomundial.org, iica.int) → "No results
                         found" — no ha producido artículos hasta ahora.
Fix aplicado 2026-06-22 : fetch_gdelt_historical() limita end a datetime.utcnow()-1d;
                          ventanas GDELT reseteadas a [] para backfill real
Fix aplicado 2026-07-12 : fetch_ddg_search() ahora verifica que la URL devuelta
                          pertenezca realmente al dominio pedido en site: —
                          causa raíz de los 7 falsos positivos de hoy (DDG
                          devolvía resultados de dominios no solicitados:
                          sltrib.com, spa.gov.sa, nyfb.org, whc.unesco.org,
                          todos etiquetados incorrectamente como prensa.com/PA)
Pendiente               : (1) GDELT sigue bloqueado en ambos extremos del
                          backfill — evaluar reordenar ventanas (más reciente
                          primero) y/o necesidad de API key; (2) confirmar si
                          las búsquedas DDG por dominio alguna vez funcionan
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Estado |
|---------|--------|
| 2015 Q1 – 2017 Q1 (~8 ventanas) | **Bloqueado** — GDELT devuelve timeout/403 en cada corrida, reintentado a diario sin éxito |
| 2017 Q2 – 2026 Q2 (~39 ventanas) | Completas (0 artículos agro-PA reales encontrados vía GDELT en estas ventanas) |
| Ventana actual (2026-06-18 → hoy) | **Bloqueado** — mismo timeout/403, no logra capturar noticias recientes |
| **TOTAL** | **48 ventanas marcadas completas / 0 artículos reales aportados por GDELT** |

> GDELT ha completado casi todo el rango 2015→hoy, pero **no ha aportado ni
> un solo artículo real** al wiki — los 6 artículos genuinos vienen de la
> carga semilla manual, no de GDELT/RSS/DDG automatizados. Los dos extremos
> del backfill (2015-2017 Q1 y la ventana más reciente) siguen bloqueados por
> GDELT de forma persistente. Ver diagnóstico en `wiki/log.md` 2026-07-12.

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-12 | 0 | 0 | Auditoría + rechazo de 7 falsos positivos (bug en fetch_ddg_search corregido) + fix de mark_ingested() + diagnóstico de bloqueo GDELT persistente |

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
