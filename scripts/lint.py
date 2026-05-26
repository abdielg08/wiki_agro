"""
Wiki health check (Lint).
Finds: orphan pages, missing cross-references, stale metadata,
broken internal links, and frontmatter inconsistencies.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

import yaml
from rich.console import Console
from rich.table import Table
from rich import box

sys.path.insert(0, str(Path(__file__).parent))
from core import (
    console, list_wiki_pages, extract_frontmatter, append_log, WIKI_DIR
)

REQUIRED_FRONTMATTER = {"title", "type", "last_updated"}
VALID_TYPES = {"topic", "entity", "summary", "overview", "query_answer"}


def _all_page_links(content: str) -> set[str]:
    """Extract all internal wiki links from markdown content."""
    return set(re.findall(r'\[.*?\]\(([^)]+\.md)\)', content))


def check_frontmatter(pages: list[Path]) -> list[dict]:
    """Check all pages have valid frontmatter."""
    issues = []
    for page in pages:
        content = page.read_text(encoding="utf-8")
        fm, _ = extract_frontmatter(content)
        rel = str(page.relative_to(WIKI_DIR))
        if not fm:
            issues.append({"page": rel, "issue": "Sin frontmatter YAML"})
            continue
        missing = REQUIRED_FRONTMATTER - set(fm.keys())
        if missing:
            issues.append({"page": rel, "issue": f"Frontmatter incompleto: {missing}"})
        if "type" in fm and fm["type"] not in VALID_TYPES:
            issues.append({"page": rel, "issue": f"Tipo inválido: {fm['type']}"})
    return issues


def check_orphan_pages(pages: list[Path]) -> list[str]:
    """Find pages with no incoming links from other wiki pages."""
    all_links: set[str] = set()
    page_names = set()
    for page in pages:
        rel = str(page.relative_to(WIKI_DIR))
        page_names.add(rel)
        page_names.add(page.name)
        content = page.read_text(encoding="utf-8")
        for link in _all_page_links(content):
            all_links.add(link)
            all_links.add(Path(link).name)

    orphans = []
    for page in pages:
        rel = str(page.relative_to(WIKI_DIR))
        if page.name in ("index.md", "log.md"):
            continue
        if rel not in all_links and page.name not in all_links:
            orphans.append(rel)
    return orphans


def check_broken_links(pages: list[Path]) -> list[dict]:
    """Find internal links pointing to non-existent pages."""
    page_paths = {str(p.relative_to(WIKI_DIR)) for p in pages}
    page_names = {p.name for p in pages}
    issues = []
    for page in pages:
        rel = str(page.relative_to(WIKI_DIR))
        content = page.read_text(encoding="utf-8")
        for link in _all_page_links(content):
            if link not in page_paths and Path(link).name not in page_names:
                issues.append({"page": rel, "broken_link": link})
    return issues


def check_stale_pages(pages: list[Path], max_days: int = 365) -> list[dict]:
    """Find pages not updated in max_days (based on last_updated frontmatter)."""
    from datetime import datetime
    stale = []
    today = datetime.now().date()
    for page in pages:
        content = page.read_text(encoding="utf-8")
        fm, _ = extract_frontmatter(content)
        last_updated = fm.get("last_updated")
        if not last_updated:
            continue
        try:
            last_date = datetime.strptime(str(last_updated), "%Y-%m-%d").date()
            days_old = (today - last_date).days
            if days_old > max_days:
                stale.append({
                    "page": str(page.relative_to(WIKI_DIR)),
                    "last_updated": str(last_updated),
                    "days_old": days_old,
                })
        except Exception:
            pass
    return stale


def check_index_coverage(pages: list[Path]) -> list[str]:
    """Find pages not listed in index.md."""
    index_path = WIKI_DIR / "index.md"
    if not index_path.exists():
        return []
    index_content = index_path.read_text(encoding="utf-8")
    unlisted = []
    for page in pages:
        if page.name in ("index.md", "log.md"):
            continue
        rel = str(page.relative_to(WIKI_DIR))
        if page.name not in index_content and rel not in index_content:
            unlisted.append(rel)
    return unlisted


def run_lint(verbose: bool = False) -> dict:
    """Run all lint checks. Returns summary dict."""
    pages = list_wiki_pages()
    console.print(f"\n[bold]Lint del wiki — {len(pages)} páginas[/bold]\n")

    results = {}

    # 1. Frontmatter
    fm_issues = check_frontmatter(pages)
    results["frontmatter_issues"] = fm_issues
    if fm_issues:
        console.print(f"[red]● Frontmatter inválido: {len(fm_issues)} páginas[/red]")
        if verbose:
            for iss in fm_issues:
                console.print(f"  {iss['page']}: {iss['issue']}")
    else:
        console.print("[green]✓ Frontmatter: todo OK[/green]")

    # 2. Orphan pages
    orphans = check_orphan_pages(pages)
    results["orphan_pages"] = orphans
    if orphans:
        console.print(f"[yellow]● Páginas huérfanas: {len(orphans)}[/yellow]")
        if verbose:
            for o in orphans:
                console.print(f"  {o}")
    else:
        console.print("[green]✓ Sin páginas huérfanas[/green]")

    # 3. Broken links
    broken = check_broken_links(pages)
    results["broken_links"] = broken
    if broken:
        console.print(f"[red]● Links rotos: {len(broken)}[/red]")
        if verbose:
            for b in broken:
                console.print(f"  {b['page']} → {b['broken_link']}")
    else:
        console.print("[green]✓ Sin links rotos[/green]")

    # 4. Stale pages
    stale = check_stale_pages(pages)
    results["stale_pages"] = stale
    if stale:
        console.print(f"[yellow]● Páginas desactualizadas (>1 año): {len(stale)}[/yellow]")
        if verbose:
            for s in stale:
                console.print(f"  {s['page']} (última actualización: {s['last_updated']})")
    else:
        console.print("[green]✓ Sin páginas desactualizadas[/green]")

    # 5. Index coverage
    unlisted = check_index_coverage(pages)
    results["unlisted_pages"] = unlisted
    if unlisted:
        console.print(f"[yellow]● Páginas no en index: {len(unlisted)}[/yellow]")
        if verbose:
            for u in unlisted:
                console.print(f"  {u}")
    else:
        console.print("[green]✓ Index completo[/green]")

    # Summary
    total_issues = (
        len(fm_issues) + len(orphans) + len(broken) + len(stale) + len(unlisted)
    )
    console.print(f"\n[bold]Total issues: {total_issues}[/bold]")

    append_log(
        f"LINT: {len(pages)} páginas revisadas, {total_issues} issues encontrados\n"
        f"  frontmatter:{len(fm_issues)}, huérfanas:{len(orphans)}, "
        f"broken_links:{len(broken)}, stale:{len(stale)}, no_index:{len(unlisted)}"
    )

    return results


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    run_lint(verbose=verbose)
