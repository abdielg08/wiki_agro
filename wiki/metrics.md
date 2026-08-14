---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-08-14
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 29 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 12 (7 previos + 5 nuevos 2026-08-14) | **0 nuevos** ⚠️ ver diagnóstico |
| Pendientes de ingesta | 11 (todos pre-confirmados falsos positivos, ver log 2026-08-14) | 0 |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 52 trimestrales + 14 diarias | 45 (2015→hoy) |
| Días sin artículos nuevos legítimos | ~15 días (último real: 2026-07-30, luego confirmado falso positivo) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-13 (diaria, corre bien — commit "0 artículos nuevos")
Resultado               : Fetch técnicamente funcional, pero desde ~2026-07-29 el 100%
                          de lo que trae son falsos positivos (0 artículos panameños reales)
Causa raíz identificada : scripts/fetch_historical.py:64-67 y scripts/fetch_news.py — la
                          query GDELT usa "MIDA" como término OR suelto, sin exigir contexto
                          panameño. "MIDA" colisiona con Malaysian Industrial Development
                          Authority, Military Installation Development Authority (Utah,
                          EEUU), etc. El filtro sourcecountry:PA de GDELT no bloquea estos
                          resultados (se colaron artículos de Arabia Saudita, Utah, Malasia,
                          España, Brasil, IEEE, UNESCO). Además el pipeline hardcodea
                          source="prensa.com", language="es", country="PA" en TODO artículo
                          de GDELT sin verificar el dominio real, ocultando el origen real
                          (23/29 artículos descargados figuran como "prensa.com" sin serlo).
Fix aplicado esta sesión : Ninguno al pipeline (requiere decisión del usuario). Se marcó
                          como procesado el lote de 5 falsos positivos para liberar la cola.
                          Diagnóstico completo en wiki/log.md 2026-08-14.
Fix recomendado (pendiente de aprobación del usuario):
  a. Quitar "MIDA" suelto de _AGRO_QUERY, o exigir coocurrencia con "Panamá"/"panameño".
  b. No confiar solo en sourcecountry:PA — validar dominio real contra allowlist de
     fuentes panameñas antes de guardar.
  c. Dejar de hardcodear source/language/country; extraerlos del artículo real.
Estado post-diagnóstico : Backfill efectivamente estancado (0 artículos panameños nuevos
                          desde finales de julio 2026) hasta aplicar el fix arriba.
```

---

## Progreso del Backfill GDELT (2015 → hoy)

| Período | Ventanas | Artículos | Estado |
|---------|----------|-----------|--------|
| 2015 Q1-Q4 | 0/4 | 0 | **Gap — no cubierto** (ventana más antigua completada empieza 2017-03-30) |
| 2016 Q1-Q4 | 0/4 | 0 | **Gap — no cubierto** |
| 2017 Q1-Q4 | 3/4 | 0 legítimos | Cubierto desde Q2 — 0 artículos panameños reales |
| 2018 Q1-Q4 | 4/4 | 0 legítimos | Cubierto — 0 artículos panameños reales |
| 2019 Q1-Q4 | 4/4 | 0 legítimos | Cubierto |
| 2020 Q1-Q4 | 4/4 | 0 legítimos | Cubierto |
| 2021 Q1-Q4 | 4/4 | 0 legítimos | Cubierto |
| 2022 Q1-Q4 | 4/4 | 0 legítimos | Cubierto |
| 2023 Q1-Q4 | 4/4 | 0 legítimos | Cubierto |
| 2024 Q1-Q4 | 4/4 | 0 legítimos | Cubierto |
| 2025 Q1-Q4 | 4/4 | 0 legítimos | Cubierto |
| 2026 Q1-Q3 | ~17 ventanas (trimestrales + catch-up diario) | 5 (todos falsos positivos) | Cubierto |
| **TOTAL** | **52/46 trimestrales completadas** | **0 artículos panameños reales vía GDELT** | **Ventanas "completas" pero la query no encuentra artículos panameños — ver causa raíz arriba** |

> Hallazgo clave: las ventanas GDELT 2017-2026 ya se completaron (52 ≥ 46 estimadas), pero
> devolvieron 0 artículos panameños legítimos — todo lo recibido fue falso positivo. El
> backfill no avanza por falta de ventanas, sino por la query rota (ver "Estado del Fetch").
> Falta además cubrir 2015-02-19 → 2017-03-29 (~8 trimestres sin ventana registrada).

---

## Historial de Sesiones de Routine

| Fecha | Artículos ingestados | Pendientes restantes | Nota |
|-------|---------------------|----------------------|------|
| 2026-05-24 | 6 (semilla manual) | 0 | Datos semilla iniciales — no son fetches automáticos |
| 2026-06-22 | 0 | 0 | Auditoría + fix de 7 falsos positivos + reset GDELT windows |
| 2026-08-14 | 0 (5 falsos positivos marcados como procesados) | 11 (todos confirmados falsos positivos) | Diagnóstico de causa raíz: query GDELT con "MIDA" suelto + sourcecountry:PA no filtra + labels hardcodeados. Ver wiki/log.md y "Estado del Fetch" arriba. |

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
