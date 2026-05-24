"""Shared utilities for the wiki_agro system."""

import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from rich.console import Console

console = Console()

ROOT = Path(__file__).parent.parent
SOURCES_DIR = ROOT / "sources" / "articles"
PROCESSED_FILE = ROOT / "sources" / "processed.json"
WIKI_DIR = ROOT / "wiki"
CONFIG_DIR = ROOT / "config"


def load_config() -> dict:
    with open(CONFIG_DIR / "sources.yaml") as f:
        return yaml.safe_load(f)


def load_processed() -> dict:
    """Return dict of url -> metadata for processed articles."""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE) as f:
            return json.load(f)
    return {}


def save_processed(processed: dict) -> None:
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_FILE, "w") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)


def url_to_slug(url: str, date: str = "", source: str = "") -> str:
    """Convert URL to a filesystem-safe slug."""
    clean = re.sub(r"https?://[^/]+", "", url)
    clean = re.sub(r"[^\w\s-]", " ", clean)
    clean = re.sub(r"\s+", "-", clean.strip())
    clean = clean[:60].strip("-").lower()
    prefix = date.replace("-", "")[:8] if date else datetime.now().strftime("%Y%m%d")
    src = re.sub(r"[^\w]", "", source.lower())[:10] if source else "unknown"
    return f"{prefix}_{src}_{clean}"


def save_article(article: dict) -> Path:
    """Save a raw article to sources/articles/. Returns path."""
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    slug = url_to_slug(article.get("url", ""), article.get("date", ""), article.get("source", ""))
    path = SOURCES_DIR / f"{slug}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    return path


def load_article(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_wiki_page(rel_path: str) -> Optional[str]:
    """Read a wiki page by relative path (e.g. 'topics/arroz.md')."""
    path = WIKI_DIR / rel_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


def write_wiki_page(rel_path: str, content: str) -> Path:
    """Write or overwrite a wiki page."""
    path = WIKI_DIR / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def append_log(entry: str) -> None:
    """Append a timestamped entry to wiki/log.md."""
    log_path = WIKI_DIR / "log.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"\n## {timestamp}\n{entry.strip()}\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line)


def list_wiki_pages() -> list[Path]:
    """Return all markdown files in the wiki directory."""
    return list(WIKI_DIR.rglob("*.md"))


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                body = parts[2].lstrip("\n")
                return fm, body
            except yaml.YAMLError:
                pass
    return {}, content


def build_frontmatter(meta: dict) -> str:
    """Render a dict as YAML frontmatter block."""
    return "---\n" + yaml.dump(meta, allow_unicode=True, default_flow_style=False) + "---\n\n"


def content_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:8]


def load_wiki_index() -> str:
    idx = WIKI_DIR / "index.md"
    if idx.exists():
        return idx.read_text(encoding="utf-8")
    return ""
