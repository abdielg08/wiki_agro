"""
Priorización y filtrado de artículos para ingesta eficiente.

Con miles de artículos en sources/, no tiene sentido ingestarlos todos.
Este módulo prioriza según:
  1. Nivel de confianza de la fuente (MIDA > La Prensa > GDELT genérico)
  2. Relevancia temática (términos específicos de alta prioridad)
  3. Fecha (artículos más recientes primero, o por época)
  4. Fuentes no representadas aún en el wiki
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

# Términos de alta prioridad temática (puntaje extra)
HIGH_PRIORITY_TERMS = [
    "MIDA", "IDIAP", "BDA", "ANAGAN", "ARAP",
    "producción", "cosecha", "rendimiento", "toneladas", "hectáreas",
    "precio", "exportación", "importación", "sequía", "El Niño",
    "gusano cogollero", "sigatoka", "fusarium", "plaga", "enfermedad",
    "crédito", "préstamo", "subsidio", "semilla",
    "arroz", "maíz", "plátano", "café", "cacao", "caña",
    "ganadería", "bovino", "porcino", "avicultura", "acuicultura",
]

# Fuentes con mayor valor informativo
SOURCE_WEIGHT = {
    "MIDA": 10,
    "IDIAP": 10,
    "BDA": 9,
    "FAO": 9,
    "BancoMundial": 8,
    "IICA": 8,
    "OIRSA": 8,
    "LaPrensaEco": 7,
    "LaPrensaGeneral": 6,
    "PanamaAmerica": 6,
    "TVNNoticias": 5,
    "LaEstrella": 5,
    "ElCapital": 5,
}


def score_article(article: dict) -> float:
    """Score an article 0-100 based on source quality and content relevance."""
    score = 0.0

    # Source weight (0-40 pts)
    source = article.get("source", "")
    score += SOURCE_WEIGHT.get(source, 3) * 4  # max 40

    # Trust level (0-20 pts)
    trust = article.get("trust_level", 3)
    score += (6 - trust) * 5  # level 1=25, 2=20, 3=15, 4=10

    # Content relevance (0-30 pts)
    text = (article.get("title", "") + " " + (article.get("summary_raw") or "")).lower()
    hits = sum(1 for t in HIGH_PRIORITY_TERMS if t.lower() in text)
    score += min(hits * 3, 30)

    # Recency bonus (0-10 pts) — more recent = slightly higher priority
    date_str = article.get("date", "")
    if date_str:
        try:
            age_years = (datetime.now() - datetime.strptime(date_str[:10], "%Y-%m-%d")).days / 365
            score += max(0, 10 - age_years)  # 10 pts if today, 0 if >10 years
        except Exception:
            pass

    return round(score, 1)


def get_wiki_coverage(wiki_dir: Path) -> dict[str, int]:
    """Count how many articles have been ingested per topic/year."""
    coverage: dict[str, int] = defaultdict(int)
    log_path = wiki_dir / "log.md"
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("## 20"):
                try:
                    year = int(line.strip()[3:7])
                    coverage[str(year)] += 1
                except Exception:
                    pass
    return dict(coverage)


def prioritize(
    pending: list[tuple[Path, dict]],
    strategy: str = "score",
    year_filter: str | None = None,
    source_filter: str | None = None,
    min_score: float = 0.0,
) -> list[tuple[Path, dict, float]]:
    """
    Sort and filter pending articles.

    strategy:
      'score'   — highest relevance score first (default)
      'recent'  — most recent first
      'oldest'  — oldest first (to fill historical gaps)
      'source'  — group by source

    year_filter:  '2018' or '2018-2020'
    source_filter: 'LaPrensaEco' or 'MIDA'
    min_score:  skip articles below this score
    """
    scored = []
    for path, article in pending:
        # Year filter
        if year_filter:
            date_str = article.get("date", "")
            if date_str:
                try:
                    year = int(date_str[:4])
                    if "-" in year_filter:
                        y1, y2 = (int(y) for y in year_filter.split("-"))
                        if not (y1 <= year <= y2):
                            continue
                    else:
                        if year != int(year_filter):
                            continue
                except Exception:
                    pass
            elif year_filter:
                continue  # skip undated if filtering by year

        # Source filter
        if source_filter and article.get("source", "") != source_filter:
            continue

        s = score_article(article)
        if s < min_score:
            continue
        scored.append((path, article, s))

    if strategy == "score":
        scored.sort(key=lambda x: -x[2])
    elif strategy == "recent":
        scored.sort(key=lambda x: x[1].get("date", ""), reverse=True)
    elif strategy == "oldest":
        scored.sort(key=lambda x: x[1].get("date", "9999"))
    elif strategy == "source":
        scored.sort(key=lambda x: (x[1].get("source", ""), -x[2]))

    return scored


def print_priority_report(
    pending: list[tuple[Path, dict]],
    top_n: int = 20,
    wiki_dir: Path | None = None,
) -> None:
    """Print a summary report of what's in the queue and top articles."""
    # Summary by source
    by_source: dict[str, int] = defaultdict(int)
    by_year: dict[str, int] = defaultdict(int)
    scores = []

    for path, article in pending:
        src = article.get("source", "unknown")
        by_source[src] += 1
        date = article.get("date", "")
        if date and len(date) >= 4:
            by_year[date[:4]] += 1
        scores.append(score_article(article))

    console.print(f"\n[bold]Cola de ingesta: {len(pending)} artículos pendientes[/bold]")
    avg_score = sum(scores) / len(scores) if scores else 0
    console.print(f"Score promedio: {avg_score:.1f}/100\n")

    # By source
    t = Table("Fuente", "Artículos", "Score promedio", box=box.SIMPLE)
    src_scores: dict[str, list] = defaultdict(list)
    for path, article in pending:
        src_scores[article.get("source", "?")].append(score_article(article))
    for src, count in sorted(by_source.items(), key=lambda x: -x[1])[:12]:
        avg = sum(src_scores[src]) / len(src_scores[src])
        t.add_row(src, str(count), f"{avg:.1f}")
    console.print(t)

    # By year
    t2 = Table("Año", "Artículos", box=box.SIMPLE)
    for year in sorted(by_year.keys(), reverse=True)[:10]:
        t2.add_row(year, str(by_year[year]))
    console.print(t2)

    # Top N by score
    scored = prioritize(pending, strategy="score")
    console.print(f"\n[bold]Top {top_n} artículos por prioridad:[/bold]")
    t3 = Table("Score", "Fuente", "Fecha", "Título", box=box.SIMPLE)
    for path, article, score in scored[:top_n]:
        t3.add_row(
            f"{score:.0f}",
            article.get("source", "?"),
            article.get("date", "")[:10],
            (article.get("title") or "")[:55],
        )
    console.print(t3)
