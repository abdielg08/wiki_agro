"""
Fetcher histórico masivo — 15 años de noticias agropecuarias de Panamá (2010–2025)

Estrategias por fuente:
  1. GDELT DocSearch API  — indexa prensa mundial, gratis, 2011–2025
  2. Wayback Machine CDX  — archivo de internet, URLs históricas por dominio
  3. Sitemaps WordPress   — La Prensa, TVN, etc. (sitemap_index.xml)
  4. FAO Document Search  — documentos y noticias FAO con filtro de país
  5. World Bank API       — proyectos y noticias BM con filtro de año

Uso:
  python scripts/fetch_historical.py --years 2010-2025 --mode all
  python scripts/fetch_historical.py --years 2010-2015 --mode gdelt
  python scripts/fetch_historical.py --domain prensa.com --mode cdx --years 2015-2020
"""

import json
import sys
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator
import xml.etree.ElementTree as ET
from urllib.parse import urlencode, quote_plus

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

sys.path.insert(0, str(Path(__file__).parent))
from core import (
    console, load_config, load_processed, save_processed,
    save_article, ROOT
)
from fetch_news import _get, HEADERS, REQUEST_DELAY, is_agro_relevant

PROGRESS_FILE = ROOT / "sources" / "historical_progress.json"


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"gdelt_windows": [], "cdx_domains": {}, "sitemaps": {}, "fao_years": [], "wb_pages": []}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def year_range(start_year: int, end_year: int) -> list[int]:
    return list(range(start_year, end_year + 1))


# ─── 1. GDELT — hasta 250 artículos por ventana trimestral ──────────────────

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

_AGRO_QUERY = (
    "agropecuario OR agricultura OR ganaderia OR MIDA OR IDIAP OR cosecha "
    "OR cultivo OR arroz OR maiz OR platano OR ganadero"
)


def fetch_gdelt_window(start: str, end: str, query: str = _AGRO_QUERY) -> list[dict] | None:
    """Fetch one quarterly window from GDELT. Returns None on network error."""
    params = {
        "query": f"({query}) sourcecountry:PA",
        "mode": "artlist",
        "maxrecords": 250,
        "format": "json",
        "sourcelang": "spa",
        "startdatetime": start.replace("-", "") + "000000",
        "enddatetime": end.replace("-", "") + "235959",
        "sort": "DateDesc",
    }
    resp = _get(GDELT_URL, params=params, timeout=30)
    if resp is None:
        return None
    try:
        data = resp.json()
    except Exception:
        return None
    results = []
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
        results.append({
            "url": url, "title": title, "date": date,
            "source": item.get("domain", "gdelt"),
            "trust_level": 3, "language": "es", "country": "PA",
            "summary_raw": "", "full_text": None, "method": "gdelt",
        })
    return results


def fetch_gdelt_years(start_year: int, end_year: int, progress: dict, processed: dict) -> Iterator[dict]:
    """Iterate GDELT quarterly windows for a year range, skipping completed ones."""
    done = set(progress.get("gdelt_windows", []))
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    current = start
    while current <= end:
        next_q = min(current + timedelta(days=90), end)
        key = f"{current.strftime('%Y%m%d')}_{next_q.strftime('%Y%m%d')}"
        if key in done:
            current = next_q + timedelta(days=1)
            continue
        console.print(f"  GDELT [cyan]{current.strftime('%Y-%m-%d')}[/cyan] → [cyan]{next_q.strftime('%Y-%m-%d')}[/cyan]")
        batch = fetch_gdelt_window(current.strftime("%Y-%m-%d"), next_q.strftime("%Y-%m-%d"))
        if batch is None:
            console.print(f"    [yellow]→ error de red, se reintentará[/yellow]")
        else:
            console.print(f"    → {len(batch)} artículos")
            for art in batch:
                if art["url"] not in processed:
                    yield art
            done.add(key)
            progress["gdelt_windows"] = list(done)
            save_progress(progress)
        current = next_q + timedelta(days=1)
        time.sleep(REQUEST_DELAY)


