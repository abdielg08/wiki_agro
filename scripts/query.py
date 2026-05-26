"""
Query the wiki using natural language.
Valuable answers are saved back into the wiki (knowledge compounds).
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

sys.path.insert(0, str(Path(__file__).parent))
from core import (
    console, read_wiki_page, write_wiki_page, append_log,
    load_wiki_index, list_wiki_pages, WIKI_DIR, ROOT
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


def find_relevant_pages(question: str) -> list[tuple[str, str]]:
    """Return list of (rel_path, content) for pages relevant to the question."""
    keywords = question.lower().split()
    stop_words = {"de", "la", "el", "en", "y", "a", "que", "es", "los", "las", "un", "una"}
    keywords = [k for k in keywords if k not in stop_words and len(k) > 3]

    scored = []
    for page_path in list_wiki_pages():
        if page_path.name in ("log.md",):
            continue
        content = page_path.read_text(encoding="utf-8")
        content_lower = content.lower()
        score = sum(1 for kw in keywords if kw in content_lower)
        if score > 0:
            rel = str(page_path.relative_to(WIKI_DIR))
            scored.append((score, rel, content))

    scored.sort(key=lambda x: -x[0])
    return [(rel, content) for _, rel, content in scored[:8]]


QUERY_SYSTEM = """\
Eres el asistente del Wiki Agropecuario de Panamá. Respondes preguntas sobre \
el sector agropecuario panameño basándote ÚNICAMENTE en el wiki disponible.

Schema del wiki:
{claude_md}

Índice del wiki:
{index}

Páginas relevantes del wiki:
{pages}

INSTRUCCIONES:
- Responde en español, con citas explícitas a las páginas del wiki
- Si la información no está en el wiki, dilo claramente
- Formato: respuesta en markdown con citas [página.md]
- Al final, incluye un JSON en bloque de código con:
  {{
    "save_to_wiki": true/false,
    "suggested_path": "topics/slug.md o null",
    "suggested_title": "Título si save_to_wiki es true"
  }}
"""

QUERY_USER = "Pregunta: {question}"


def run_query(question: str, save_answers: bool = True) -> str:
    """Answer a question using the wiki. Optionally save the answer back."""
    client = get_client()
    claude_md = load_claude_md()
    index = load_wiki_index()
    relevant = find_relevant_pages(question)

    pages_text = ""
    for rel_path, content in relevant:
        pages_text += f"\n### wiki/{rel_path}\n{content[:2000]}\n"

    system = QUERY_SYSTEM.format(
        claude_md=claude_md[:2000],
        index=index[:2000],
        pages=pages_text[:6000],
    )

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
        messages=[{"role": "user", "content": QUERY_USER.format(question=question)}],
    )

    answer = response.content[0].text

    # Extract save metadata
    save_meta = {"save_to_wiki": False, "suggested_path": None}
    if "```json" in answer:
        try:
            json_block = answer.split("```json")[1].split("```")[0].strip()
            save_meta = json.loads(json_block)
        except Exception:
            pass

    # Display answer (strip the JSON block for display)
    display_answer = answer
    if "```json" in display_answer:
        display_answer = display_answer.split("```json")[0].strip()

    console.print(Panel(Markdown(display_answer), title="[bold]Respuesta[/bold]", border_style="green"))

    # Save valuable answers back to wiki
    if save_answers and save_meta.get("save_to_wiki") and save_meta.get("suggested_path"):
        path = save_meta["suggested_path"]
        title = save_meta.get("suggested_title", question[:60])
        today = datetime.now().strftime("%Y-%m-%d")
        page_content = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"type: query_answer\n"
            f"tags: [query, auto-generado]\n"
            f"last_updated: {today}\n"
            f"question: \"{question}\"\n"
            f"---\n\n"
            f"# {title}\n\n"
            f"> Pregunta original: *{question}*\n\n"
            f"{display_answer}\n"
        )
        write_wiki_page(path, page_content)
        append_log(
            f"QUERY: '{question[:60]}'\n"
            f"  Respuesta guardada en: wiki/{path}"
        )
        console.print(f"\n[dim]Respuesta guardada en wiki/{path}[/dim]")

    return display_answer


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "¿Cuáles son los principales retos del sector agropecuario panameño?"
    run_query(q)
