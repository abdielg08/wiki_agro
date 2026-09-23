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

## 2026-09-15 08:00
INGEST (routine automatizada): 10 artículos reales ingestados en dos lotes de 5.

**Lote 1** (todos sobre arroz/MIDA, prensa.com):
  - 20250724 — Productores temen pérdidas por importaciones en cosecha → summaries/ + topics/arroz.md, topics/precios_mercados.md (creado), entities/mida.md
  - 20241107 — Pérdidas por inundaciones (arroz, maíz, ganadería) en Veraguas → summaries/ + topics/arroz.md, topics/maiz.md, topics/cambio_climatico.md
  - 20220524 — Proyección de siembra ~90,000 ha arroz ciclo 2022-2023 → summaries/ + topics/arroz.md, entities/mida.md
  - 20240607 — Roberto Linares revisará subsidios en el Mida → summaries/ + topics/subsidios_programas.md (creado), topics/politicas_agropecuarias.md, entities/mida.md
  - 20240613 — Productores de arroz Panamá Este/Darién exigen pago de compensaciones → summaries/ + topics/arroz.md, topics/subsidios_programas.md, entities/mida.md

**Lote 2** (MIDA — gobierno, avicultura, clima, opinión):
  - 20260303 — Nuevo viceministro del Mida (renuncia de Ameglio) → summaries/ + topics/politicas_agropecuarias.md, entities/mida.md
  - 20230216 — Mida previene gripe aviar en Panamá Oeste → summaries/ + topics/avicultura.md (creado), topics/plagas_enfermedades.md, entities/mida.md
  - 20260224 — Opinión: agricultura de subsistencia a precisión exportadora → summaries/ + topics/politicas_agropecuarias.md, topics/tecnologia_innovacion.md (creado)
  - 20221022 — Mida refuerza controles influenza aviar frontera Colombia → summaries/ + topics/avicultura.md, topics/plagas_enfermedades.md, entities/mida.md
  - 20251007 — Boquete: Mida evalúa áreas afectadas por lluvias → summaries/ + topics/cambio_climatico.md, topics/chirique.md (creado), entities/mida.md

Páginas creadas: precios_mercados.md, subsidios_programas.md, avicultura.md, tecnologia_innovacion.md, chirique.md
Páginas actualizadas: arroz.md, maiz.md, cambio_climatico.md, politicas_agropecuarias.md, plagas_enfermedades.md, entities/mida.md
Summaries: 10 nuevos archivos en wiki/summaries/
Nota: el texto fuente de estos 10 artículos venía truncado (`summary_raw`, `full_text: null`); los resúmenes documentan explícitamente qué cifras/detalles no están disponibles en vez de inferirlos, para sostener la tasa de falsos positivos en 0%.

## 2026-09-15 08:20
BUG CRÍTICO ENCONTRADO Y CORREGIDO: `mark-all-ingested` marcaba artículos equivocados.

`scripts/ingest.py::mark_all_ingested()` seleccionaba los "primeros N pendientes" con
`find_pending()`, que ordena por archivo (orden alfabético). Pero `ingest` (el comando
que genera `pending_ingest.md` y que Claude realmente procesa) ordena por
`prioritize()` (score de prioridad). Como los dos órdenes no coinciden, cada corrida de
`mark-all-ingested` marcaba como `ingested: true` un conjunto de artículos DISTINTO al
que Claude acababa de procesar y escribir en el wiki. Efecto acumulado:
  - Los artículos realmente procesados por Claude quedaban `ingested: false` para siempre
    (riesgo de reprocesarlos/duplicar contenido en el wiki en una sesión futura).
  - Artículos alfabéticamente-primeros —incluidos varios falsos positivos nunca
    revisados— quedaban marcados `ingested: true` sin haber pasado por ningún control,
    violando la política de 0% falsos positivos de forma silenciosa.

**Fix aplicado**: `mark_all_ingested()` ahora parsea las URLs directamente de los
`mark-ingested '<url>'` al final de `pending_ingest.md` (el archivo que Claude acaba de
procesar), en vez de re-derivar la lista con un orden distinto. Ver `scripts/ingest.py`.

