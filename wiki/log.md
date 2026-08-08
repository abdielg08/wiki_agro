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

## 2026-08-08 00:00
ROUTINE: Diagnóstico inicial — 16 pendientes de ingesta (29 descargados, 13 ingestados)
INGEST: lote de 5 artículos revisado — 5 FALSOS POSITIVOS, 0 ingestados
  Causa raíz: coincidencia de la sigla "MIDA" sin relación con Panamá.
  Todos capturados por la fuente `prensa.com` (fetch por keyword, sin filtro de país):
    1. "MITI working on simplified NCM..." (paultan.org, 2026-07-08)
       → MIDA = Malaysian Investment Development Authority (Malasia), no Panamá.
    2. "Timeline: How the Kevin O'Leary data center plan came to be..." (sltrib.com, 2026-05-19)
       → MIDA = Military Installation Development Authority (Utah, EE.UU.), no Panamá.
    3. "Box Elder data center opponents hope for a vote..." (sltrib.com, 2026-05-27)
       → mismo MIDA de Utah, disputa de centro de datos.
    4. "Utah Gov. Cox issues order to protect Great Salt Lake..." (sltrib.com, 2026-05-29)
       → mismo MIDA de Utah, calidad de aire/agua.
    5. "Cultural Rules For Staying With Locals Abroad" (msn.com, 2026-03-07)
       → artículo de viajes; menciona demanda contra MIDA de Utah de pasada.
  Ninguno trata sobre agro panameño. No se creó ninguna página de wiki.
  Acción: marcados como ingested=true vía `mark-all-ingested` para vaciar la cola de pendientes
  (no cuentan como avance real del wiki; ver metrics.md).
  Recomendación: el fetcher de `prensa.com`/GDELT debería filtrar por país=Panamá o excluir
  coincidencias de "MIDA" cuando el resto del texto no menciona Panamá/agro, para reducir
  falsos positivos futuros.

## 2026-08-08 16:03
INGEST: 5 artículos marcados como ingestados por sesión Claude Code

## 2026-08-08 16:20
BUGFIX: dos bugs encontrados en scripts/ingest.py durante la sesión de rutina
  1. `mark-all-ingested --limit N` usaba `find_pending()` sin priorizar, mientras que
     `ingest --limit N` usa `prioritize(strategy="score")`. Con más de N pendientes,
     ambos comandos operan sobre conjuntos DISTINTOS de artículos — `mark-all-ingested`
     puede marcar como ingestados artículos que Claude nunca revisó. Ocurrió en esta
     sesión: se marcaron 5 artículos no relacionados con los 5 mostrados en
     pending_ingest.md (por suerte, los 5 marcados también resultaron ser falsos
     positivos — ver detalle abajo — pero el riesgo de perder un artículo real de
     Panamá sin revisión es real). Fix: `mark_all_ingested()` ahora usa
     `prioritize()` con el mismo `strategy` (default "score") que `ingest`, y el CLI
     expone `--strategy` en `mark-all-ingested` para que coincida con `ingest`.
     Recomendación futura: usar los comandos `mark-ingested '<url>'` exactos que
     genera `pending_ingest.md` en vez de `mark-all-ingested --limit N`, que es más
     seguro porque marca artículos por URL explícita.
  2. `mark-ingested '<url>'` fallaba con `AttributeError: 'list' object has no
     attribute 'get'` porque iteraba `processed.items()` directamente, incluyendo la
     clave interna `_gdelt_windows` (una lista, no un dict). Fix: usa
     `article_entries(processed)` (ya usado en otras partes del código) para excluir
     claves internas que empiezan con `_`.
  Archivos modificados: scripts/ingest.py, wiki_agro.py