# ─── 2. WAYBACK MACHINE CDX API — archivo de internet por dominio ───────────

CDX_URL = "https://web.archive.org/cdx/search/cdx"


def fetch_cdx_domain(
    domain: str,
    start_year: int,
    end_year: int,
    progress: dict,
    processed: dict,
    config: dict,
) -> Iterator[dict]:
    """
    Search the Wayback Machine CDX index for archived URLs from a domain.
    Returns article metadata; full text must be downloaded separately.
    """
    domain_key = f"{domain}_{start_year}_{end_year}"
    done_pages = set(progress.get("cdx_domains", {}).get(domain_key, []))

    params = {
        "url": f"{domain}/*",
        "output": "json",
        "limit": 500,
        "from": f"{start_year}0101",
        "to": f"{end_year}1231",
        "filter": "statuscode:200",
        "matchType": "prefix",
        "collapse": "urlkey",   # deduplicate same URL
        "fl": "original,timestamp,statuscode",
    }

    console.print(f"  CDX [cyan]{domain}[/cyan] ({start_year}–{end_year})")
    resp = _get(CDX_URL, params=params, timeout=60)
    if resp is None:
        return
    try:
        rows = resp.json()
    except Exception:
        return

    if not rows or len(rows) < 2:
        return

    headers = rows[0]  # first row is field names
    url_idx = headers.index("original") if "original" in headers else 0
    ts_idx = headers.index("timestamp") if "timestamp" in headers else 1

    count = 0
    for row in rows[1:]:
        if len(row) <= max(url_idx, ts_idx):
            continue
        url = row[url_idx]
        ts = row[ts_idx]
        # Filter likely article URLs (not category/tag pages)
        if not re.search(r"/\d{4}/\d{2}/|/articulo|/noticia|/noticias/", url):
            continue
        if url in processed:
            continue
        # Parse date from CDX timestamp (YYYYMMDDHHMMSS)
        try:
            date = datetime.strptime(ts[:8], "%Y%m%d").strftime("%Y-%m-%d")
        except Exception:
            date = ""
        # Use a heuristic title from URL slug
        slug = url.rstrip("/").split("/")[-1]
        title = slug.replace("-", " ").replace("_", " ")[:100]
        if not is_agro_relevant(title, "", config):
            continue
        yield {
            "url": url, "title": title, "date": date,
            "source": domain, "trust_level": 3, "language": "es",
            "country": "PA", "summary_raw": "", "full_text": None,
            "method": "cdx_wayback",
        }
        count += 1
        time.sleep(0.05)

    if domain_key not in progress["cdx_domains"]:
        progress["cdx_domains"][domain_key] = []
    progress["cdx_domains"][domain_key].append(domain_key)
    save_progress(progress)
    console.print(f"    → {count} URLs archivadas relevantes")


# ─── 3. SITEMAPS WORDPRESS — índice completo de artículos ───────────────────

def _parse_sitemap_index(xml_bytes: bytes) -> list[str]:
    """Extract sitemap URLs from sitemap_index.xml."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text for loc in root.findall(".//sm:loc", ns) if loc.text]


def _parse_sitemap(xml_bytes: bytes) -> list[dict]:
    """Extract article URLs and dates from a sitemap XML."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    entries = []
    for url_el in root.findall("sm:url", ns):
        loc = url_el.findtext("sm:loc", "", ns)
        lastmod = url_el.findtext("sm:lastmod", "", ns)
        if loc:
            entries.append({"url": loc, "lastmod": lastmod})
    return entries


def _year_from_url_or_date(url: str, lastmod: str) -> int | None:
    """Extract publication year from URL path or lastmod date."""
    m = re.search(r"/(\d{4})/\d{2}/", url)
    if m:
        return int(m.group(1))
    if lastmod:
        try:
            return dateparser.parse(lastmod).year
        except Exception:
            pass
    return None


