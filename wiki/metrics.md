---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-07-24
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 24 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 18 | **0 nuevos** (11 detectados y documentados hoy) |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 54 / ~45 estimadas | rango agotado — necesita expansión |
| Días sin artículos nuevos | 4 (desde 2026-07-20) | máx 3 antes de diagnosticar — **ALARMA** |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-07-24 (corrió correctamente, 0 artículos nuevos)
Resultado 07-20→07-24  : 2, 0, (sin log 07-22), 0, 0 artículos nuevos por día
Ventanas GDELT          : 54 completadas, ≥ 45 estimadas → rango 2015→hoy ya cubierto,
                          se necesita ampliar el rango objetivo o las queries GDELT para
                          seguir encontrando artículos nuevos
Causa de los 0 reales   : de los 11 artículos que llegaron a sources/ esta sesión, los 11
                          fueron falsos positivos — el pipeline de "prensa.com" (RSS/
                          búsqueda genérica) hace match por palabras clave ("MIDA",
                          "agriculture") sin filtro geográfico de Panamá, trayendo
                          contenido de Utah, Malasia, Arabia Saudita, Irán, Brasil, etc.
Acción recomendada      : (1) ampliar/redefinir ventanas GDELT si aún hay huecos en
                          2015-2026; (2) agregar filtro de país/dominio a la fuente
                          "prensa.com" en scripts/fetch*.py para reducir falsos positivos
                          (detalle completo en wiki/log.md 2026-07-24)
Estado                  : Pendientes de ingesta = 0, pero cobertura real de Panamá no
                          avanzó esta sesión — requiere intervención en el código de fetch
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
| 2026-07-24 | 0 | 0 | 11 falsos positivos detectados y documentados (0 ingestados reales) + fix de bug en mark_ingested() |

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
