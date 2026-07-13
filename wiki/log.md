---
title: Log de Actividad del Wiki
type: overview
tags: [log, actividad]
last_updated: 2025-05-24
---

# Log de Actividad

> Registro cronológico append-only de ingestas, consultas y operaciones de mantenimiento.

---

## 2025-05-24 00:00
INIT: Wiki Agropecuario de Panamá inicializado
  Estructura: topics/, entities/, summaries/, index.md, log.md
  Metodología: Karpathy LLM Wiki (3 capas: sources → wiki → schema)
  Cobertura objetivo: noticias agropecuarias de Panamá 2015–2025
  Fuentes configuradas: MIDA, IDIAP, BDA, IICA, FAO, La Prensa, Panamá América, TVN, La Estrella
  Método histórico: GDELT API (gratuito, sin clave, cobertura 2015–2025)

## 2026-05-24 13:38
LINT: 8 páginas revisadas, 39 issues encontrados
  frontmatter:0, huérfanas:0, broken_links:39, stale:0, no_index:0

## 2026-05-24 15:04
LINT: 8 páginas revisadas, 39 issues encontrados
  frontmatter:0, huérfanas:0, broken_links:39, stale:0, no_index:0

## 2026-05-24 16:00
INGEST: 6 artículos semilla procesados (sesión Claude Code — metodología Karpathy)
  Artículos:
    - 20230915_mida_produccion-arroz-panama-2023 → summaries/ + topics/arroz.md actualizado
    - 20180620_laprensaeco_gusano-cogollero-crisis-maiz-2018 → summaries/ + topics/maiz.md creado + topics/plagas_enfermedades.md actualizado
    - 20160301_tvnnoticias_sequia-azuero-nino-2015-2016 → summaries/ + topics/cambio_climatico.md actualizado
    - 20220410_iica_platano-banano-exportaciones-fusarium → summaries/ + topics/platano_banano.md actualizado + topics/plagas_enfermedades.md actualizado
    - 20210815_bda_credito-agropecuario-pandemia-2020-2021 → summaries/ + topics/credito_financiamiento.md creado + entities/bda.md actualizado
    - 20240305_mida_politica-agropecuaria-mulino-2024 → summaries/ + topics/politicas_agropecuarias.md creado + entities/mida.md actualizado
  Páginas creadas: maiz.md, credito_financiamiento.md, politicas_agropecuarias.md
  Páginas actualizadas: arroz.md, plagas_enfermedades.md, cambio_climatico.md, platano_banano.md, mida.md, bda.md
  Summaries: 6 nuevos archivos en wiki/summaries/

## 2026-05-24 22:58
INGEST: 6 artículos marcados como ingestados por sesión Claude Code

## 2026-05-27 00:00
MAINTENANCE: Verificación automática de artículos pendientes
  Sin artículos pendientes — 6/6 artículos ya ingestados
  Total páginas wiki: 19 (8 topics, 3 entities, 6 summaries, 2 overview)
  Fuentes con cobertura: MIDA (2), TVNNoticias (1), LaPrensaEco (1), BDA (1), IICA (1)

## 2026-07-13 00:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-13 (sesión routine)
INGEST: 0 artículos nuevos al wiki — 8 pendientes revisados, los 8 son FALSOS POSITIVOS
  Artículos rechazados (ninguno es sobre agro panameño):
    - sltrib.com "Box Elder data center opponents..." (Utah, MIDA=Military Installation Development Authority)
    - sltrib.com "Utah Gov. Cox issues order to protect Great Salt Lake..." (Utah)
    - sltrib.com "Timeline: Kevin O'Leary data center plan..." (Utah)
    - sltrib.com "Utah wants to process uranium on the Wasatch Front..." (Utah)
    - whc.unesco.org "The Persian Qanat" (Irán, sistema de riego histórico)
    - nyfb.org "New York Farm Bureau" (EE.UU.)
    - spa.gov.sa "'Reef Saudi'..." (Arabia Saudita)
  Los 8 fueron marcados `ingested: true` en processed.json (revisados y descartados,
  no reintentar) pero NO generaron páginas de wiki.

