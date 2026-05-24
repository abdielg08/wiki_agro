#!/usr/bin/env python3
"""
wiki_agro — CLI para el Wiki Agropecuario de Panamá
Metodología: Karpathy LLM Wiki (fuentes crudas → wiki persistente mantenido por LLM)

Comandos:
  fetch    Descargar artículos de noticias (RSS + GDELT histórico)
  ingest   Procesar artículos con Claude y actualizar el wiki
  query    Consultar el wiki con lenguaje natural
  lint     Revisar salud del wiki
  stats    Mostrar estadísticas del sistema
"""

import sys
import os
from pathlib import Path
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Load .env if present
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

console = Console()

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))


@click.group()
def cli():
    """Wiki Agropecuario de Panamá — Metodología Karpathy LLM Wiki."""
    pass


@cli.command()
@click.option("--mode", default="daily",
              type=click.Choice(["daily", "rss", "web", "gdelt", "worldbank", "all"]),
              help=(
                  "daily=RSS+web (rutina diaria), rss=solo RSS, web=solo DDG, "
                  "gdelt=crawl histórico 2015-2025, worldbank=Banco Mundial, all=todo"
              ))
@click.option("--limit", default=0, type=int, help="Máximo de artículos a guardar (0=ilimitado)")
@click.option("--no-text", is_flag=True, default=False, help="No descargar texto completo")
def fetch(mode, limit, no_text):
    """Descargar artículos de noticias agropecuarias de Panamá."""
    from fetch_news import run_fetch
    console.print(Panel(
        f"Modo: [bold]{mode}[/bold] | Límite: {'∞' if not limit else limit} | "
        f"Texto completo: {'No' if no_text else 'Sí'}",
        title="[bold cyan]Fetch — Descarga de Noticias[/bold cyan]",
    ))
    saved = run_fetch(mode=mode, limit=limit, extract_text=not no_text)
    console.print(f"\n[bold green]✓ {saved} artículos guardados[/bold green]")


@cli.command("fetch-historical")
@click.option("--years", default="2010-2025",
              help="Rango de años: 2010-2025, 2015-2020, etc.")
@click.option("--mode", default="all",
              type=click.Choice(["all", "gdelt", "cdx", "sitemap", "fao", "worldbank"]),
              help="gdelt=GDELT API, cdx=Wayback Machine, sitemap=WordPress sitemaps, fao=FAO docs, worldbank=BM proyectos")
@click.option("--domain", default=None,
              help="Restringir CDX/sitemap a un dominio, e.g. www.prensa.com")
@click.option("--limit", default=0, type=int,
              help="Máximo artículos a guardar (0=sin límite)")
def fetch_historical(years, mode, domain, limit):
    """
    Crawl histórico masivo — 15 años de noticias agropecuarias de Panamá.

    Fuentes: GDELT (2011+), Wayback Machine CDX, Sitemaps WordPress,
    FAO OpenKnowledge, World Bank Projects API.

    Ejemplos:
      python wiki_agro.py fetch-historical --years 2010-2025
      python wiki_agro.py fetch-historical --years 2015-2020 --mode gdelt --limit 500
      python wiki_agro.py fetch-historical --mode cdx --domain www.prensa.com --years 2010-2024
      python wiki_agro.py fetch-historical --mode sitemap --domain www.tvn-2.com
    """
    from fetch_historical import run_historical_fetch
    try:
        start_y, end_y = (int(y) for y in years.split("-"))
    except ValueError:
        console.print("[red]Error: formato de años debe ser YYYY-YYYY, e.g. 2010-2025[/red]")
        return
    console.print(Panel(
        f"Años: [bold]{start_y}–{end_y}[/bold] | Modo: [bold]{mode}[/bold] | "
        f"Dominio: {domain or 'todos'} | Límite: {'∞' if not limit else limit}",
        title="[bold cyan]Fetch Histórico — 15 Años[/bold cyan]",
    ))
    saved = run_historical_fetch(start_y, end_y, mode=mode, domain=domain, limit=limit)
    console.print(f"\n[bold green]✓ {saved} artículos históricos guardados[/bold green]")


@cli.command()
@click.option("--limit", default=5, type=int,
              help="Artículos a preparar por sesión (recomendado: 5-10)")
