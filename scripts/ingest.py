"""
Ingest — preparación de artículos para que Claude Code los procese.

NO usa la Anthropic API. Claude Code (sesión Pro) hace el trabajo de IA.

Flujo:
  1. `python wiki_agro.py fetch`  — descarga artículos (Python puro)
  2. `python wiki_agro.py ingest` — muestra qué artículos procesar y cómo
  3. Claude Code lee este output y actualiza el wiki directamente en la sesión

Para marcar un artículo como ingestado después de que Claude lo procese:
  python wiki_agro.py mark-ingested <url_o_slug>
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

sys.path.insert(0, str(Path(__file__).parent))
from core import (
    console, load_processed, save_processed, load_article,
    load_wiki_index, append_log, article_entries, SOURCES_DIR, WIKI_DIR, ROOT
)


def find_pending(limit: int = 0, reprocess: bool = False) -> list[tuple[Path, dict]]:
    """Return list of (path, article) for articles not yet ingested."""
    processed = load_processed()
    articles = article_entries(processed)
    pending = []
    for path in sorted(SOURCES_DIR.glob("*.json")):
        article = load_article(path)
        url = article.get("url", "")
        meta = articles.get(url, {})
        if not meta.get("ingested") or reprocess:
            has_text = bool(article.get("full_text") or article.get("summary_raw"))
            if has_text:
                pending.append((path, article))
    if limit:
        pending = pending[:limit]
    return pending


def format_article_for_claude(path: Path, article: dict, index: int, total: int) -> str:
    """Format one article as a markdown block for Claude to read."""
    text = article.get("full_text") or article.get("summary_raw") or ""
    return (
        f"---\n"
        f"## Artículo {index}/{total}: {article.get('title', 'Sin título')}\n\n"
        f"- **Archivo**: `{path.name}`\n"
        f"- **URL**: {article.get('url', '')}\n"
        f"- **Fuente**: {article.get('source', '')} (nivel de confianza: {article.get('trust_level', 3)})\n"
        f"- **Fecha**: {article.get('date', 'desconocida')}\n\n"
        f"**Texto**:\n\n{text[:3000]}\n"
    )


def run_prepare(
    limit: int = 5,
    reprocess: bool = False,
    strategy: str = "score",
    year_filter: str | None = None,
    source_filter: str | None = None,
) -> int:
    """
    Print a structured prompt for Claude Code to process pending articles.
    Selects articles by priority (highest score first by default).
    Returns number of articles ready to process.
    """
    from prioritize import prioritize

    all_pending = find_pending(limit=0, reprocess=reprocess)
    scored = prioritize(
        all_pending,
        strategy=strategy,
        year_filter=year_filter,
        source_filter=source_filter,
    )
    pending = [(path, article) for path, article, _ in scored[:limit]]

    if not pending:
        console.print("[bold green]✓ No hay artículos pendientes de ingesta.[/bold green]")
        return 0

    claude_md = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    wiki_index = load_wiki_index()

    # Build the prompt that Claude Code will see
    prompt_parts = [
        "# Instrucciones de Ingesta para Claude Code\n",
        "Eres el mantenedor del **Wiki Agropecuario de Panamá**. "
        "Procesa cada artículo a continuación siguiendo el schema de `CLAUDE.md`.\n",
        "## Schema del Wiki (CLAUDE.md)\n",
        f"```\n{claude_md[:2000]}\n```\n",
        "## Índice actual del Wiki\n",
        f"```\n{wiki_index[:1500]}\n```\n",
        f"## {len(pending)} Artículos para procesar\n",
        "Para cada artículo:\n"
        "1. Crea `wiki/summaries/<slug>.md` con el resumen\n"
        "2. Actualiza hasta 3 páginas de `wiki/topics/` relevantes\n"
        "3. Actualiza hasta 2 páginas de `wiki/entities/` si aplica\n"
        "4. Actualiza `wiki/index.md` con la nueva entrada\n"
        "5. Agrega entrada a `wiki/log.md`\n\n",
    ]

    for i, (path, article) in enumerate(pending, 1):
        prompt_parts.append(format_article_for_claude(path, article, i, len(pending)))

    prompt_parts.append(
        "\n---\n"
        "**Después de procesar todos los artículos**, ejecuta:\n"
        "```bash\n"
        + "\n".join(
            f"python wiki_agro.py mark-ingested '{article.get('url', '')}'"
            for _, article in pending
        )
        + "\n```\n"
    )

    full_prompt = "\n".join(prompt_parts)

    # Save to a file so Claude Code can read it
    ingest_file = ROOT / "pending_ingest.md"
    ingest_file.write_text(full_prompt, encoding="utf-8")

    console.print(Panel(
        f"[bold]{len(pending)} artículos listos para ingestar.[/bold]\n\n"
        f"El prompt ha sido guardado en [cyan]pending_ingest.md[/cyan]\n\n"
        f"Claude Code procesará los artículos automáticamente al leer ese archivo.\n"
        f"Puedes decirle: [italic]\"Lee pending_ingest.md y actualiza el wiki\"[/italic]",
        title="[bold magenta]Ingest — Listo para Claude Code[/bold magenta]",
    ))
    return len(pending)


def mark_ingested(url_or_slug: str) -> bool:
    """Mark an article as ingested in processed.json."""
    processed = load_processed()
    for url, meta in article_entries(processed).items():
        if url == url_or_slug or url_or_slug in meta.get("path", ""):
            meta["ingested"] = True
            meta["ingested_at"] = datetime.now().isoformat()
            save_processed(processed)
            console.print(f"[green]✓ Marcado como ingestado: {url[:60]}[/green]")
            return True
    console.print(f"[red]No encontrado: {url_or_slug}[/red]")
    return False


def mark_all_ingested(limit: int = 0) -> int:
    """Mark the first `limit` pending articles as ingested (after Claude processed them).

    Uses the same score-based priority order as `run_prepare`/`ingest`, so the
    articles marked here match the ones actually shown in pending_ingest.md
    (find_pending's raw filename order does not match that selection).
    """
    from prioritize import prioritize

    processed = load_processed()
    articles = article_entries(processed)
    all_pending = find_pending(limit=0)
    scored = prioritize(all_pending, strategy="score")
    pending = [(path, article) for path, article, _ in scored[:limit]] if limit else \
              [(path, article) for path, article, _ in scored]
    count = 0
    for _, article in pending:
        url = article.get("url", "")
        if url in articles:
            processed[url]["ingested"] = True
            processed[url]["ingested_at"] = datetime.now().isoformat()
            count += 1
    save_processed(processed)
    append_log(
        f"INGEST: {count} artículos marcados como ingestados por sesión Claude Code"
    )
    return count


# ── Ingest usando Anthropic SDK (opcional, solo si hay API key) ───────────────

def run_ingest_api(limit: int = 0, reprocess: bool = False) -> int:
    """
    Fallback: ingest via Anthropic API if ANTHROPIC_API_KEY is set.
    Only used if explicitly requested via --api flag.
    """
    try:
        import anthropic
        import os
    except ImportError:
        console.print("[red]anthropic SDK no instalado. Usa: pip install anthropic[/red]")
        return 0

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY no configurada.[/red]")
        return 0

    # Lazy import to avoid breaking the module when anthropic isn't installed
    from _ingest_api import run_ingest_with_api
    return run_ingest_with_api(limit=limit, reprocess=reprocess)