**Corrección de datos**: se revirtieron los 5 artículos marcados incorrectamente por
esta sesión (los 5 reales del Lote 1 se re-marcaron correctamente después del fix). De
esos 5, 3 resultaron genuinamente irrelevantes/fuera de alcance:
  - `archive.org/details/Cataloguedipter2SaoP`: FALSO POSITIVO — catálogo zoológico de
    dípteros de Brasil, sin relación con Panamá. Marcado `false_positive: true`.
  - 2 artículos de prensa.com (2007, 2010) sobre plagas y diagnóstico del Mida: no son
    falsos positivos temáticos, pero su fecha es anterior a la cobertura objetivo del
    wiki (2015-02-19 → hoy). Marcados `out_of_scope: true`.
  - Los otros 2 (trazabilidad 2019, "Horizonte agropecuario" 2019 — sequía en Panamá
    Este/Darién) son artículos legítimos y quedaron `ingested: false` para procesarse
    en una sesión futura normal.

## 2026-09-15 08:25
DIAGNÓSTICO — FALSOS POSITIVOS SISTÉMICOS en el pipeline de fetch (`fetch_ddg_search`).

Al revisar `sources/processed.json` completo se encontraron **17 artículos adicionales**
ya descargados (`ingested: false`, es decir, aún en la cola de pendientes) que NO son
sobre agro panameño: MITI/MIDA de Malasia, "MIDA" (Military Installation Development
Authority) de Utah — 3 notas sobre centros de datos —, granjas y política agrícola de
Aragón (España) x4, agricultura en Brasil, Arabia Saudita, Mozambique y Maine (EE.UU.),
New York Farm Bureau, un paper de IEEE sobre IoT genérico, y un sitio de patrimonio
UNESCO en Irán. Ninguno menciona a Panamá en su texto. Todos se marcaron
`false_positive: true` con su razón documentada en `sources/processed.json` (no se
creó contenido de wiki para ninguno).

Además se etiquetaron retroactivamente (con `false_positive: true`) 7 artículos que ya
estaban marcados `ingested: true` desde antes de esta sesión (4 de thestar.com.my
—Malasia—, fox13now.com —Utah—, una página genérica de worldbank.org, y un paper de
IEEE) — coincide exactamente con los "7 falsos positivos" reportados en la auditoría
del 2026-06-22 en `wiki/metrics.md`, que ya los había excluido de la cola pero sin
dejar la razón documentada en processed.json.

**Causa raíz identificada**: `fetch_ddg_search()` en `scripts/fetch_news.py` (búsqueda
DuckDuckGo configurada en `config/sources.yaml` → `web_searches`) solo filtraba con
`is_agro_relevant()` (términos genéricos de agro, incluye "MIDA") pero — a diferencia
de los fetchers de RSS y GDELT en el mismo archivo — NO aplicaba `_is_panama_related()`
ni `_is_blocked_domain()`. La consulta usa `site:prensa.com ... OR MIDA OR ...`, y el
operador `site:` de DDG no se respeta de forma confiable cuando la query tiene cláusulas
OR, por lo que se filtran resultados de dominios y países completamente ajenos
(coincidiendo solo en la palabra "MIDA" u otros términos agro genéricos).

**Fix aplicado**: se agregó el mismo guardián de relevancia Panamá
(`_is_blocked_domain(url) or not _is_panama_related(title, url)`) a `fetch_ddg_search()`,
igualando su comportamiento al de `fetch_rss()` y `fetch_gdelt_batch()`. Ver
`scripts/fetch_news.py`.

**Cola de pendientes después de la limpieza**: 14 artículos, todos verificados como
genuinamente sobre agro/MIDA panameño (revisados manualmente por título y fecha).

**Recomendación para sesiones futuras**: seguir revisando `sources/processed.json` en
busca de nuevos falsos positivos de `fetch_ddg_search()` hasta confirmar, en una corrida
real de GitHub Actions con el fix desplegado, que ya no aparecen resultados de dominios
no panameños.

