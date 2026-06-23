---
title: "Dashboard de Métricas — Wiki Agropecuario"
type: overview
last_updated: 2026-06-23
---

# Dashboard de Métricas

> Actualizado automáticamente por cada routine. La routine DEBE actualizar este archivo en cada sesión.

---

## Estado Actual

| Métrica | Valor | Meta |
|---------|-------|------|
| Artículos en sources/ | 13 | ↑ continuo |
| Artículos reales ingestados | 6 | = total sin falsos positivos |
| Falsos positivos acumulados | 7 | **0 nuevos** |
| Páginas en wiki/ | 20 | ↑ continuo |
| Cobertura temporal | 2015-2026 (semilla) | 2015 → hoy real |
| Ventanas GDELT completadas | 0 / ~46 estimadas | 46 (2015→hoy) |
| Días sin artículos nuevos | 4 (desde 2026-06-19) | máx 3 antes de diagnosticar |

---

## Estado del Fetch (GitHub Actions)

```
Última corrida Actions : 2026-06-22T15:47Z (run #27 de 27 totales)
Resultado              : success — 0 artículos nuevos (no commit a sources/)
Último artículo en sources/ : 20260607_prensacom_document-11018750.json (2026-06-19, falso positivo)
Días sin artículos nuevos   : 4 (⚠ supera umbral de 3 → ALERTA)
Corrida de hoy (2026-06-23) : Aún no ha corrido (cron 11:00 UTC)

Causa raíz del problema     : 
  1. "MIDA" como término de búsqueda en DDG captura Malaysian Investment Dev Authority
  2. El filtro site:prensa.com de DDG no es estricto → retorna thestar.com.my, etc.
  3. _is_panama_related() no rechaza URLs sin dominio .pa explícito cuando el título
     tampoco menciona "Panamá" o "panameño"
  4. GDELT backfill: _gdelt_windows=[] — aún no ha procesado ninguna ventana histórica
     El fix (limitar end a now-1d) es correcto pero needs validation en próxima corrida

Fix aplicado (2026-06-22) : fetch_gdelt_historical() limita end a datetime.utcnow()-1d
                             Ventanas GDELT reseteadas a [] para backfill real
Estado post-fix            : Una corrida post-fix (2026-06-22) produjo 0 artículos
                             → el fix no rompió nada pero GDELT tampoco entregó artículos aún
Próximos pasos             : Monitorear corrida de hoy; si sigue en 0 → revisar fetch_gdelt_historical
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
| 2026-06-23 | 0 | 0 | Diagnóstico pipeline: 4 días sin artículos nuevos, GDELT sin iniciar |

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
