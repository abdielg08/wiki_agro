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

## 2026-08-03 00:00
ROUTINE: 16/16 pendientes = 16 falsos positivos (0 artículos reales ingestados)
  Ninguno de los 16 artículos pendientes trataba sobre agro panameño. NO se
  ingestó ninguno al wiki, siguiendo la regla de 0% falsos positivos.

  Detalle por artículo (todos con country=PA mal etiquetado, source=prensa.com
  mal etiquetado — ver causa raíz abajo):
    - spa.gov.sa/en/N2096157 → programa "Reef Saudi" de agricultura de secano (Arabia Saudita)
    - sltrib.com (x3) → centros de datos de Kevin O'Leary en Utah, mencionan "MIDA"
      = Military Installation Development Authority (Utah), NO Ministerio de
      Desarrollo Agropecuario de Panamá
    - nyfb.org → New York Farm Bureau (EE.UU.)
    - whc.unesco.org/en/list/1506 → qanats persas (patrimonio UNESCO, Irán)
    - paultan.org → MITI/MIDA = Malaysian Investment Development Authority
      (incentivos industriales de Malasia), NO Panamá
    - ieeexplore.ieee.org/document/10945742 → paper académico IoT/agricultura de precisión (genérico, sin país)
    - msn.com → artículo de viajes ("reglas culturales para hospedarse con locales"), menciona MIDA de Utah
    - archive.org → catálogo de dípteros de 1966/67 (Secretaria da Agricultura, Brasil histórico)
    - heraldo.es (x3) → noticias agropecuarias de Aragón, España
    - agenciabrasil.ebc.com.br → financiamiento Finep para agricultura familiar (Brasil)

  CAUSA RAÍZ IDENTIFICADA: `scripts/fetch_news.py::fetch_ddg_search()` construye
  la búsqueda con `site:prensa.com <query>`, pero el operador `site:` de la
  librería `ddgs` (DuckDuckGo) no restringe de forma confiable los resultados
  al dominio configurado. La función aceptaba CUALQUIER resultado devuelto por
  la búsqueda y lo etiquetaba con `source: "prensa.com"` y `country: "PA"` sin
  verificar el dominio real de la URL. Combinado con `is_agro_relevant()`, que
  solo verifica presencia de palabras clave genéricas (p.ej. "MIDA",
  "agricultura") sin contexto de Panamá, esto permitió que noticias agrícolas
  de Arabia Saudita, España, Brasil, EE.UU. (Utah) y Malasia entraran como
  "pendientes de ingesta" con apariencia de fuente panameña confiable.

  FIX APLICADO (scripts/fetch_news.py, fetch_ddg_search): se agregó
  verificación de que el `netloc` de la URL devuelta coincida con el dominio
  `site` configurado (o sea subdominio de este) antes de aceptar el resultado;
  si no coincide, se descarta silenciosamente. Esto habría bloqueado los 16
  falsos positivos de esta sesión en el momento del fetch, no en el ingest.

  BUG SECUNDARIO ENCONTRADO Y CORREGIDO: `scripts/ingest.py::mark_ingested()`
  (comando singular `mark-ingested`) iteraba sobre TODAS las claves de
  `processed.json` sin filtrar la clave interna `_gdelt_windows` (una lista),
  causando `AttributeError` en cualquier llamada. Se corrigió para usar
  `article_entries()` igual que `mark_all_ingested()`.

  Acción: los 16 artículos se marcaron `ingested: true` en processed.json
  (decisión tomada, no re-entran a la cola) pero NO se creó contenido de wiki
  para ninguno. Pendientes de ingesta: 16 → 0.

DIAGNÓSTICO DE FETCH:
  - Última corrida GitHub Actions con artículos nuevos: 2026-07-30 (3 artículos)
  - Corridas recientes con 0 artículos nuevos: 2026-07-31, 2026-08-02 (2 días
    consecutivos — no llega aún al umbral de 3 días de falla)
  - Ventanas GDELT completadas: 61. Al desglosar por trimestre (parseando
    `_gdelt_windows`), 2017 Q1 → 2025 Q4 están completos (36/36, 1 ventana
    c/u), 2026 tiene una ventana rolling que se re-genera en cada corrida
    (25 registros), pero **2015 Q1 → 2016 Q4 (8 trimestres) tienen CERO
    ventanas registradas** — nunca se completaron exitosamente. Esta es la
    brecha histórica real pendiente, no un agotamiento del rango.
    HIPÓTESIS (no confirmada — esta sesión no tiene acceso de red a
    api.gdeltproject.org para probarlo en vivo, el runner de GitHub Actions
    sí lo tiene): dado que `fetch_gdelt_historical()` itera secuencialmente
    desde 2015-01-01 y en caso de error de red NO marca la ventana como
    completa (permitiendo reintento) pero SÍ avanza a la siguiente ventana
    en la misma corrida, es consistente que las ventanas 2015-2016
    fallen sistemáticamente en cada corrida (por ejemplo, GDELT podría
    tener cobertura/soporte débil para fechas tan antiguas) mientras que
    2017 en adelante responde con éxito. Recomendación para próxima sesión
    con acceso al runner de Actions: revisar los logs de Actions de una
    corrida reciente y buscar errores de red específicamente en las
    ventanas `2015*` y `2016*`.
  - Fuentes RSS activas (IICA, La Prensa): sin cambios reportados esta sesión.
