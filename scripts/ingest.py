"""
Ingest articles into the wiki using the Claude API.

For each unprocessed article:
  1. Read article text from sources/articles/
  2. Load relevant wiki context (index + related pages)
  3. Ask Claude to extract structured knowledge
  4. Write/update wiki pages
  5. Update index.md and log.md
  6. Mark article as ingested in processed.json
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

import anthropic
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent))
from core import (
    console, load_processed, save_processed, load_article,
    read_wiki_page, write_wiki_page, append_log, load_wiki_index,
    SOURCES_DIR, WIKI_DIR, ROOT
)

MODEL = os.getenv("WIKI_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.getenv("WIKI_MAX_TOKENS", "8192"))


def get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]Error: ANTHROPIC_API_KEY not set.[/red]")
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def load_claude_md() -> str:
    path = ROOT / "CLAUDE.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_relevant_wiki_pages(topics: list[str], entities: list[str]) -> str:
    """Load wiki pages likely relevant to the article for context."""
    pages_content = []
    checked = set()

    def try_load(rel_path: str):
        if rel_path in checked:
            return
        checked.add(rel_path)
        content = read_wiki_page(rel_path)
        if content:
            pages_content.append(f"\n### wiki/{rel_path}\n{content[:1500]}")

    try_load("index.md")

    for topic in topics[:4]:
        slug = topic.lower().replace(" ", "_").replace("/", "_")
        try_load(f"topics/{slug}.md")

    for entity in entities[:3]:
        slug = entity.lower().replace(" ", "_").replace("/", "_")
        try_load(f"entities/{slug}.md")

    return "\n".join(pages_content) if pages_content else "(wiki vacío, primera ingesta)"


INGEST_SYSTEM = """\
Eres el mantenedor del Wiki Agropecuario de Panamá, siguiendo la metodología \
Karpathy de wiki persistente mantenido por LLM.

Tu tarea es analizar un artículo de noticias agropecuarias de Panamá y retornar \
un JSON con el conocimiento extraído y las actualizaciones necesarias al wiki.

Schema del wiki (CLAUDE.md):
{claude_md}

Estado actual del wiki relevante:
{wiki_context}

REGLAS CRÍTICAS:
- Responde ÚNICAMENTE con JSON válido (sin markdown, sin texto extra)
- Las páginas wiki deben estar en markdown con frontmatter YAML
- Máximo 5 wiki_updates por artículo
- Usa español panameño en todo el contenido
- Fechas en formato YYYY-MM-DD
- Cita la fuente y URL en cada hecho clave
"""

INGEST_USER = """\
Analiza este artículo y retorna el JSON de actualización del wiki:

ARTÍCULO:
URL: {url}
Fuente: {source}
Fecha: {date}
Título: {title}

Texto completo:
{text}

