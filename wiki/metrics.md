---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-25
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 22 | **0 nuevos** ⚠️ ver diagnóstico |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 55 / ~45 estimadas | 45 (2015→hoy) — **agotado** |
| Días sin artículos nuevos (reales) | 5 (desde 2026-07-20) | máx 3 antes de diagnosticar ⚠️ **FALLA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-25 (commit ddc65e2, "0 artículos nuevos")
Resultado               : 0 artículos nuevos reales en los últimos 5 días hábiles
                          (2026-07-21, 07-23, 07-24, 07-25 = 0; 07-22 sin corrida)
                          → excede el umbral de 3 días — SISTEMA EN FALLA

DIAGNÓSTICO (2026-07-25):

1) Ventanas GDELT: 55/45 completadas → RANGO DE FECHAS AGOTADO.
   Causa raíz probable de por qué ya no llegan artículos reales nuevos:
   GDELT ya fue recorrido para todo el rango 2015→hoy bajo la
   configuración de ventanas actual. Se requiere EXPANSIÓN del rango
   o de las queries (más keywords/sinónimos agro) para seguir
   descubriendo artículos panameños nuevos.

2) CONTAMINACIÓN DE FUENTE "prensa.com" (hallazgo nuevo, crítico):
   De los 24 artículos descargados, 18 están etiquetados como fuente
   "prensa.com". Esta sesión evaluó los 15 pendientes restantes de esa
   cola y las 15 resultaron ser FALSOS POSITIVOS — ninguno sobre agro
   de Panamá. Dominios encontrados bajo la etiqueta "prensa.com":
     paultan.org (Malaysia/MITI), thestar.com.my (Malaysia/MIDA),
     sltrib.com (Utah/MIDA — autoridad de desarrollo militar),
     fox13now.com (Utah/MIDA), whc.unesco.org (Irán/qanat),
     nyfb.org (NY Farm Bureau, EE.UU.), msn.com (viajes),
     worldbank.org (página genérica sin artículo), ieeexplore.ieee.org
     (papers técnicos), spa.gov.sa (Arabia Saudita), archive.org
     (catálogo de dípteros).
   Patrón común: el matching parece basarse en coincidencia de la
   sigla "MIDA" (o similar) sin verificar que se trate del Ministerio
   de Desarrollo Agropecuario de Panamá, ni el país/idioma del
   artículo. RECOMENDACIÓN: revisar el fetcher de "prensa.com" en
   scripts/ (o la query GDELT que alimenta esa etiqueta) para:
     a. Filtrar por dominio/país Panamá explícitamente
     b. Evitar match ciego de "MIDA" sin contexto ("Panamá",
        "Ministerio de Desarrollo Agropecuario", etc.)
   Sin este fix, cada sesión seguirá gastando su cupo de ingesta
   evaluando y descartando ruido en vez de avanzar cobertura real.

3) RSS IICA y La Prensa: no se evaluaron fuentes nuevas de estas
   fuentes en esta sesión (no había pendientes con esa etiqueta);
   sin cambios respecto al diagnóstico previo.

Estado post-diagnóstico : Pendiente que una sesión con acceso a
                          scripts/ ajuste el filtro de fetch de
                          "prensa.com" y expanda/repita ventanas GDELT.
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
| 2026-07-25 | 0 (15/15 evaluados = falsos positivos) | 0 | Cola de pendientes destrabada. Diagnóstico: GDELT agotado (55/45 ventanas) + fuente "prensa.com" contaminada con contenido no panameño — ver "Estado del Fetch" |

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
