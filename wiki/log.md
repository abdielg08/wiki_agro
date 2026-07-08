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

## 2026-07-08 00:00
FALSOS POSITIVOS: 5/5 artículos pendientes rechazados (0 ingestados esta sesión)
  El keyword "MIDA" produjo coincidencias con "Military Installation Development
  Authority" (Utah, EE.UU.), no con el Ministerio de Desarrollo Agropecuario de Panamá.
  Artículos NO ingestados:
    - 20260519_prensacom_news-2026-05-19-kevin-oleary-data-center-timeline.json
      → Data center de Kevin O'Leary en Utah (MIDA = autoridad militar de Utah)
    - 20260527_prensacom_news-2026-05-27-box-elder-data-center-opponents.json
      → Oposición a data center en Box Elder, Utah
    - 20260529_prensacom_news-environment-2026-05-29-utah-governor-issues-order-prote.json
      → Orden del gobernador de Utah sobre Great Salt Lake y calidad del aire (data centers)
    - 20250613_prensacom_news-environment-2025-06-12-utah-nuclear-energy-state.json
      → Procesamiento de uranio en Utah (menciona "MIDA" = autoridad militar de Utah)
    - 20260624_prensacom_en-n2096157.json
      → Programa "Reef Saudi" de agricultura de secano en Arabia Saudita (agro, pero no Panamá)
  Acción: marcados como ingested=true (procesados/descartados) para limpiar la cola de
  pendientes. No se creó contenido en wiki/. Falsos positivos: 5, tasa acumulada
  de esta sesión: 100% de la muestra — indica que el fetcher está capturando ruido
  por coincidencia de la palabra "MIDA" fuera de contexto panameño; recomendable
  ajustar el filtro de keywords en el fetch (ver diagnóstico más abajo).

## 2026-07-08 16:02
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-07-08 16:05
FALSOS POSITIVOS: 1/1 artículo pendiente rechazado (0 ingestados)
  Artículo NO ingestado:
    - 20260624_prensacom_en-n2096157.json (https://www.spa.gov.sa/en/N2096157)
      → Programa "Reef Saudi" de agricultura de secano en Arabia Saudita — agro, pero
        no de Panamá. Quedó pendiente tras el batch anterior (mark-all-ingested --limit 5
        no lo marcó junto con los otros 4); se marca manualmente ahora.
  Total falsos positivos consecutivos en esta sesión: 6/6 (100%) — confirma que el
  fetch está trayendo ruido no panameño. Ver diagnóstico en la sección siguiente.

## 2026-07-08 16:20
FIX (scripts/ingest.py): `mark_ingested()` iteraba `processed.items()` crudo y
  llamaba `.get()` sobre valores no-dict (p. ej. la clave interna `_gdelt_windows`,
  que es una lista), causando `AttributeError: 'list' object has no attribute 'get'`
  al ejecutar `python wiki_agro.py mark-ingested <url>`. Corregido para usar
  `article_entries(processed)` (igual que `mark_all_ingested`), que excluye claves
  internas `_*`.

## 2026-07-08 16:25
DIAGNÓSTICO (Pendientes = 0, diagnóstico avanzado según CLAUDE.md Paso 4):
  1. GitHub Actions SÍ corrió hoy (commit b46e6af, "0 artículos nuevos
     descargados"). Las últimas 3 corridas de sources/ (07-08, 07-04, 07-03)
     trajeron 0 artículos nuevos cada una.
  2. `_gdelt_windows` en sources/processed.json = 46 ventanas (≥ 45 estimadas
     según CLAUDE.md), pero al inspeccionar el contenido:
     - 37 ventanas trimestrales distintas cubren 2017-03-30 → 2026-06-17.
     - Faltan por completo 2015-02-19 → 2017-03-29 (~2 años nunca consultados).
     - 9 ventanas adicionales comparten el mismo inicio (20260618) con fin
       incremental día a día (20260618_20260623 … 20260618_20260707) — son
       casi duplicadas entre sí y no representan cobertura trimestral real,
       simplemente inflan el contador de "ventanas completadas".
     Conclusión: el rango NO está realmente agotado — hay un gap real de ~2
     años al inicio del período objetivo. Se documenta en wiki/metrics.md con
     la recomendación de correr manualmente `wiki_historical.yml` con
     `years: "2015-2017"` para cerrar el gap (no se ejecuta en esta sesión por
     ser una acción de varias horas en CI, queda para decisión humana).
  3. Causa raíz de los 6 falsos positivos de hoy: `fetch_ddg_search()` en
     scripts/fetch_news.py construía la query como `site:prensa.com <keywords>`
     pero no validaba que la URL del resultado realmente perteneciera a ese
     dominio — `ddgs.news()` no respeta el operador `site:` de forma
     confiable. Además, `source` y `country` se asignaban desde la config
     (hardcoded "prensa.com" / "PA"), no desde la URL real, por lo que
     artículos de sltrib.com (Utah) y spa.gov.sa (Arabia Saudita) quedaron
     mal etiquetados como fuente panameña de confianza nivel 3.
  FIX aplicado: `fetch_ddg_search()` ahora compara `urlparse(url).netloc` con
  el `site` configurado y descarta el resultado si no coincide (o no es
  subdominio). Esto debería eliminar esta clase de falso positivo en la
  próxima corrida de Actions.
  Métricas actualizadas en wiki/metrics.md.

## 2026-07-08 16:35
BUG ADICIONAL DESCUBIERTO Y CORREGIDO: al revisar el diff de
sources/processed.json antes del commit, se encontró un 7mo artículo marcado
`ingested: true` que NUNCA apareció en pending_ingest.md ni fue revisado:
  - 20260617_prensacom_.json (https://www.nyfb.org/, "New York Farm Bureau")
    → New York Farm Bureau (EE.UU.), no relacionado con Panamá. Falso positivo,
      mismo bug raíz que los otros 6 (site: filter de DDG).
Causa: `mark_all_ingested(limit=5)` usaba `find_pending()` (orden por nombre
de archivo) mientras que `ingest --limit 5` usa `prioritize(strategy="score")`
(orden por score de relevancia) — los dos comandos podían seleccionar
conjuntos de artículos DISTINTOS para el mismo `--limit`, permitiendo que
`mark-all-ingested` marque como ingestado un artículo que Claude Code nunca
llegó a ver ni revisar. Esto viola directamente la garantía de "0% falsos
positivos" del proyecto, ya que un artículo podía quedar "procesado" sin
pasar por revisión.
FIX aplicado (scripts/ingest.py): `mark_all_ingested()` ahora usa
`prioritize(strategy="score")` igual que `ingest`, garantizando que
`--limit N` marque exactamente los mismos N artículos que el último
`ingest --limit N` mostró.
Total real de falsos positivos de esta sesión: 7/7 (100%). Totales
acumulados corregidos en wiki/metrics.md.
