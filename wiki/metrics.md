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
| Falsos positivos acumulados | 23 (7 previos + 16 esta sesión) | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 66 (ver nota de calidad abajo) | 47 limpias (2015→hoy) |
| Días sin artículos nuevos | 15 (desde 2026-07-30) | máx 3 antes de diagnosticar — **ALARMA ACTIVA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-08-13 (corre a diario, confirmado por historial de commits)
Resultado               : 0 artículos nuevos en cada corrida desde 2026-07-31 (15 días)
Causa raíz identificada (2026-08-14):
  1. fetch_ddg_search() no validaba que las URLs devueltas por DDGS().news()
     pertenecieran al dominio `site:` solicitado. Las 16 entradas pendientes
     de "prensa.com" NO eran de prensa.com (paultan.org, sltrib.com, heraldo.es,
     msn.com, archive.org, ieeexplore.org, nyfb.org, spa.gov.sa, agenciabrasil.ebc.com.br,
     whc.unesco.org). 0/23 artículos históricos de esa fuente eran reales.
     FIX APLICADO: verificación de dominio (urlparse) en fetch_ddg_search —
     descarta resultados fuera del dominio configurado.
  2. is_agro_relevant() acepta cualquier término genérico (agricultura, cultivo,
     MIDA) sin exigir contexto Panamá — colisiona con MIDA Malasia/Utah.
     NO corregido esta sesión (el fix #1 ya elimina el 100% de los falsos
     positivos observados; revisar si reaparecen dentro del dominio correcto).
  3. Ventanas GDELT: 66 "completadas" pero solo 47 ventanas trimestrales limpias
     cubren 2015→hoy. 10 ventanas de 2015-2017 siguen sin completar pese a
     meses de corridas diarias; 29 ventanas son variantes duplicadas de una
     sola ventana abierta (inicio 2026-06-18) con fecha de cierre dinámica
     distinta cada día — el backfill está atascado re-consultando el mismo
     rango reciente en vez de avanzar sobre 2015-2017.
     NO corregido esta sesión (requiere pruebas contra API real de GDELT) —
     pendiente para sesión de ingeniería dedicada.
Estado post-fix         : Fix de dominio pendiente de validación en próxima
                          corrida de Actions (2026-08-15 6am Panamá).
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
| 2026-08-14 | 0 | 0 | 16 falsos positivos detectados y descartados (fuente prensa_agro). Fix de dominio en fetch_ddg_search + fix de bug en mark_ingested. Diagnóstico de ventanas GDELT atascadas documentado (ver Estado del Fetch). |

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