@click.option("--reprocess", is_flag=True, default=False,
              help="Incluir artículos ya ingestados")
@click.option("--strategy", default="score",
              type=click.Choice(["score", "recent", "oldest", "source"]),
              help="Orden de prioridad: score=más relevante, recent=más nuevo, oldest=más antiguo")
@click.option("--year", default=None,
              help="Filtrar por año o rango: 2020 o 2018-2021")
@click.option("--source", default=None,
              help="Filtrar por fuente: MIDA, LaPrensaEco, FAO, etc.")
def ingest(limit, reprocess, strategy, year, source):
    """
    Preparar artículos para que Claude Code los ingeste al wiki (sin API key).

    Selecciona los artículos más valiosos primero (por score de relevancia).
    Genera pending_ingest.md con el lote a procesar.

    Ejemplos:
      wiki_agro.py ingest --limit 5               # top 5 por score
      wiki_agro.py ingest --strategy oldest        # llenar el historial
      wiki_agro.py ingest --year 2020              # solo artículos de 2020
      wiki_agro.py ingest --source MIDA --limit 3  # solo artículos del MIDA
    """
    from ingest import run_prepare
    run_prepare(limit=limit, reprocess=reprocess, strategy=strategy,
                year_filter=year, source_filter=source)


@cli.command()
@click.option("--top", default=20, type=int, help="Mostrar top N artículos")
@click.option("--year", default=None, help="Filtrar por año o rango: 2020 o 2018-2021")
@click.option("--source", default=None, help="Filtrar por fuente")
def queue(top, year, source):
    """
    Ver el estado de la cola de ingesta: qué hay pendiente y por qué prioridad.

    Muestra distribución por fuente, año y top artículos por score de relevancia.
    """
    from ingest import find_pending
    from prioritize import prioritize, print_priority_report

    all_pending = find_pending(limit=0)
    if not all_pending:
        console.print("[bold green]✓ Cola vacía — todos los artículos han sido ingestados.[/bold green]")
        return
    # Apply filters for report
    filtered = [(p, a) for p, a in all_pending
                if (not year or a.get("date", "")[:4] == year[:4] if year and "-" not in year
                    else not year or (len(year) == 9 and
                                      int(year[:4]) <= int(a.get("date","9999")[:4]) <= int(year[5:])))
                and (not source or a.get("source") == source)]
    print_priority_report(filtered if (year or source) else all_pending, top_n=top)


@cli.command("mark-ingested")
@click.argument("url_or_slug")
def mark_ingested(url_or_slug):
    """Marcar un artículo como ingestado en processed.json."""
    from ingest import mark_ingested as _mark
    _mark(url_or_slug)


@cli.command("mark-all-ingested")
@click.option("--limit", default=0, type=int,
              help="Número de artículos a marcar (0 = todos los pendientes)")
def mark_all_ingested(limit):
    """Marcar artículos pendientes como ingestados (después de que Claude los procesó)."""
    from ingest import mark_all_ingested as _mark_all
    count = _mark_all(limit=limit)
    console.print(f"[bold green]✓ {count} artículos marcados como ingestados[/bold green]")


@cli.command()
@click.argument("question", nargs=-1, required=False)
@click.option("--no-save", is_flag=True, default=False, help="No guardar respuesta en el wiki")
def query(question, no_save):
    """Consultar el wiki en lenguaje natural."""
    from query import run_query
    if question:
        q = " ".join(question)
    else:
        console.print("[dim]Ingresa tu pregunta (Enter para enviar):[/dim]")
        q = input("> ").strip()
    if not q:
        console.print("[red]Pregunta vacía[/red]")
        return
    console.print(Panel(f"[italic]{q}[/italic]", title="[bold]Consulta[/bold]"))
    run_query(q, save_answers=not no_save)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Mostrar detalles de cada issue")
def lint(verbose):
    """Revisar salud del wiki (páginas huérfanas, links rotos, etc.)."""
    from lint import run_lint
    console.print(Panel("", title="[bold yellow]Lint — Salud del Wiki[/bold yellow]"))
    run_lint(verbose=verbose)


