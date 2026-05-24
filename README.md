# Wiki Agropecuario de Panamá

Wiki de noticias y conocimiento agropecuario panameño (2015–2025), construido
programáticamente con la **metodología Karpathy de LLM Wiki**.

## Arquitectura (3 capas)

```
sources/          ← Artículos crudos (INMUTABLES)
wiki/             ← Wiki persistente mantenido por LLM
CLAUDE.md         ← Schema: instrucciones para el LLM
```

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
# Editar .env y agregar ANTHROPIC_API_KEY
```

## Uso

```bash
# 1. Descargar artículos (RSS recientes + GDELT histórico 2015-2025)
python wiki_agro.py fetch --mode all --limit 100

# 2. Ingestar artículos → actualizar wiki con Claude
python wiki_agro.py ingest --limit 20

# 3. Consultar el wiki
python wiki_agro.py query "¿Cuáles son los principales retos del arroz en Panamá?"

# 4. Revisar salud del wiki
python wiki_agro.py lint --verbose

# 5. Ver estadísticas
python wiki_agro.py stats
```

## Fuentes de Datos

| Tipo | Fuente | Cobertura |
|------|--------|-----------|
| RSS | La Prensa, TVN, Panamá América, La Estrella | Reciente |
| API | GDELT Project (gratis, sin clave) | 2015–2025 |
| Oficial | MIDA, IDIAP, BDA | Scraping manual |

## Estructura del Wiki

```
wiki/
├── index.md          # Catálogo maestro de páginas
├── log.md            # Actividad cronológica (append-only)
├── topics/           # Temas: cultivos, retos, regiones, políticas
├── entities/         # Organizaciones, instituciones, actores
└── summaries/        # Resúmenes de artículos individuales
```

## Metodología Karpathy

En lugar de RAG clásico (buscar → recuperar documentos crudos), el LLM **mantiene
activamente un wiki persistente** que acumula y sintetiza conocimiento con el tiempo.

El conocimiento **se compone**: cada artículo nuevo enriquece páginas existentes,
crea cross-references y actualiza el índice. Las respuestas a consultas valiosas
se guardan como nuevas páginas del wiki.

Ver [CLAUDE.md](CLAUDE.md) para el schema completo.