## 2026-08-08 16:25
INGEST: lote adicional de 11 artículos revisado — 11 FALSOS POSITIVOS, 0 ingestados
  (incluye los 4 no marcados correctamente del lote anterior por el bug #1 arriba,
  más 7 nuevos: fetch --limit 5 los volvió a mostrar tras el fix de mark-ingested).
  Ninguno trata sobre agro panameño:
    - heraldo.es ×3 (Aragón, España): nombramiento de consejero de Medio Ambiente,
      protesta agraria AEGA, ampliación de planta Arvensis Agro — todos sobre
      agricultura de Aragón, España, no Panamá.
    - sltrib.com ×2 adicionales (Utah, EE.UU.): disputa de centro de datos de
      Kevin O'Leary / MIDA de Utah — mismo problema que el lote anterior.
    - nyfb.org: página institucional de New York Farm Bureau (EE.UU.).
    - spa.gov.sa: programa "Reef Saudi" de agricultura de secano en Arabia Saudita.
    - agenciabrasil.ebc.com.br: financiamiento Finep para agricultura familiar en
      Brasil.
    - whc.unesco.org: sitio UNESCO sobre los qanats persas (Irán), patrimonio
      histórico de irrigación — no es noticia ni es de Panamá.
    - paultan.org: MITI/MIDA/MARii de Malasia (repetido del lote anterior, no
      marcado a tiempo por el bug #1).
  Con esto, PENDIENTES DE INGESTA = 0 (29/29 artículos descargados revisados;
  16 de los 29 son falsos positivos de esta sesión, sumados a los 7 falsos
  positivos ya documentados en metrics.md de sesiones previas = 23 falsos
  positivos acumulados sobre 29 descargas totales). Cero páginas de wiki nuevas
  esta sesión — no había ningún artículo genuino sobre agro panameño en la cola.

## 2026-08-08 16:30
DIAGNÓSTICO AVANZADO (pendientes = 0):
  - Artículos nuevos hoy en sources/articles/: 0.
  - Último commit de GitHub Actions a sources/: 2026-08-07 ("0 artículos nuevos
    descargados"). Las 4 corridas más recientes con cambios en sources/
    (2026-07-31, 08-02, 08-04, 08-07) reportaron 0 artículos nuevos cada una.
    La última corrida con artículos nuevos fue 2026-07-30 (3 nuevos) — es decir,
    9 días consecutivos sin artículos nuevos en sources/articles/, lo que supera
    el umbral de falla de 3 días definido en CLAUDE.md.
  - Ventanas GDELT completadas: 63 (rango real 2017-03-30 → 2026-08-06). Esto es
    ≥45, pero la ventana más antigua completada empieza en 2017-03-30, NO en
    2015-01-01/2015-02-19 como pide la cobertura objetivo. Esto indica que las
    ventanas de 2015-01-01 a 2017-03-29 (~9 ventanas trimestrales) están
    fallando/bloqueadas en cada corrida (fetch_gdelt_historical hace
    `batch is None` → no las marca completas → se reintentan sin éxito en cada
    ejecución) mientras el resto del rango 2017-2026 sí se completó. Causa
    probable: bloqueo/rate-limit de GDELT específicamente en las ventanas más
    antiguas, o esas consultas exceden algún límite del endpoint.
  - Causa raíz de los falsos positivos: `scripts/prioritize.py` incluye "MIDA"
    en `HIGH_PRIORITY_TERMS`, y el fetch por keyword vía GDELT/prensa.com no
    filtra por país. Esto captura sistemáticamente noticias sobre la Malaysian
    Investment Development Authority (Malasia) y la Military Installation
    Development Authority (Utah, EE.UU.), que también se abrevian "MIDA", además
    de noticias agrícolas genéricas de otros países (España/Aragón, Brasil,
    Arabia Saudita, Irán/UNESCO, EE.UU.) que coinciden con términos genéricos de
    agricultura sin relación con Panamá. 23 de 29 artículos descargados
    (79%) son falsos positivos por esta causa.
  Recomendación (fuera de alcance de esta sesión, requiere cambio en el fetcher):
    1. Filtrar resultados GDELT/prensa.com por `sourcecountry:Panama` o similar,
       o exigir coincidencia con un topónimo panameño (Panamá, Chiriquí, Azuero,
       Veraguas, Coclé, Darién, etc.) además del término temático.
    2. Revisar por qué las ventanas GDELT 2015-01 a 2017-03 fallan sistemáticamente
       (posible bloqueo/rate-limit) — considerar reintentos con backoff o una
       fuente alterna para ese rango.

## 2026-08-08 16:08
INGEST: 0 artículos marcados como ingestados por sesión Claude Code
