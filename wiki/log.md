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

## 2026-07-18 16:03
INGEST: routine automática — 5 pendientes revisados, 0 ingestados, 5 falsos positivos
  Los 5 artículos del lote NO son sobre agro panameño. Ninguno fue ingestado
  al wiki (schema CLAUDE.md regla 9). Marcados como procesados vía
  mark-all-ingested para no bloquear la cola de pendientes.

  Falsos positivos detectados:
    1. "MITI working on simplified NCM..." (paultan.org) — sobre MITI/MIDA de
       Malasia (Ministry of Investment, Trade and Industry), no Panamá.
    2. "Box Elder data center opponents..." (sltrib.com) — MIDA = Military
       Installation Development Authority de Utah, EE.UU.
    3. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com)
       — mismo MIDA de Utah, sin relación con Panamá.
    4. "Timeline: How the Kevin O'Leary data center plan..." (sltrib.com) —
       mismo MIDA de Utah (junta que aprobó el plan Stratos).
    5. "Utah wants to process uranium..." (sltrib.com) — Military Installation
       Development Authority (MIDA) de Utah, energía nuclear.

  CAUSA RAÍZ identificada: la búsqueda web `prensa_agro` en config/sources.yaml
  usa DuckDuckGo (`ddgs.news()`) con `site:prensa.com` + término "MIDA". La
  librería ddgs no respeta de forma confiable el operador `site:` en búsquedas
  de noticias — devuelve resultados globales de cualquier dominio que
  contengan "MIDA" en título/cuerpo (acrónimo compartido con agencias de
  Malasia y Utah). `is_agro_relevant()` solo compara contra la lista de
  `search_terms`, sin verificar el dominio real ni exigir contexto de Panamá,
  así que estos artículos pasaban el filtro y quedaban mal etiquetados con
  `country: PA` y `source: prensa.com` pese a venir de paultan.org/sltrib.com.

  FIX aplicado: scripts/fetch_news.py `fetch_ddg_search()` ahora valida que el
  dominio real de la URL devuelta coincida con `site` (o sea subdominio de
  este) antes de aceptar el resultado; si no coincide, se descarta y se loguea.
  Esto cierra el vector de falsos positivos por colisión del acrónimo "MIDA"
  para las búsquedas restringidas por sitio (prensa_agro, mida_noticias,
  idiap_investigacion, bda_credito, iica_panama). No se tocó fetch_gdelt_batch
  (ya exige mención explícita de Panamá) ni fetch_rss (no usa `site:`).

  Total falsos positivos acumulados: 12 (7 previos + 5 de esta sesión).

## 2026-07-18 16:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-18 16:06
INGEST: routine automática — 4 pendientes revisados, 0 ingestados, 4 falsos positivos
  Ninguno de los 4 artículos restantes de la cola es sobre agro panameño.
  Ninguno fue ingestado al wiki. Confirmé que ninguno menciona "Panamá"/"Panama"
  en el texto completo.

  Falsos positivos detectados:
    1. "The Persian Qanat" (whc.unesco.org/en/list/1506) — sitio UNESCO sobre
       el sistema de irrigación qanat en Irán.
    2. "New York Farm Bureau" (nyfb.org) — organización agrícola de Nueva York,
       EE.UU. (página institucional, sin contenido noticioso).
    3. "'Reef Saudi'..." (spa.gov.sa) — programa de agricultura de secano de
       Arabia Saudita.
    4. "Ambient IoT: Communications Enabling Precision Agriculture"
       (ieeexplore.ieee.org) — paper académico genérico sobre 6G/agricultura
       de precisión, sin mención geográfica a Panamá.

  Mismo patrón que el lote anterior: ninguno de estos 4 dominios es
  prensa.com, pero quedaron etiquetados `source: prensa.com` por la búsqueda
  `prensa_agro` (ver diagnóstico de las 16:03) — confirma que el fix de
  validación de dominio en fetch_ddg_search() era necesario y cubre este caso
  también (whc.unesco.org, nyfb.org, spa.gov.sa, ieeexplore.ieee.org — ninguno
  es ni subdominio de prensa.com).

  Total falsos positivos acumulados: 16 (12 previos + 4 de esta sesión).

## 2026-07-18 16:06 (bugfix)
MAINTENANCE: 2 bugs corregidos en scripts/ de ingesta (encontrados durante
  la revisión de falsos positivos de esta sesión)

  1. `mark_ingested()` en scripts/ingest.py — crasheaba con AttributeError en
     TODA invocación (`python wiki_agro.py mark-ingested <url>`, el comando
     exacto que pending_ingest.md indica ejecutar tras cada artículo) porque
     iteraba `processed.items()` sin excluir la clave interna `_gdelt_windows`
     (una lista, no un dict). Fix: usa `article_entries()` para filtrar claves
     internas, igual que el resto de core.py.

  2. `mark_all_ingested()` en scripts/ingest.py — usaba `find_pending()` en
     orden alfabético de archivo, mientras que `ingest` selecciona el lote a
     mostrar a Claude vía `prioritize(strategy="score")`. Esto podía marcar
     como ingestado un artículo *distinto* al que realmente se revisó,
     dejándolo perdido de la cola sin haber sido nunca evaluado ni añadido al
     wiki. Confirmado en esta sesión: marcó
     `https://ieeexplore.ieee.org/document/10945742` como ingestado sin haber
     sido mostrado a Claude — revertido manualmente y corregido el código para
     que `mark_all_ingested()` use la misma priorización por score que `ingest`.

  Ambos fixes en scripts/fetch_news.py (validación de dominio) y
  scripts/ingest.py (los dos bugs anteriores) — commiteados junto con esta
  sesión de routine.

## 2026-07-18 16:08
DIAGNÓSTICO: pendientes=0 tras esta sesión → diagnóstico avanzado (Paso 4)
  1. ¿Actions corrió hoy? Sí — commit `9bf774b` de hoy, "0 artículos nuevos".
  2. Racha sin artículos nuevos en sources/: 3 días (16, 17, 18 jul) — llega
     al límite de alarma de CLAUDE.md ("3 días consecutivos").
  3. Ventanas GDELT: 50 completadas (>=45) → rango 2015→hoy ya cubierto, pero
     0 artículos guardados vía GDELT en ninguna ventana histórica. No
     confirmado si es cobertura real 0 o filtro demasiado estricto — queda
     como acción pendiente para próxima sesión (ver wiki/metrics.md).
  4. RSS: solo IICA y LaPrensaGeneral activas; 0 artículos con method=rss en
     el dataset actual. No se pudo probar alcanzabilidad de los feeds desde
     este entorno (sin acceso saliente a internet) — revisar logs de Actions.

  Conclusión: la alarma de "3 días sin nuevos" está técnicamente activa, pero
  el hallazgo más importante es que el pipeline automático llevaba ~55 días
  (desde el seed del 2026-05-24) sin producir NINGÚN artículo real — el 100%
  de lo que llegaba eran falsos positivos por el bug de `site:` en DDG,
  corregido hoy. El próximo indicador a vigilar es si, tras el fix, la
  corrida de mañana de Actions trae artículos de dominios reales de
  prensa.com/mida.gob.pa/etc. en vez de dominios ajenos.
