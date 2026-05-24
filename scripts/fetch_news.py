"""
Fetch agro news from Panama from multiple sources:
  1. RSS feeds (recent articles)
  2. GDELT API (historical, 2015–2025, free, no key needed)
  3. Direct website scraping as fallback
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator
from urllib.parse import urljoin, quote_plus

import feedparser
import requests
import trafilatura
import yaml
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from rich.console import Console
from rich.progress import track

sys.path.insert(0, str(Path(__file__).parent))
from core import (
    console, load_config, load_processed, save_processed,
    save_article, url_to_slug, ROOT
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; WikiAgro/1.0; "
        "+https://github.com/abdielg08/wiki_agro)"
    )
}
REQUEST_DELAY = 1.5  # seconds between requests


def _get(url: str, timeout: int = 15, **kwargs) -> requests.Response | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, **kwargs)
        resp.raise_for_status()
        return resp
    except Exception as e:
        console.print(f"  [red]GET error {url}: {e}[/red]")
        return None


def _extract_text(url: str) -> str | None:
    """Extract main article text from a URL using trafilatura."""
    try:
        resp = _get(url)
        if resp is None:
            return None
        downloaded = trafilatura.extract(
            resp.text,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
            favor_precision=True,
        )
        return downloaded
    except Exception as e:
        console.print(f"  [yellow]Extract error {url}: {e}[/yellow]")
        return None


def is_agro_relevant(title: str, text: str = "", config: dict = None) -> bool:
    """Check if article is relevant to Panama agro sector."""
    if config is None:
        config = load_config()
    terms = (
        config.get("search_terms", {}).get("primary", [])
        + config.get("search_terms", {}).get("secondary", [])
    )
    combined = (title + " " + (text or "")).lower()
    return any(t.lower() in combined for t in terms)


# ─── RSS FETCHER ─────────────────────────────────────────────────────────────

def fetch_rss(source: dict, config: dict) -> Iterator[dict]:
    """Yield article dicts from an RSS feed."""
    rss_url = source.get("rss")
    if not rss_url:
        return
    console.print(f"  Parsing RSS: [cyan]{source['name']}[/cyan]")
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        url = entry.get("link", "")
        title = entry.get("title", "")
        if not url or not title:
            continue
        pub_date = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            pub_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        summary = entry.get("summary", "")
        if not is_agro_relevant(title, summary, config):
            continue
        yield {
            "url": url,
            "title": title,
            "date": pub_date,
            "source": source["name"],
            "trust_level": source.get("trust_level", 3),
            "language": source.get("language", "es"),
            "country": source.get("country", "PA"),
            "summary_raw": summary,
            "full_text": None,
        }


# ─── GDELT FETCHER ────────────────────────────────────────────────────────────

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

def _gdelt_query_string(terms: list[str]) -> str:
    """Build a GDELT query combining terms with OR."""
    escaped = [f'"{t}"' if " " in t else t for t in terms]
    return " OR ".join(escaped)


def fetch_gdelt_batch(
    query: str,
    start_date: str,
    end_date: str,
    max_records: int = 250,
) -> list[dict]:
    """Fetch one GDELT batch. Returns list of article dicts."""
    params = {
        "query": f"{query} sourcecountry:PA",
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json",
        "sourcelang": "spa",
        "startdatetime": start_date.replace("-", "") + "000000",
        "enddatetime": end_date.replace("-", "") + "235959",
        "sort": "DateDesc",
    }
    resp = _get(GDELT_URL, params=params, timeout=30)
    if resp is None:
        return []
    try:
        data = resp.json()
    except Exception:
        return []
    articles = []
    for item in data.get("articles", []):
        url = item.get("url", "")
        title = item.get("title", "")
        if not url or not title:
            continue
        date_raw = item.get("seendate", "")
        try:
            date = datetime.strptime(date_raw[:8], "%Y%m%d").strftime("%Y-%m-%d")
        except Exception:
            date = ""
        articles.append({
            "url": url,
            "title": title,
            "date": date,
            "source": item.get("domain", ""),
            "trust_level": 3,
            "language": "es",
            "country": "PA",
            "summary_raw": "",
            "full_text": None,
            "gdelt": True,
        })
    return articles


def fetch_gdelt_historical(config: dict) -> Iterator[dict]:
    """Iterate GDELT over quarterly windows for 10 years."""
    cfg = config.get("gdelt", {})
    terms_primary = config.get("search_terms", {}).get("primary", [])
    query = _gdelt_query_string(terms_primary)

    start = datetime.strptime(cfg.get("date_range", {}).get("start", "2015-01-01"), "%Y-%m-%d")
    end = datetime.strptime(cfg.get("date_range", {}).get("end", "2025-12-31"), "%Y-%m-%d")

    # Split into quarterly windows to maximize coverage
    current = start
    while current < end:
        next_quarter = current + timedelta(days=90)
        if next_quarter > end:
            next_quarter = end
        window_start = current.strftime("%Y-%m-%d")
        window_end = next_quarter.strftime("%Y-%m-%d")
        console.print(
            f"  GDELT [cyan]{window_start}[/cyan] → [cyan]{window_end}[/cyan]"
        )
        batch = fetch_gdelt_batch(query, window_start, window_end)
        console.print(f"    → {len(batch)} artículos encontrados")
        for article in batch:
            yield article
        current = next_quarter + timedelta(days=1)
        time.sleep(REQUEST_DELAY)


# ─── FULL TEXT ENRICHMENT ────────────────────────────────────────────────────

def enrich_with_fulltext(article: dict) -> dict:
    """Download and attach full article text."""
    if article.get("full_text"):
        return article
    text = _extract_text(article["url"])
    article["full_text"] = text
    time.sleep(REQUEST_DELAY)
    return article


# ─── MAIN FETCH COMMAND ──────────────────────────────────────────────────────

def run_fetch(
    mode: str = "all",
    limit: int = 0,
    extract_text: bool = True,
    skip_duplicates: bool = True,
) -> int:
    """
    Main fetch entry point.

    mode: 'rss' | 'gdelt' | 'all'
    limit: max articles to save (0 = unlimited)
    extract_text: download full article text
    Returns number of new articles saved.
    """
    config = load_config()
    processed = load_processed()
    saved = 0

    def _process_article(art: dict) -> bool:
        nonlocal saved
        url = art.get("url", "")
        if skip_duplicates and url in processed:
            return False
        if extract_text and not art.get("full_text"):
            art = enrich_with_fulltext(art)
        # Skip articles with no extractable text
        if extract_text and not art.get("full_text"):
            return False
        path = save_article(art)
        processed[url] = {
            "saved_at": datetime.now().isoformat(),
            "path": str(path),
            "title": art.get("title", ""),
            "date": art.get("date", ""),
            "source": art.get("source", ""),
            "ingested": False,
        }
        saved += 1
        console.print(
            f"  [green]✓[/green] [{saved}] {art.get('title', '')[:70]}"
        )
        return True

    if mode in ("rss", "all"):
        console.print("\n[bold]── Fetching RSS feeds ──[/bold]")
        all_sources = []
        for group in config.get("sources", {}).values():
            all_sources.extend(group)
        for source in all_sources:
            for article in fetch_rss(source, config):
                _process_article(article)
                if limit and saved >= limit:
                    break
            if limit and saved >= limit:
                break

    if mode in ("gdelt", "all"):
        console.print("\n[bold]── Fetching GDELT historical (2015–2025) ──[/bold]")
        for article in fetch_gdelt_historical(config):
            _process_article(article)
            if limit and saved >= limit:
                break

    save_processed(processed)
    console.print(f"\n[bold green]Total guardados: {saved} artículos[/bold green]")
    return saved


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    run_fetch(mode=mode, limit=limit)
