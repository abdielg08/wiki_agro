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

## 2026-08-05 00:00
INGEST (routine automática): 5 artículos pendientes revisados — 5/5 FALSOS POSITIVOS
  Los 5 artículos del batch de `ingest --limit 5` NO son sobre agro de Panamá.
  Ninguno se ingestó al wiki (sin summaries, sin cambios a topics/ ni entities/).

  Detalle de falsos positivos:
    1. "MITI working on simplified NCM customised incentive mechanism..."
       (paultan.org) — MITI/MIDA/MARii son agencias de Malasia (Malaysian
       Investment Development Authority), no el MIDA panameño.
    2. "Timeline: How the Kevin O'Leary data center plan came to be..."
       (sltrib.com) — MIDA = Military Installation Development Authority
       de Utah, EE.UU. Nada que ver con agropecuario panameño.
    3. "Box Elder data center opponents hope for a vote..." (sltrib.com) —
       mismo MIDA de Utah (data center de O'Leary en Box Elder County).
    4. "Utah Gov. Cox issues order to protect Great Salt Lake..."
       (sltrib.com) — mismo MIDA de Utah, calidad del aire/agua.
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com) —
       artículo genérico de viajes; mención tangencial a MIDA de Utah en
       una demanda legal, cero relación con Panamá.

  CAUSA RAÍZ: colisión de la sigla "MIDA" — el fetcher (GDELT/búsqueda por
  palabra clave) no distingue entre:
    - MIDA Panamá = Ministerio de Desarrollo Agropecuario (el que nos interesa)
    - MIDA Malasia = Malaysian Investment Development Authority
    - MIDA Utah = Military Installation Development Authority
  Revisando `sources/articles/` se observan más artículos con el mismo
  patrón (Malasia: MITI/NCM/Tengku Zafrul; Utah: data centers/Box Elder;
  además ruido de "Aragón" España confundido con topónimos). Esto ya se
  había detectado antes (ver wiki/metrics.md, fix de 2026-06-22, 7 falsos
  positivos previos) — el fetch sigue sin filtro geográfico/de contexto
  para "MIDA", por lo que el problema persiste y probablemente afecta
  varios de los 16 pendientes restantes.
  RECOMENDACIÓN (no aplicada esta sesión, fuera de alcance de la routine):
  agregar filtro negativo en scripts/fetch* — descartar artículos cuyo
  dominio/contexto sea Utah (.gov Utah, sltrib.com), Malasia (paultan.org,
  MITI/NCM/Ringgit) o España (Aragón, Vox) salvo que el texto mencione
  explícitamente Panamá.

  Marcados como ingestados (processed.json) vía `mark-all-ingested --limit 5`
  para no bloquear la cola — no se creó contenido nuevo en wiki/.

## 2026-08-05 00:04
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-05 00:20
CORRECCIÓN + BUG ENCONTRADO: `mark-all-ingested --limit N` marca artículos en
orden alfabético de archivo (`find_pending`), NO en el mismo orden por score
que `ingest --limit N` le muestra a Claude en `pending_ingest.md`. El
`mark-all-ingested --limit 5` de la entrada anterior marcó 5 artículos
DISTINTOS a los 5 revisados arriba (incluyendo uno que nunca se revisó:
"Ambient IoT: Communications Enabling Precision Agriculture", IEEE, un paper
académico global sobre 6G/IoT sin mención de Panamá — igualmente un falso
positivo, pero por suerte, no contenido real perdido). Los 4 artículos
realmente revisados (paultan MITI, kevin-oleary, box-elder, utah-governor)
seguían pendientes. Se corrigieron con `mark-ingested <url>` individual.

Falsos positivos adicionales detectados al auditar qué se marcó por error:
  - "Ambient IoT: Communications Enabling Precision Agriculture" (IEEE) —
    paper académico genérico, sin mención de Panamá.
  - "Catalogue of the diptera of the Americas South of United States"
    (archive.org) — catálogo zoológico brasileño de 1966/67, sin relación
    con Panamá actual.
  - "Aragón celebra la sentencia del Supremo que tumba ampliación...cerdo
    en las granjas" (heraldo.es) — Aragón, ESPAÑA, no Panamá.
  - "Utah wants to process uranium...for nuclear energy" (sltrib.com) —
    menciona MIDA (Military Installation Development Authority) de Utah.

INGEST (segundo lote, 5 artículos): 5/5 FALSOS POSITIVOS adicionales:
  1. Repetidos del primer lote aún pendientes por el bug de arriba: MITI
     Malasia, Kevin O'Leary timeline, Box Elder, Utah Gov. Cox.
  2. "New York Farm Bureau" (nyfb.org) — organización agrícola de EE.UU.,
     sin relación con Panamá.
  Los 5 se marcaron correctamente con `mark-ingested <url>` individual
  (no se usó mark-all-ingested para evitar el bug de desincronización).