def fetch_sitemap_domain(
    domain: str,
    start_year: int,
    end_year: int,
    progress: dict,
    processed: dict,
    config: dict,
) -> Iterator[dict]:
    """Scrape all article URLs from a WordPress sitemap for a year range."""
    domain_key = f"sitemap_{domain}_{start_year}_{end_year}"
    if domain_key in progress.get("sitemaps", {}):
        console.print(f"  [dim]Sitemap skip (ya procesado): {domain}[/dim]")
        return

    base = f"https://{domain}"
    console.print(f"  Sitemap [cyan]{domain}[/cyan] ({start_year}–{end_year})")

    # Try sitemap_index.xml first
    index_resp = _get(f"{base}/sitemap_index.xml")
    if index_resp is None:
        index_resp = _get(f"{base}/sitemap.xml")
    if index_resp is None:
        console.print(f"    [yellow]→ sin sitemap disponible[/yellow]")
        return

    child_sitemaps = _parse_sitemap_index(index_resp.content)
    if not child_sitemaps:
        # It might be a direct sitemap, not an index
        child_sitemaps = [f"{base}/sitemap.xml"]

    # Filter sitemaps by year range (many sites name them post-sitemap-2020.xml)
    filtered = []
    for sm_url in child_sitemaps:
        year_m = re.search(r"(\d{4})", sm_url)
        if year_m:
            y = int(year_m.group(1))
            if start_year <= y <= end_year:
                filtered.append(sm_url)
        else:
            filtered.append(sm_url)  # include if no year in name

    console.print(f"    → {len(filtered)} sitemaps a escanear")
    count = 0
    for sm_url in filtered:
        resp = _get(sm_url)
        if resp is None:
            continue
        for entry in _parse_sitemap(resp.content):
            url = entry["url"]
            year = _year_from_url_or_date(url, entry.get("lastmod", ""))
            if year and not (start_year <= year <= end_year):
                continue
            if url in processed:
                continue
            slug = url.rstrip("/").split("/")[-1]
            title = slug.replace("-", " ").replace("_", " ")[:100]
            if not is_agro_relevant(title, "", config):
                continue
            date = ""
            if entry.get("lastmod"):
                try:
                    date = dateparser.parse(entry["lastmod"]).strftime("%Y-%m-%d")
                except Exception:
                    pass
            yield {
                "url": url, "title": title, "date": date,
                "source": domain, "trust_level": 3, "language": "es",
                "country": "PA", "summary_raw": "", "full_text": None,
                "method": "sitemap",
            }
            count += 1
        time.sleep(REQUEST_DELAY)

    progress.setdefault("sitemaps", {})[domain_key] = True
    save_progress(progress)
    console.print(f"    → {count} artículos relevantes encontrados")


# ─── 4. FAO DOCUMENT SEARCH — documentos y reportes FAO sobre Panamá ────────

FAO_SEARCH = "https://openknowledge.fao.org/rest/search"