@cli.command()
def stats():
    """Mostrar estadísticas del sistema wiki."""
    from core import load_processed, WIKI_DIR, SOURCES_DIR

    processed = load_processed()
    # Filter out internal metadata keys (prefixed with _)
    articles = {k: v for k, v in processed.items() if not k.startswith("_") and isinstance(v, dict)}
    total_articles = len(articles)
    ingested = sum(1 for v in articles.values() if v.get("ingested"))
    pending = total_articles - ingested

    wiki_pages = list((WIKI_DIR).rglob("*.md"))
    topics = list((WIKI_DIR / "topics").glob("*.md"))
    entities = list((WIKI_DIR / "entities").glob("*.md"))
    summaries = list((WIKI_DIR / "summaries").glob("*.md"))

    # Source breakdown
    sources: dict[str, int] = {}
    for meta in articles.values():
        src = meta.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1

    console.print(Panel("", title="[bold]Estadísticas del Wiki Agropecuario[/bold]"))

    t = Table(box=box.SIMPLE)
    t.add_column("Métrica", style="cyan")
    t.add_column("Valor", style="bold")
    t.add_row("Artículos descargados", str(total_articles))
    t.add_row("Artículos ingestados", str(ingested))
    t.add_row("Pendientes de ingesta", str(pending))
    t.add_row("Total páginas wiki", str(len(wiki_pages)))
    t.add_row("  Topics", str(len(topics)))
    t.add_row("  Entidades", str(len(entities)))
    t.add_row("  Resúmenes", str(len(summaries)))
    console.print(t)

    if sources:
        console.print("\n[bold]Artículos por fuente:[/bold]")
        src_table = Table(box=box.SIMPLE)
        src_table.add_column("Fuente", style="cyan")
        src_table.add_column("Artículos", style="bold")
        for src, count in sorted(sources.items(), key=lambda x: -x[1])[:15]:
            src_table.add_row(src, str(count))
        console.print(src_table)


@cli.command()
def init_wiki():
    """Inicializar la estructura base del wiki (solo necesario la primera vez)."""
    _init_wiki_structure()
    console.print("[bold green]✓ Wiki inicializado[/bold green]")


def _init_wiki_structure():
    """Create initial wiki scaffold if not exists."""
    from pathlib import Path
    wiki_dir = Path(__file__).parent / "wiki"
    sources_dir = Path(__file__).parent / "sources" / "articles"
    sources_dir.mkdir(parents=True, exist_ok=True)
    (wiki_dir / "topics").mkdir(parents=True, exist_ok=True)
    (wiki_dir / "entities").mkdir(parents=True, exist_ok=True)
    (wiki_dir / "summaries").mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    # index.md
    index_path = wiki_dir / "index.md"
    if not index_path.exists():
        index_path.write_text(
            f"---\ntitle: Índice del Wiki Agropecuario de Panamá\n"
            f"type: overview\nlast_updated: {today}\n---\n\n"
            "# Wiki Agropecuario de Panamá\n\n"
            "> Wiki de noticias y conocimiento agropecuario panameño 2015–2025.\n"
            "> Mantenido por LLM siguiendo la metodología Karpathy.\n\n"
            "## Temas (topics/)\n\n"
            "*(Se poblarán automáticamente durante la ingesta)*\n\n"
            "## Entidades (entities/)\n\n"
            "*(Se poblarán automáticamente durante la ingesta)*\n\n"
            "## Artículos procesados\n\n"
            "*(Se agregarán automáticamente durante la ingesta)*\n",
            encoding="utf-8",
        )
        console.print("[dim]Creado: wiki/index.md[/dim]")

    # log.md
    log_path = wiki_dir / "log.md"
    if not log_path.exists():
        log_path.write_text(
            f"---\ntitle: Log de Actividad\ntype: overview\nlast_updated: {today}\n---\n\n"
            "# Log de Actividad del Wiki\n\n"
            "> Registro cronológico de ingestas, consultas y mantenimiento.\n\n"
            f"## {today} 00:00\n"
            "INIT: Wiki inicializado\n",
            encoding="utf-8",
        )
        console.print("[dim]Creado: wiki/log.md[/dim]")


if __name__ == "__main__":
    _init_wiki_structure()
    cli()
