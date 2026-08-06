"""
Fetch agro news from Panama from multiple sources:
  1. RSS feeds (recent articles — all configured sources)
  2. DuckDuckGo web search (targeted per domain, no API key)
  3. World Bank API (free, no key)
  4. GDELT API (historical 2015–2025, free, no key) — for initial crawl
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator

import requests
import trafilatura
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent))
from core import (
    console, load_config, load_processed, save_processed,
    save_article, ROOT
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-PA,es;q=0.9,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
}
REQUEST_DELAY = 1.5  # seconds between requests to be polite

# Domains/TLDs that are definitively NOT Panama — used to reject false positives
_NON_PA_TLDS = frozenset({
    ".my", ".com.my", ".gov.my",          # Malaysia
    ".com.au", ".gov.au", ".net.au",      # Australia
    ".co.uk", ".gov.uk", ".org.uk",       # UK
    ".com.sg", ".gov.sg",                  # Singapore
    ".co.nz",                              # New Zealand
    ".co.za", ".gov.za",                   # South Africa
    ".co.in", ".gov.in",                   # India
})

# At least one of these must appear in the article title or URL for RSS/GDELT.
# Only unambiguous geographic/national terms — no acronyms (MIDA matches Malaysia too).
_PANAMA_TERMS = frozenset({
    "panama", "panamá", "panameño", "panameña", "panameños", "panameñas",
    "chiriquí", "chiriqui", "veraguas", "azuero", "coclé", "cocle",
    "herrera", "colón", "colon", "bocas del toro", "darién", "darien",
    "istmo", "canal de panamá", "canal de panama",
})


def _url_domain(url: str) -> str:
    """Extract the hostname from a URL (e.g. 'www.thestar.com.my')."""
    try:
        return url.lower().split("/")[2]
    except IndexError:
        return ""


def _is_blocked_domain(url: str) -> bool:
    """True if the URL's domain ends with a known non-Panama TLD."""
    domain = _url_domain(url)
    return any(domain.endswith(tld) for tld in _NON_PA_TLDS)


def _is_panama_related(title: str, url: str = "") -> bool:
    """True if the title or URL contains at least one Panama-related term."""
    text = (title + " " + url).lower()
    return any(term in text for term in _PANAMA_TERMS)


def _get(url: str, timeout: int = 20, retries: int = 2, **kwargs) -> requests.Response | None:
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout, **kwargs)
            resp.raise_for_status()
            return resp
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code in (403, 429):
                if attempt < retries:
                    time.sleep(3 * (attempt + 1))
                    continue
                console.print(f"  [yellow]GET blocked (403/429): {url[:60]}[/yellow]")
                return None
            console.print(f"  [red]GET error {url[:60]}: {e}[/red]")
            return None
        except Exception as e:
            console.print(f"  [red]GET error {url[:60]}: {e}[/red]")
            return None
    return None


def extract_full_text(url: str) -> str | None:
    """Extract main article text from a URL using trafilatura."""
    try:
        resp = _get(url)
        if resp is None:
            return None
        return trafilatura.extract(
            resp.text,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
            favor_precision=True,
        )
    except Exception as e:
        console.print(f"  [yellow]Extract error: {e}[/yellow]")
        return None


def is_agro_relevant(title: str, text: str = "", config: dict = None) -> bool:
    """Return True if the content is relevant to Panama's agro sector."""
    if config is None:
        config = load_config()
    terms = (
        config.get("search_terms", {}).get("primary", [])
        + config.get("search_terms", {}).get("secondary", [])
    )
    combined = (title + " " + (text or "")).lower()
    return any(t.lower() in combined for t in terms)


# ─── 1. RSS FETCHER ──────────────────────────────────────────────────────────

_ATOM = "{http://www.w3.org/2005/Atom}"
_CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
_DC = "{http://purl.org/dc/elements/1.1/}"