BUG ENCONTRADO Y CORREGIDO (scripts/ingest.py):
  1. `mark_all_ingested()` seleccionaba los "primeros N pendientes" por orden de
     archivo (find_pending), pero `ingest` (run_prepare) selecciona por score de
     prioridad (prioritize.py). Los dos conjuntos no coinciden. Esta sesión,
     `mark-all-ingested --limit 5` marcó como ingestado
     https://www.nyfb.org/ (New York Farm Bureau) — un artículo que Claude
     NUNCA vio ni revisó. Se revirtió (ingested: false) y se corrigió la función
     para usar la misma ordenación por score que `ingest`.
  2. `mark_ingested()` (comando individual, el que pending_ingest.md le indica
     ejecutar a Claude) crasheaba con AttributeError al iterar processed.json
     crudo, porque la clave interna `_gdelt_windows` (una lista) no se filtraba
     como en `article_entries()`. Corregido para usar `article_entries()`.

DESCUBRIMIENTO: 6 falsos positivos previos (de sesiones anteriores) estaban
  marcados `ingested: true` sin haber sido documentados como falso positivo en
  este log — probablemente víctimas del mismo bug #1 en sesiones pasadas:
    - thestar.com.my "Mida welcomes Tengku Zafrul's appointment..." (Malasia,
      MIDA=Malaysian Investment Development Authority)
    - thestar.com.my "MIDA sees broader investment pipeline..." (Malasia)
    - thestar.com.my "Malaysia should reform, recalibrate..." (Malasia)
    - fox13now.com "MIDA violated state law..." (Utah)
    - worldbank.org "Development Topics" (página genérica, no un artículo)
    - ieeexplore.ieee.org "3D-Printed Worm-Like Robot for Corrugated Pipes..."
      (paper de robótica, sin relación con agro)
  No se modificó su estado (ya están correctamente excluidos del wiki); se
  documentan aquí para dejar registro del alcance real del problema.

DIAGNÓSTICO — CAUSA RAÍZ (los 14 artículos descargados desde 2026-05-24 son
  100% falsos positivos; CERO artículos reales de agro panameño han llegado
  en ~7 semanas):
  1. La búsqueda web `prensa_agro` (config/sources.yaml, DuckDuckGo vía `ddgs`)
     usa `site:prensa.com` pero la librería `ddgs` NO respeta ese operador de
     forma confiable — se colaron resultados de sltrib.com, nyfb.org,
     spa.gov.sa, whc.unesco.org, thestar.com.my, fox13now.com, worldbank.org,
     ieeexplore.ieee.org, todos etiquetados incorrectamente como
     source="prensa.com", country="PA".
  2. El filtro `is_agro_relevant()` (scripts/fetch_news.py) hace un simple
     substring match case-insensitive. El término español "agricultura" es
     substring literal de la palabra inglesa "agricultural", por lo que
     CUALQUIER artículo en inglés sobre agricultura global pasa el filtro.
     El término "MIDA" (genérico, sin contexto) también matchea instituciones
     homónimas en Malasia y Utah que no tienen relación con Panamá.
  FIX APLICADO (bajo riesgo, contenido):
    - scripts/fetch_news.py: `fetch_ddg_search()` ahora valida que el dominio
      real de la URL devuelta contenga el `site` configurado antes de aceptar
      el resultado (descarta resultados fuera de dominio).
    - config/sources.yaml: query de `prensa_agro` reagrupada para requerir
      "Panamá" junto con un término temático:
      `"Panamá (agropecuario OR agricultura OR ganadería OR MIDA OR cosecha)"`
  PENDIENTE (fuera de alcance de esta sesión, requiere validación con red real):
    - Confirmar en la próxima corrida de GitHub Actions que `prensa_agro`
      empieza a devolver artículos reales de prensa.com sobre Panamá.
    - Revisar si `is_agro_relevant()` necesita requerir explícitamente
      "panamá"/"panama" en el texto para los demás fetchers (RSS/GDELT),
      balanceando contra el riesgo de excluir artículos legítimos que no
      mencionen "Panamá" literalmente (p.ej. IDIAP/MIDA hablando de una
      variedad de semilla sin nombrar el país).

GDELT: `_gdelt_windows` = 48 ventanas completadas (≥45 → umbral de "rango agotado"
  de CLAUDE.md). Verificado: 48 ventanas trimestrales de 90 días desde 2015-01-01
  hasta hoy (2026-07-13) es matemáticamente el total esperado (~11.5 años × 4).
  Esto NO es una falla — el backfill histórico ya cubrió 2015→hoy por completo.
  GDELT no traerá ventanas nuevas hasta que avance el calendario (nueva ventana
  cada ~90 días). El estancamiento real de artículos nuevos viene 100% de la
  causa raíz de falsos positivos arriba (prensa_agro), no de GDELT.