def fetch_fao_docs(start_year: int, end_year: int, progress: dict, processed: dict) -> Iterator[dict]:
    """Search FAO OpenKnowledge repository for Panama agricultural documents."""
    fao_key = f"fao_{start_year}_{end_year}"
    if fao_key in progress.get("fao_years", []):
        console.print(f"  [dim]FAO skip (ya procesado): {start_year}–{end_year}[/dim]")
        return

    console.print(f"  FAO OpenKnowledge [cyan]{start_year}–{end_year}[/cyan]")
    page = 0
    page_size = 50
    total_found = 0

    while True:
        params = {
            "query": "panama agricultura agropecuario",
            "scope": "/",
            "rpp": page_size,
            "start": page * page_size,
            "sort_by": "dc.date.issued_dt",
            "order": "desc",
            "facet": "true",
        }
        resp = _get(FAO_SEARCH, params=params, timeout=30)
        if resp is None:
            break
        try:
            data = resp.json()
        except Exception:
            break

        items = data.get("results", [])
        if not items:
            break

        for item in items:
            # Filter by date
            date_raw = item.get("dc.date.issued", [""])[0] if item.get("dc.date.issued") else ""
            try:
                year = int(str(date_raw)[:4])
                if not (start_year <= year <= end_year):
                    continue
                date = f"{year}-01-01"
            except Exception:
                continue

            url = item.get("link", "")
            if not url:
                handles = item.get("dc.identifier.uri", [])
                url = handles[0] if handles else ""
            if not url or url in processed:
                continue

            titles = item.get("dc.title", [])
            title = titles[0] if titles else ""
            if not title:
                continue

            abstracts = item.get("dc.description.abstract", [])
            abstract = abstracts[0][:500] if abstracts else ""

            yield {
                "url": url, "title": title, "date": date,
                "source": "FAO", "trust_level": 2, "language": "es",
                "country": "INT", "summary_raw": abstract, "full_text": None,
                "method": "fao_api",
            }
            total_found += 1

        if len(items) < page_size:
            break
        page += 1
        time.sleep(REQUEST_DELAY)

    progress.setdefault("fao_years", []).append(fao_key)
    save_progress(progress)
    console.print(f"    → {total_found} documentos FAO")


# ─── 5. WORLD BANK API — proyectos y reportes BM por año ────────────────────

WB_SEARCH = "https://search.worldbank.org/api/v2/projects"


def fetch_worldbank_years(start_year: int, end_year: int, progress: dict, processed: dict) -> Iterator[dict]:
    """Fetch World Bank projects in Panama related to agriculture by year range."""
    wb_key = f"wb_{start_year}_{end_year}"
    if wb_key in progress.get("wb_pages", []):
        console.print(f"  [dim]WorldBank skip: {start_year}–{end_year}[/dim]")
        return

    console.print(f"  WorldBank [cyan]{start_year}–{end_year}[/cyan]")
    params = {
        "qterm": "panama agriculture food",
        "countryshortname_exact": "Panama",
        "os": 0,
        "rows": 100,
        "format": "json",
    }
    resp = _get(WB_SEARCH, params=params, timeout=30)
    if resp is None:
        return
    try:
        data = resp.json()
    except Exception:
        return

    count = 0
    for proj in data.get("projects", {}).values() if isinstance(data.get("projects"), dict) else []:
        if not isinstance(proj, dict):
            continue
        date_raw = proj.get("boardapprovaldate", "") or proj.get("closingdate", "")
        try:
            year = int(str(date_raw)[:4])
            if not (start_year <= year <= end_year):
                continue
            date = dateparser.parse(date_raw).strftime("%Y-%m-%d")
        except Exception:
            continue

        url = proj.get("url", "") or f"https://projects.worldbank.org/en/projects-operations/project-detail/{proj.get('id','')}"
        title = proj.get("project_name", "")
        if not url or not title or url in processed:
            continue
        abstract = proj.get("project_abstract", {})
        if isinstance(abstract, dict):
            abstract = abstract.get("cdata", "")
        yield {
            "url": url, "title": title, "date": date,
            "source": "BancoMundial", "trust_level": 2, "language": "es",
            "country": "INT", "summary_raw": str(abstract)[:500],
            "full_text": None, "method": "worldbank_api",
        }
        count += 1

    progress.setdefault("wb_pages", []).append(wb_key)
    save_progress(progress)
    console.print(f"    → {count} proyectos BM")


# ─── MAIN ────────────────────────────────────────────────────────────────────

SITEMAP_SOURCES = [
    "www.prensa.com",
    "www.panamaamerica.com.pa",
    "www.tvn-2.com",
    "www.laestrella.com.pa",
    "elcapitalfinanciero.com",
]