def _parse_rss_xml(xml_bytes: bytes) -> list[dict]:
    """Parse RSS 2.0 or Atom feed from raw bytes. Returns list of entry dicts."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []

    entries = []

    # ── RSS 2.0 ──
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        pub_raw = item.findtext("pubDate") or item.findtext(f"{_DC}date") or ""
        pub_date = ""
        if pub_raw:
            try:
                pub_date = dateparser.parse(pub_raw).strftime("%Y-%m-%d")
            except Exception:
                pass
        desc = (
            item.findtext("description")
            or item.findtext(f"{_CONTENT}encoded")
            or ""
        )
        if desc and "<" in desc:
            desc = BeautifulSoup(desc, "lxml").get_text(" ", strip=True)
        entries.append({"title": title, "url": link, "date": pub_date, "summary": desc[:1000]})

    # ── Atom ──
    for entry in root.findall(f"{_ATOM}entry"):
        title = (entry.findtext(f"{_ATOM}title") or "").strip()
        link_el = entry.find(f"{_ATOM}link[@rel='alternate']") or entry.find(f"{_ATOM}link")
        link = (link_el.get("href", "") if link_el is not None else "").strip()
        if not title or not link:
            continue
        pub_raw = (
            entry.findtext(f"{_ATOM}updated")
            or entry.findtext(f"{_ATOM}published")
            or ""
        )
        pub_date = ""
        if pub_raw:
            try:
                pub_date = dateparser.parse(pub_raw).strftime("%Y-%m-%d")
            except Exception:
                pass
        summary = (
            entry.findtext(f"{_ATOM}summary")
            or entry.findtext(f"{_ATOM}content")
            or ""
        )
        if summary and "<" in summary:
            summary = BeautifulSoup(summary, "lxml").get_text(" ", strip=True)
        entries.append({"title": title, "url": link, "date": pub_date, "summary": summary[:1000]})

    return entries


def fetch_rss(source: dict, config: dict) -> Iterator[dict]:
    """Yield article dicts from an RSS feed source."""
    rss_url = source.get("rss")
    if not rss_url:
        return
    console.print(f"  RSS [cyan]{source['name']}[/cyan] → {rss_url[:60]}")
    resp = _get(rss_url)
    if resp is None:
        return
    entries = _parse_rss_xml(resp.content)
    console.print(f"    → {len(entries)} entradas en el feed")
    for entry in entries:
        url = entry.get("url", "")
        title = entry.get("title", "")
        if not url or not title:
            continue
        # Reject articles from blocked (non-Panama) domains
        if _is_blocked_domain(url):
            continue
        summary = entry.get("summary", "")
        if not is_agro_relevant(title, summary, config):
            continue
        # Require at least one Panama-related term in title or URL
        if not _is_panama_related(title, url):
            continue
        yield {
            "url": url,
            "title": title,
            "date": entry.get("date", ""),
            "source": source["name"],
            "trust_level": source.get("trust_level", 3),
            "language": source.get("language", "es"),
            "country": source.get("country", "PA"),
            "summary_raw": summary,
            "full_text": None,
        }
        time.sleep(0.1)


# ─── 2. DUCKDUCKGO WEB SEARCH ────────────────────────────────────────────────

def fetch_ddg_search(search_cfg: dict, config: dict) -> Iterator[dict]:
    """Yield articles from a DuckDuckGo news search (no API key needed)."""
    try:
        from ddgs import DDGS
    except ImportError:
        console.print("  [yellow]ddgs not installed (pip install ddgs), skipping web search[/yellow]")
        return

    site = search_cfg.get("site", "")
    query = search_cfg.get("query", "")
    max_results = search_cfg.get("max_results", 20)
    name = search_cfg.get("name", site)

    full_query = f"site:{site} {query}" if site else query
    console.print(f"  DDG [cyan]{name}[/cyan] → {full_query[:70]}")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(full_query, max_results=max_results))
    except Exception as e:
        if "403" in str(e) or "Ratelimit" in str(e):
            console.print(f"  [yellow]DDG rate limited — espera 30s...[/yellow]")
            time.sleep(30)
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.news(full_query, max_results=max_results))
            except Exception:
                console.print(f"  [yellow]DDG skip: {name}[/yellow]")
                return
        else:
            console.print(f"  [yellow]DDG error: {e}[/yellow]")
            return

    for r in results:
        url = r.get("url") or r.get("href", "")
        title = r.get("title", "")
        if not url or not title:
            continue
        date_raw = r.get("date") or r.get("published", "")
        pub_date = ""
        if date_raw:
            try:
                pub_date = dateparser.parse(str(date_raw)).strftime("%Y-%m-%d")
            except Exception:
                pass
        # Reject articles from blocked (non-Panama) domains
        if _is_blocked_domain(url):
            continue
        body = r.get("body") or r.get("excerpt", "")
        if not is_agro_relevant(title, body, config):
            continue
        # Require at least one Panama-related term in title or URL —
        # DDG's site: filter is not reliably honored by the backend, so
        # bare acronyms like "MIDA" can match homonym orgs abroad
        # (Malaysia's MITI/MIDA, Utah's Military Installation Development
        # Authority) even when a site: restriction was requested.
        if not _is_panama_related(title, url):
            continue
        yield {
            "url": url,
            "title": title,
            "date": pub_date,
            "source": site or name,
            "trust_level": 3,
            "language": "es",
            "country": "PA",
            "summary_raw": body[:1000],
            "full_text": None,
        }
    time.sleep(REQUEST_DELAY)


# ─── 3. WORLD BANK API ───────────────────────────────────────────────────────

def fetch_world_bank(source: dict, config: dict) -> Iterator[dict]:
    """Fetch Panama agriculture news from the World Bank API (free, no key)."""
    api_url = source.get("api_url")
    if not api_url:
        return
    params = source.get("api_params", {})
    params.setdefault("qterm", "panama agricultura")
    params.setdefault("lang_exact", "Spanish")
    params.setdefault("format", "json")
    params.setdefault("rows", 50)

    console.print(f"  WorldBank API [cyan]{source['name']}[/cyan]")
    resp = _get(api_url, params=params, timeout=30)
    if resp is None:
        return
    try:
        data = resp.json()
    except Exception:
        return

    for doc in data.get("documents", {}).values():
        if not isinstance(doc, dict):
            continue
        url = doc.get("url") or doc.get("pdfurl", "")
        title = doc.get("display_title") or doc.get("docdt", "")
        if not url or not title:
            continue
        date_raw = doc.get("docdt", "")
        pub_date = ""
        if date_raw:
            try:
                pub_date = dateparser.parse(date_raw).strftime("%Y-%m-%d")
            except Exception:
                pass
        abstract = doc.get("abstracts", "")
        if not is_agro_relevant(title, abstract, config):
            continue
        yield {
            "url": url,
            "title": title,
            "date": pub_date,
            "source": "BancoMundial",
            "trust_level": 2,
            "language": "es",
            "country": "INT",
            "summary_raw": abstract[:1000] if abstract else "",
            "full_text": None,
        }
    time.sleep(REQUEST_DELAY)


# ─── 4. GDELT (historical crawl) ─────────────────────────────────────────────

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def _gdelt_query_string(terms: list[str]) -> str:
    terms_part = " OR ".join(f'"{t}"' if " " in t else t for t in terms)
    # AND-require Panama mention to avoid false positives (e.g. "MIDA" matching Malaysia)
    return f"({terms_part}) (Panama OR Panamá OR panameño OR panameña OR Chiriquí OR Veraguas OR Azuero)"


def fetch_gdelt_batch(query: str, start_date: str, end_date: str, max_records: int = 250) -> list[dict] | None:
    """
    Fetch one GDELT window.
    Returns list of articles on success (may be empty), None on network/HTTP error.
    Only call mark-complete when result is not None.
    """
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
        return None  # network error — do NOT mark window as complete
    try:
        data = resp.json()
    except Exception:
        return None
    articles = []
    for item in data.get("articles", []):
        url = item.get("url", "")
        title = item.get("title", "")
        if not url or not title:
            continue

        # Reject URLs from known non-Panama domains
        if _is_blocked_domain(url):
            continue

        # Require at least one Panama term in title or URL
        if not _is_panama_related(title, url):
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
            "source": item.get("domain", "gdelt"),
            "trust_level": 3,
            "language": "es",
            "country": "PA",
            "summary_raw": "",
            "full_text": None,
            "gdelt": True,
        })
    return articles


def fetch_gdelt_historical(config: dict, processed: dict) -> Iterator[dict]:
    """
    Iterate GDELT over quarterly windows (2015–today).
    Skips windows already marked complete in processed["_gdelt_windows"].
    Never queries future dates — GDELT only indexes published articles.
    """
    cfg = config.get("gdelt", {})
    terms = config.get("search_terms", {}).get("primary", [])
    query = _gdelt_query_string(terms)

    completed_windows: set[str] = set(processed.get("_gdelt_windows", []))

    start = datetime.strptime(cfg.get("date_range", {}).get("start", "2015-01-01"), "%Y-%m-%d")
    # Never query beyond yesterday — GDELT doesn't have future articles
    config_end = datetime.strptime(cfg.get("date_range", {}).get("end", "2025-12-31"), "%Y-%m-%d")
    end = min(config_end, datetime.utcnow() - timedelta(days=1))

    current = start
    while current < end:
        next_q = min(current + timedelta(days=90), end)
        window_key = f"{current.strftime('%Y%m%d')}_{next_q.strftime('%Y%m%d')}"

        if window_key in completed_windows:
            console.print(f"  [dim]GDELT skip (ya descargado): {window_key}[/dim]")
            current = next_q + timedelta(days=1)
            continue

        console.print(
            f"  GDELT [cyan]{current.strftime('%Y-%m-%d')}[/cyan]"
            f" → [cyan]{next_q.strftime('%Y-%m-%d')}[/cyan]"
        )
        batch = fetch_gdelt_batch(query, current.strftime("%Y-%m-%d"), next_q.strftime("%Y-%m-%d"))

        if batch is None:
            # Network error — skip window WITHOUT marking complete so it's retried next run
            console.print(f"    [yellow]→ error de red, se reintentará en próxima ejecución[/yellow]")
            current = next_q + timedelta(days=1)
            time.sleep(REQUEST_DELAY * 3)  # longer pause after error before next window
            continue

        console.print(f"    → {len(batch)} artículos")
        for article in batch:
            yield article

        # Mark window as complete only on successful HTTP response (even if 0 results)
        completed_windows.add(window_key)
        processed["_gdelt_windows"] = list(completed_windows)

        current = next_q + timedelta(days=1)
        time.sleep(REQUEST_DELAY * 2)  # polite pause between GDELT windows


# ─── FULL TEXT ENRICHMENT ────────────────────────────────────────────────────

def enrich_with_fulltext(article: dict) -> dict:
    """Download full text for an article that doesn't have it yet."""
    if article.get("full_text"):
        return article
    article["full_text"] = extract_full_text(article["url"])
    time.sleep(REQUEST_DELAY)
    return article