## 2026-09-15 08:30
DIAGNÓSTICO CRÍTICO — GitHub Actions (`wiki_daily.yml`) lleva 8 ejecuciones diarias
consecutivas fallando (2026-09-07 → 2026-09-14), sin producir ningún commit nuevo en
`sources/`. Esto excede el umbral de falla definido en CLAUDE.md ("3 días consecutivos
sin nuevos artículos").

**Evidencia** (vía GitHub Actions API):
  - Última ejecución **exitosa**: run #103, 2026-09-06 13:50–13:56 UTC (~5.5 min,
    duración normal de un fetch real) → commit `24cfc3c` "6 artículos nuevos descargados"
  - Runs #104 a #111 (2026-09-07 a 2026-09-14, uno por día): **conclusion: failure**,
    cada uno completado en **~3 segundos** — muy por debajo del tiempo mínimo de un fetch
    real (RSS+DDG+GDELT tardan minutos). El patrón es consistente con un **fallo de
    arranque del job** (falla antes de ejecutar cualquier paso del workflow: checkout,
    setup-python, o el script de fetch), no con un bug en la lógica de `fetch_news.py`
    o `fetch_historical.py`.
  - Los logs de esas ejecuciones ya **expiraron** (HTTP 404 al solicitarlos vía API) al
    momento de este diagnóstico, por lo que no fue posible obtener el mensaje de error
    exacto desde esta sesión.

**Causas más probables a revisar manualmente** (requieren acceso a la configuración
del repositorio/organización en GitHub, fuera del alcance de esta sesión):
  1. Cuota de minutos de GitHub Actions agotada (billing) — causa típica de fallos
     instantáneos y consistentes en todas las ejecuciones programadas.
  2. Cambio en permisos del `GITHUB_TOKEN` o en la protección de la rama `main` que
     bloquee el `permissions: contents: write` que el workflow requiere para commitear.
  3. El workflow fue deshabilitado o pausado a nivel de repositorio (Settings → Actions).

**Acción recomendada**: el usuario debe revisar
https://github.com/abdielg08/wiki_agro/actions/runs/34870292147 (última ejecución
fallida) mientras el log siga disponible, y validar cuota de Actions / configuración de
permisos. Esta sesión no tiene visibilidad de facturación ni de configuración a nivel
de organización.

**Impacto en el backlog**: no es crítico de inmediato — quedan 14 artículos genuinos
pendientes de ingesta (suficiente para ~3 sesiones de routine más), pero si el fetch no
se restablece, el backlog se agotará en pocos días y el backfill histórico 2015→hoy
quedará detenido.

## 2026-09-15 08:15
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-09-15 08:18
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-09-15 08:25
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-09-15 08:28
LINT: 35 páginas revisadas, 40 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:29, stale:9, no_index:1

## 2026-09-15 08:28
LINT: 35 páginas revisadas, 40 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:29, stale:9, no_index:1

## 2026-09-15 08:29
LINT: 35 páginas revisadas, 40 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:29, stale:9, no_index:1

