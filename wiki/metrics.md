---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-16
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 22 | ↑ continuo |
| Artículos reales ingestados (con página en wiki/) | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 16 (7 previos + 9 hoy) | **0 nuevos** |
| Páginas en wiki/ | 20 (8 topics, 3 entities, 6 summaries, 3 overview) | ↑ continuo |
| Cobertura temporal real | 2017-Q2 → 2026-Q2 (GDELT) + semilla manual | 2015-02-19 → hoy |
| Ventanas GDELT completadas | 49 (≥45 → **rango agotado**, faltan 2015→2017-Q1) | cobertura 2015→hoy |
| Días sin artículos nuevos reales al wiki | ~53 (desde semilla 2026-05-24) | máx 3 antes de diagnosticar |

**Alerta activa**: desde la semilla manual del 2026-05-24, el fetch automático diario
no ha aportado ningún artículo real al wiki — el 73% de lo descargado (16/22) vino de
la fuente `prensa_agro` (DDG search) rota, y el 100% de esos 16 fueron falsos
positivos. Ver diagnóstico completo y fix en `wiki/log.md` (entrada 2026-07-16).

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-15 (commit "1 artículos nuevos descargados")
Resultado              : 1 artículo descargado — resultó ser falso positivo
                         (fuente prensa_agro/DDG, ver causa raíz abajo)
Causa raíz identificada : fetch_ddg_search() arma la query como "site:prensa.com ..."
                         pero DDG no respeta el operador site: en su backend de
                         noticias → devuelve artículos de dominios no relacionados
                         con Panamá que matchean términos genéricos (MIDA, agricultura).
                         fetch_rss() sí tenía filtro de dominio/Panamá; fetch_ddg_search()
                         no lo tenía.
Fix aplicado (2026-07-16): _domain_matches_site() + _is_blocked_domain() ahora se
                         aplican también en fetch_ddg_search() (scripts/fetch_news.py).
                         Bug adicional corregido: mark_ingested() en scripts/ingest.py
                         crasheaba con _gdelt_windows (lista) en processed.json.
Estado post-fix         : Pendiente validación en próxima corrida Actions (2026-07-16
                         cron ~11:00 UTC). Si prensa_agro sigue trayendo 0 artículos
                         reales tras el fix, revisar si La Prensa cambió su feed/dominio.
GDELT backfill          : 49 ventanas completadas, faltan 2015-02-19→2017-Q1 (~9
                         ventanas). GDELT solo es alcanzable desde runners de GH
                         Actions (confirmado: ProxyError 403 al probar localmente).
                         Acción pendiente: disparar workflow "Crawl Histórico 15 Años"
                         con years=2015-2017, mode=gdelt.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

> Corregido 2026-07-16: la tabla anterior decía "0/46 no iniciado", pero
> `processed.json._gdelt_windows` ya registra 49 ventanas completadas. Reconciliado
> con los datos reales del archivo.

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Pendiente — hueco de cobertura** |
| 2017 Q1 | 0/1 | 0 | **Pendiente — hueco de cobertura** |
| 2017 Q2-Q4 → 2026 Q2 | 36/36 | 0 confirmados (todo vía DDG roto) | Ventanas marcadas completas, sin artículos reales verificados |
| 2026-06-18 → 2026-07-14 | 13 ventanas diarias/solapadas | ver nota | Posible duplicación — misma fecha de inicio, fin incremental día a día; no son trimestres reales, no revisado a fondo |
| **TOTAL** | **49/~50** | **0 vía GDELT** | **Rango 2017-Q2→hoy "agotado" pero sin artículos reales; falta 2015→2017-Q1 y limpiar ventanas duplicadas de 2026-06** |

> GDELT solo es alcanzable desde runners de GitHub Actions (ProxyError 403 confirmado
> en sesión local 2026-07-16). Próxima acción: correr el workflow "Crawl Histórico 15
> Años" (years=2015-2017, mode=gdelt) para cerrar el hueco inicial, y revisar por qué
> ninguna de las 36 ventanas trimestrales 2017-2026 produjo un artículo real (posible
> causa: GDELT devuelve 0 resultados para la query, o el filtro Panamá descarta todo).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-07-16 | 0 (9/9 falsos positivos) | 0 | Causa raíz encontrada y corregida: `fetch_ddg_search()` sin filtro de dominio/Panamá (fix en `scripts/fetch_news.py`); bug de `mark_ingested()` con `_gdelt_windows` corregido (`scripts/ingest.py`). Ver `wiki/log.md`. |

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
