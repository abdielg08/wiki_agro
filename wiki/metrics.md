---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-20
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 30 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 24 (todos rechazados) | **0 nuevos** |
| Pendientes de ingesta | 0 | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2016-2024 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~46 (reseteadas) | 46 (2015→hoy) |
| Días sin artículos reales | ~88 (desde 2026-05-24) | máx 3 antes de diagnosticar |

> **El wiki en sí mantiene 0% de falsos positivos**: los 24 artículos irrelevantes
> nunca generaron página. La contaminación estaba solo en la contabilidad de
> `processed.json`, ahora corregida con el estado `rejected`.

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-20
Resultado              : 0 artículos nuevos (patrón sostenido desde mayo)
Causa raíz #1 (GDELT)  : sourcecountry:PA — en FIPS 10-4 "PA" es PARAGUAY.
                         Panamá es "PM". Las 71 ventanas crawleadas entre
                         junio y agosto consultaron Paraguay → 0 resultados.
Causa raíz #2 (GDELT)  : el filtro exigía un término "Panamá" en el TITULAR,
                         redundante sobre sourcecountry y letal para el recall:
                         la prensa doméstica no nombra al país en sus títulos.
Causa raíz #3 (DDG)    : el endpoint de noticias ignora el operador `site:`, y
                         el código no verificaba el dominio ni aplicaba los
                         guardas _is_blocked_domain/_is_panama_related que sí
                         usan las rutas RSS y GDELT. Origen de los 24 falsos
                         positivos, todos etiquetados como "prensa.com".
Causa raíz #4 (filtro) : is_agro_relevant hacía match por subcadena, así que
                         "MIDA" disparaba con "comida", "medida", "temida".

Fix aplicado (2026-08-20):
  - sourcecountry:PM en fetch_news.py y fetch_historical.py + config
  - GDELT: se sustituye el filtro de titular por relevancia agro
  - DDG: se verifica el dominio real, se aplican ambos guardas y se etiqueta
    la fuente con el dominio efectivo en vez del `site` solicitado
  - is_agro_relevant pasa a match por palabra completa
  - Ventanas GDELT reseteadas (las 71 previas apuntaban a Paraguay)
  - Nuevo estado `rejected` + comando `mark-rejected` para falsos positivos

Estado post-fix        : Pendiente validación en la próxima corrida de Actions.
                         El sandbox de la routine no alcanza GDELT/RSS/DDG
                         (egress bloqueado), así que la validación en vivo
                         solo puede ocurrir en GitHub Actions.
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
| 2026-08-20 | 0 | 0 | Causa raíz del backfill muerto: `sourcecountry:PA` = Paraguay. 24 falsos positivos rechazados; 4 bugs de filtrado corregidos |

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