## 2026-09-23 (sesión Claude Code — RECUPERACIÓN + FIX TRANSMISIÓN)
RECOVERY: El wiki construido por las routines nunca llegaba a main.
  Causa: sesiones de routine con outcome-branch propio + PR draft sin mergear.
  Resultado: 273 ramas claude/modest-galileo-* con trabajo huérfano.
  Acción:
    - Recuperado el wiki más avanzado (rama modest-galileo-b0de9d):
      16 summaries, 13 topics, 3 entities → traído a main.
    - processed.json reconstruido: 18 ingestados reales, 25 falsos positivos
      marcados skipped (Utah, España, Malasia, Saudita, Mozambique...), 14 reales pendientes.
    - FIX: fetch_ddg_search() ahora aplica _is_blocked_domain + _is_panama_related
      (era la fuga de falsos positivos que GDELT/RSS ya bloqueaban).
    - NUEVO: .github/workflows/promote_wiki.yml — auto-promueve wiki/ +
      processed.json de ramas claude/** a main (arregla el Sísifo).

## 2026-09-23 16:17
LINT: 35 páginas revisadas, 40 issues encontrados
  frontmatter:0, huérfanas:1, broken_links:29, stale:9, no_index:1

## 2026-09-23 (sesión Claude Code — routine, DIAGNÓSTICO + FIX SIN INGESTA)

DUPLICADO DETECTADO: `python wiki_agro.py ingest --limit 5` devolvió los mismos
5 artículos que ya había procesado una sesión anterior el mismo día (08:17),
publicados en el PR #307 (rama `claude/modest-galileo-21i61b`, aún abierto como
draft, sin mergear a main): crédito Banco Nacional 2024 ($714.1M), medidas
Covid-19 cosecha de café 2020-2021, "los subsidios acaparan los fondos del
Mida" (2020), agroturismo temporada de cosecha (2019), MIDA/IMA presupuestos
reducidos 2023. Esta sesión generó primero el mismo contenido de forma
independiente (mismos 5 artículos, mismas páginas nuevas `cafe_cacao.md` y
`agroturismo.md`) sin saber que el PR #307 ya existía, y lo descartó
(`git checkout` + `git clean`) al descubrir el duplicado vía la API de GitHub
Actions, para no crear un segundo PR redundante ni contenido en conflicto.
**Acción recomendada al usuario**: revisar y mergear el PR #307
(https://github.com/abdielg08/wiki_agro/pull/307) para que esos 5 artículos
avancen a `main` y `Pendientes` baje de 14 a 9.

FIX DE RAÍZ (independiente, verificado con código, no solo copiado del PR
#307): `scripts/ingest.py::mark_all_ingested()` llamaba de nuevo a
`find_pending()` (orden alfabético por nombre de archivo) en vez de leer las
URLs reales que `ingest` ya había mostrado a Claude en `pending_ingest.md`
(orden por `prioritize()`/score). Verificado experimentalmente: con el
backlog actual, `find_pending(limit=5)` alfabético solo coincide en 1 de 5
URLs con las que de verdad se mostraron a Claude — es decir, `mark-all-ingested`
podía marcar 4 artículos equivocados como ingestados mientras los 5 reales
quedaban pendientes (mismo bug ya corregido el 2026-09-15 y perdido en la
recuperación de rama del 2026-09-22, y de nuevo corregido de forma
independiente por el PR #307 en su propia rama). Corregido ahora en `main`:
`mark_all_ingested()` parsea las URLs directamente de los comandos
`mark-ingested` al final de `pending_ingest.md`. Probado: genera el mismo
resultado que las URLs reales del pending_ingest.md vigente, revertido tras
la prueba (no se marcó nada como ingestado en esta sesión).

DIAGNÓSTICO AVANZADO — GitHub Actions (confirmado vía API, no solo por
ausencia de commits):
- `wiki_daily.yml`: 17+ corridas diarias consecutivas con `conclusion: failure`
  desde 2026-09-07 (última corrida exitosa: run #103, 2026-09-06, 6 artículos).
  Cada corrida falla en ~4 segundos (`created_at` ≈ `completed_at`), sin
  `runner_id` asignado (`runner_id: 0`, `runner_name: ""`) y sin logs
  descargables (404 inmediato) — firma típica de `startup_failure`, es decir
  el job nunca llega a ejecutar ni un solo step (ni siquiera el checkout).
- `promote_wiki.yml` (el workflow que promueve wiki/+processed.json de ramas
  `claude/**` a `main`): mismo patrón exacto — sus 3 corridas hasta ahora
  (incluida la del PR #307) fallan en ~3-4 segundos, `runner_id: 0`. Esto
  confirma que el problema es de infraestructura de Actions a nivel de
  repositorio/cuenta, no un bug de `fetch_news.py` ni de `promote_wiki.yml` —
  y explica por qué el trabajo de rutinas sigue acumulándose en ramas/PRs sin
  llegar nunca a `main` (el mismo "Sísifo" que ya se documentó el 2026-09-22).
- Causa más probable: límite de gasto/minutos de GitHub Actions agotado en
  Settings → Billing, o Actions deshabilitado a nivel de repo/cuenta. Fuera
  del alcance de esta sesión — requiere revisión manual del usuario.

Sin cambios a `wiki/summaries/`, `wiki/topics/` ni `wiki/entities/` en esta
sesión (para no duplicar el contenido ya presente en el PR #307). Únicos
cambios: fix en `scripts/ingest.py` y esta entrada de diagnóstico.