Al revisar los 6 pendientes restantes (`queue`), los 6/6 eran también
falsos positivos, todos de fuentes internacionales sin relación con Panamá:
  - 3× heraldo.es (Aragón, España): consejería de Medio Ambiente/caso
    Forestalia, elecciones agrarias AEGA, ampliación de Arvensis Agro.
  - "Reef Saudi, a Successful Program Based on Rain-Fed Agriculture"
    (spa.gov.sa) — Arabia Saudita.
  - "Finep vai pagar R$ 220 milhões para inovações em agricultura
    familiar" (agenciabrasil.ebc.com.br) — Brasil.
  - "The Persian Qanat" (whc.unesco.org) — sistema de riego histórico de
    Irán/patrimonio UNESCO.
  Se marcaron los 6 como ingestados (falsos positivos) con `mark-ingested`.

RESULTADO: los 16 artículos pendientes al inicio de esta sesión eran
16/16 (100%) falsos positivos. 0 artículos reales ingestados al wiki esta
sesión, pero se mantiene la tasa de 0% falsos positivos EN el wiki
(ninguno se agregó a topics/entities/summaries). Total acumulado de
falsos positivos: 7 (previos, 2026-06-22) + 16 (hoy) = 23.

CAUSA RAÍZ (root cause, identificada y corregida):
`fetch_ddg_search()` en `scripts/fetch_news.py` (fuente "prensa.com" del
modo `daily`, la que más artículos aporta según `stats`) no aplicaba los
filtros `_is_blocked_domain()` / `_is_panama_related()` que sí tiene
`fetch_rss()`. El operador `site:prensa.com` de DuckDuckGo no se respeta
de forma confiable en la librería `ddgs` — devolvía resultados de
cualquier dominio global que matcheara términos genéricos como "MIDA" o
"agricultura" (colisión de siglas: MIDA Panamá = Ministerio de Desarrollo
Agropecuario, pero también MIDA Malasia = Malaysian Investment
Development Authority y MIDA Utah = Military Installation Development
Authority). Además, el código etiquetaba `source` con el sitio
configurado sin verificar que la URL real perteneciera a ese dominio,
por lo que `stats` mostraba "prensa.com: 23 artículos" ocultando que
eran en realidad de sltrib.com, heraldo.es, paultan.org, etc.

FIX APLICADO (commit de esta sesión):
  1. `scripts/fetch_news.py::fetch_ddg_search()` — ahora valida que el
     dominio real de la URL contenga el `site` configurado, y aplica
     `_is_blocked_domain()` + `_is_panama_related()`, igual que
     `fetch_rss()`.
  2. `scripts/ingest.py::mark_ingested()` — ya no crashea al iterar
     claves internas no-dict de `processed.json` (ej. `_gdelt_windows`).
  3. `scripts/ingest.py::mark_all_ingested()` — ahora ordena los
     pendientes por score (mismo criterio que `ingest`) antes de aplicar
     `--limit`, para no marcar artículos distintos a los revisados.

DIAGNÓSTICO AVANZADO (Paso 4, pendientes=0):
  - GitHub Actions corrió: 2026-08-04 (ayer), 2026-08-02, 2026-07-31,
    2026-07-30, 2026-07-29 — corre casi a diario mode=daily.
  - Últimos artículos NUEVOS reales: 2026-07-30 (3) y 2026-07-29 (2).
    Desde entonces, 3 corridas consecutivas (07-31, 08-02, 08-04) con
    0 artículos nuevos → **se cumple la condición de alarma de CLAUDE.md**
    ("3 días consecutivos sin nuevos artículos").
  - `_gdelt_windows`: 62 ventanas completadas. Desglose: 2017-2025 con
    4/4 trimestres cada uno (completos), pero **2015 y 2016 con 0/4** —
    el rango objetivo del wiki (2015-02-19 → hoy) tiene un hueco real de
    2 años nunca cubierto por GDELT. 2026 muestra 26 "ventanas" (vs. ~4
    esperadas) por churn: cada corrida diaria genera una ventana nueva
    con fecha de fin distinta en vez de reusar la del trimestre en
    curso — infla el contador sin aportar cobertura real.
  - RSS (IICA, La Prensa): no se ejecutó un fetch en esta sesión para
    verificar en vivo; los datos de `stats` muestran solo 1 artículo de
    IICA y 1 de LaPrensaEco acumulados desde el inicio del proyecto, lo
    cual sugiere que las fuentes RSS aportan muy poco volumen frente a
    la fuente DDG (ahora corregida).

RECOMENDACIÓN PARA PRÓXIMA SESIÓN: correr
`python wiki_agro.py fetch-historical --years 2015-2016 --mode gdelt`
para cerrar el hueco real de cobertura, y validar tras la próxima corrida
de Actions que el fix de `fetch_ddg_search()` elimine los falsos positivos
de dominios no-Panama.