# ─── MAIN FETCH COMMAND ──────────────────────────────────────────────────────

def run_fetch(
    mode: str = "daily",
    limit: int = 0,
    extract_text: bool = False,
    skip_duplicates: bool = True,
) -> int:
    """
    Main fetch entry point.

    mode:
      'daily'    — RSS feeds + DDG web searches (fast, for scheduled runs)
      'rss'      — RSS feeds only
      'web'      — DuckDuckGo searches only
      'gdelt'    — GDELT historical crawl (2015–2025, for initial setup)
      'worldbank'— World Bank API
      'all'      — everything

    Returns number of new articles saved.
    """
    config = load_config()
    processed = load_processed()
    saved = 0

    def _save(art: dict) -> bool:
        nonlocal saved
        url = art.get("url", "")
        if not url:
            return False
        if skip_duplicates and url in processed:
            return False
        if extract_text and not art.get("full_text"):
            art = enrich_with_fulltext(art)
        # Need at least title + (text or summary)
        if not art.get("full_text") and not art.get("summary_raw"):
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
            f"  [green]✓[/green] [{saved}] {art.get('title', '')[:72]}"
        )
        return True

    def _check_limit() -> bool:
        return bool(limit) and saved >= limit

    # Collect all sources
    all_sources: list[dict] = []
    for group in config.get("sources", {}).values():
        all_sources.extend(group)

    # ── RSS ──────────────────────────────────────────────────────────────────
    if mode in ("daily", "rss", "all"):
        console.print("\n[bold]── RSS Feeds ──[/bold]")
        for src in all_sources:
            if not src.get("rss"):
                continue
            for art in fetch_rss(src, config):
                _save(art)
                if _check_limit():
                    break
            if _check_limit():
                break

    # ── DuckDuckGo Web Search ─────────────────────────────────────────────
    if mode in ("daily", "web", "all"):
        console.print("\n[bold]── Búsqueda Web (DDG) ──[/bold]")
        for search_cfg in config.get("web_searches", []):
            for art in fetch_ddg_search(search_cfg, config):
                _save(art)
                if _check_limit():
                    break
            if _check_limit():
                break

    # ── World Bank API ────────────────────────────────────────────────────
    if mode in ("worldbank", "all"):
        console.print("\n[bold]── World Bank API ──[/bold]")
        for src in all_sources:
            if src.get("name") == "BancoMundial":
                for art in fetch_world_bank(src, config):
                    _save(art)
                    if _check_limit():
                        break

    # ── GDELT Historical ──────────────────────────────────────────────────
    if mode in ("gdelt", "all"):
        console.print("\n[bold]── GDELT Histórico 2015–2025 ──[/bold]")
        for art in fetch_gdelt_historical(config, processed):
            _save(art)
            # Save progress every 50 GDELT articles (windows are marked in processed)
            if saved % 50 == 0 and saved > 0:
                save_processed(processed)
            if _check_limit():
                break

    save_processed(processed)
    console.print(f"\n[bold green]Total guardados: {saved} artículos nuevos[/bold green]")
    return saved


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    run_fetch(mode=mode, limit=limit)