Retorna un objeto JSON con exactamente esta estructura:
{{
  "summary": "Resumen de 2-3 oraciones del artículo",
  "entities": ["entidad1", "entidad2"],
  "topics": ["tema1", "tema2"],
  "region": "región de Panamá o 'Nacional'",
  "crops_mentioned": ["cultivo1"],
  "key_facts": [
    {{"fact": "hecho importante", "date": "YYYY-MM-DD", "value": "dato si aplica"}}
  ],
  "challenges": ["reto1", "reto2"],
  "opportunities": ["oportunidad1"],
  "wiki_updates": [
    {{
      "path": "summaries/YYYYMMDD_fuente_slug.md",
      "action": "create",
      "content": "---\\ntitle: ...\\ntype: summary\\n...\\n---\\n\\n# Título\\n..."
    }},
    {{
      "path": "topics/arroz.md",
      "action": "update",
      "section": "## Hechos Clave",
      "content": "Contenido completo actualizado de la página"
    }}
  ],
  "index_entry": "- [Título corto](summaries/slug.md) — descripción una línea [Fuente, Fecha]",
  "log_entry": "INGEST: artículo procesado de [Fuente], tema: [temas]"
}}
"""


def call_claude_ingest(client: anthropic.Anthropic, article: dict, wiki_context: str, claude_md: str) -> dict | None:
    """Call Claude to extract knowledge from article. Returns parsed JSON or None."""
    text = article.get("full_text") or article.get("summary_raw") or ""
    if not text.strip():
        return None

    system = INGEST_SYSTEM.format(
        claude_md=claude_md[:3000],
        wiki_context=wiki_context[:4000],
    )
    user = INGEST_USER.format(
        url=article.get("url", ""),
        source=article.get("source", ""),
        date=article.get("date", ""),
        title=article.get("title", ""),
        text=text[:5000],
    )

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user}],
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw
            if raw.endswith("```"):
                raw = raw[:-3]
        return json.loads(raw)
    except json.JSONDecodeError as e:
        console.print(f"  [red]JSON parse error: {e}[/red]")
        console.print(f"  Raw response: {raw[:300]}")
        return None
    except Exception as e:
        console.print(f"  [red]Claude API error: {e}[/red]")
        return None


def apply_wiki_updates(updates: list[dict]) -> list[str]:
    """Write wiki page updates. Returns list of paths written."""
    written = []
    for upd in updates:
        path = upd.get("path", "").strip("/")
        content = upd.get("content", "")
        if not path or not content:
            continue
        write_wiki_page(path, content)
        written.append(path)
        console.print(f"  [blue]→ wiki/{path}[/blue]")
    return written


def update_index(entry: str) -> None:
    """Append a new entry to wiki/index.md."""
    idx_path = WIKI_DIR / "index.md"
    if not idx_path.exists():
        return
    content = idx_path.read_text(encoding="utf-8")
    marker = "## Artículos procesados"
    if marker in content:
        content = content.replace(marker, f"{marker}\n{entry}")
    else:
        content += f"\n{marker}\n{entry}\n"
    idx_path.write_text(content, encoding="utf-8")


def ingest_article(path: Path, client: anthropic.Anthropic, claude_md: str, processed: dict) -> bool:
    """Ingest a single article. Returns True if successful."""
    article = load_article(path)
    url = article.get("url", "")
    title = article.get("title", "")[:70]

    console.print(f"\n[bold]Procesando:[/bold] {title}")

    # Load wiki context based on title keywords
    keywords = title.lower().split()[:5]
    wiki_ctx = load_relevant_wiki_pages(keywords, [])

    result = call_claude_ingest(client, article, wiki_ctx, claude_md)
    if result is None:
        console.print("  [yellow]Skipped (no result)[/yellow]")
        return False

    # Apply wiki page updates
    written = apply_wiki_updates(result.get("wiki_updates", []))

    # Update index
    if result.get("index_entry"):
        update_index(result["index_entry"])

    # Append to log
    log_entry = result.get("log_entry", f"INGEST: {title[:50]}")
    append_log(
        f"{log_entry}\n"
        f"  URL: {url}\n"
        f"  Temas: {', '.join(result.get('topics', []))}\n"
        f"  Páginas actualizadas: {', '.join(written) if written else 'ninguna'}"
    )

    # Mark as ingested
    if url in processed:
        processed[url]["ingested"] = True
        processed[url]["ingested_at"] = datetime.now().isoformat()
        processed[url]["topics"] = result.get("topics", [])
        processed[url]["wiki_pages"] = written

    console.print(f"  [green]✓ Completado[/green] — {len(written)} páginas wiki actualizadas")
    return True


def run_ingest(limit: int = 0, reprocess: bool = False) -> int:
    """Ingest all unprocessed articles. Returns count ingested."""
    client = get_client()
    claude_md = load_claude_md()
    processed = load_processed()

    # Find articles to process
    to_process = []
    for path in sorted(SOURCES_DIR.glob("*.json")):
        url_key = None
        for url, meta in processed.items():
            if meta.get("path") == str(path):
                url_key = url
                break
        already_ingested = url_key and processed.get(url_key, {}).get("ingested", False)
        if not already_ingested or reprocess:
            to_process.append(path)

    console.print(f"\n[bold]{len(to_process)} artículos pendientes de ingesta[/bold]")

    count = 0
    for i, path in enumerate(to_process):
        if limit and count >= limit:
            break
        success = ingest_article(path, client, claude_md, processed)
        if success:
            count += 1
        # Save progress every 5 articles
        if i % 5 == 0:
            save_processed(processed)

    save_processed(processed)
    console.print(f"\n[bold green]Ingestados: {count} artículos[/bold green]")
    return count


if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    run_ingest(limit=limit)