CDX_SOURCES = [
    "www.prensa.com",
    "www.mida.gob.pa",
    "www.idiap.gob.pa",
    "www.tvn-2.com",
    "www.laestrella.com.pa",
]


def run_historical_fetch(
    start_year: int = 2010,
    end_year: int = 2025,
    mode: str = "all",
    domain: str | None = None,
    limit: int = 0,
) -> int:
    """
    Main historical fetch. Returns number of articles saved.

    mode: gdelt | cdx | sitemap | fao | worldbank | all
    domain: restrict CDX/sitemap to a specific domain
    limit: max articles to save (0 = unlimited)
    """
    config = load_config()
    processed = load_processed()
    progress = load_progress()
    saved = 0

    def _save(art: dict) -> bool:
        nonlocal saved
        url = art.get("url", "")
        if not url or url in processed:
            return False
        path = save_article(art)
        processed[url] = {
            "saved_at": datetime.now().isoformat(),
            "path": str(path),
            "title": art.get("title", ""),
            "date": art.get("date", ""),
            "source": art.get("source", ""),
            "method": art.get("method", ""),
            "ingested": False,
        }
        saved += 1
        if saved % 25 == 0:
            save_processed(processed)
        console.print(f"  [green]✓[/green] [{saved}] {art.get('title','')[:70]}")
        return True

    def _check_limit() -> bool:
        return bool(limit) and saved >= limit

    if mode in ("gdelt", "all"):
        console.print(f"\n[bold]── GDELT {start_year}–{end_year} ──[/bold]")
        for art in fetch_gdelt_years(start_year, end_year, progress, processed):
            _save(art)
            if _check_limit():
                break

    if mode in ("fao", "all") and not _check_limit():
        console.print(f"\n[bold]── FAO Documents {start_year}–{end_year} ──[/bold]")
        for art in fetch_fao_docs(start_year, end_year, progress, processed):
            _save(art)
            if _check_limit():
                break

    if mode in ("worldbank", "all") and not _check_limit():
        console.print(f"\n[bold]── World Bank {start_year}–{end_year} ──[/bold]")
        for art in fetch_worldbank_years(start_year, end_year, progress, processed):
            _save(art)
            if _check_limit():
                break

    cdx_domains = [domain] if domain else CDX_SOURCES
    if mode in ("cdx", "all") and not _check_limit():
        console.print(f"\n[bold]── Wayback Machine CDX {start_year}–{end_year} ──[/bold]")
        for dom in cdx_domains:
            for art in fetch_cdx_domain(dom, start_year, end_year, progress, processed, config):
                _save(art)
                if _check_limit():
                    break
            if _check_limit():
                break

    sitemap_domains = [domain] if domain else SITEMAP_SOURCES
    if mode in ("sitemap", "all") and not _check_limit():
        console.print(f"\n[bold]── Sitemaps {start_year}–{end_year} ──[/bold]")
        for dom in sitemap_domains:
            for art in fetch_sitemap_domain(dom, start_year, end_year, progress, processed, config):
                _save(art)
                if _check_limit():
                    break
            if _check_limit():
                break

    save_processed(processed)
    console.print(f"\n[bold green]Total guardados: {saved} artículos[/bold green]")
    return saved


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Fetch histórico masivo de noticias agropecuarias")
    p.add_argument("--years", default="2010-2025", help="Rango de años, e.g. 2010-2025")
    p.add_argument("--mode", default="all",
                   choices=["all", "gdelt", "cdx", "sitemap", "fao", "worldbank"])
    p.add_argument("--domain", default=None, help="Restringir CDX/sitemap a un dominio")
    p.add_argument("--limit", type=int, default=0, help="Máximo artículos (0=sin límite)")
    args = p.parse_args()
    start_y, end_y = (int(y) for y in args.years.split("-"))
    run_historical_fetch(start_y, end_y, mode=args.mode, domain=args.domain, limit=args.limit)
