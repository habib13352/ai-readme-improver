"""High level helpers to talk to the OpenAI API for README updates."""

from __future__ import annotations

import os
from typing import Any
from pathlib import Path
import yaml

from .openai_helper import ask_openai

# Fallback rewrite ordering (used only if no sections list is found)
README_ORDER_MESSAGE = (
    "Structure the README exactly in this order, using these section headings "
    "(with Markdown H2):\n\n"
    "Title & Logo\n\n"
    "Badges\n\n"
    "Table of Contents\n\n"
    "Demo\n\n"
    "Installation\n\n"
    "Usage\n\n"
    "Contributing\n\n"
    "License\n\n"
    "Maintainers\n\n"
    "Acknowledgements\n\n"
    "Contact"
)


def load_config(path: str = "config.yaml") -> dict[str, Any]:
    """Load configuration values from a YAML file."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_repo_layout() -> str:
    """Scan key directories and return a markdown list of code files."""
    files: list[str] = []
    for pattern in ("readme_improver/**/*.py", "scripts/**/*.py"):
        files.extend(sorted(str(p) for p in Path().glob(pattern)))

    if not files:
        return ""

    lines = ["Here’s the repository layout:"]
    for path in files:
        lines.append(f"- `{path}`")
    return "\n".join(lines)


DEFAULT_SUMMARY_PROMPT = (
    "You are an AI assistant that reads README files. "
    "Provide a concise TL;DR summary of the following README (2–3 lines):\n\n"
)

DEFAULT_SUGGEST_PROMPT = (
    "You are an expert technical writer. "
    "Suggest specific improvements for this README. "
    "Mention missing sections (Installation, Usage, License, etc.), "
    "clarity of language, badge additions, and SEO keywords. "
    "Output as bullet points:\n\n"
)

DEFAULT_REWRITE_PROMPT = (
    "You are an AI that rewrites project README files to be more professional, "
    "clear, and complete. "
    "Rewrite the following README, ensuring it includes these sections: "
    "Title, Short Description, Installation, Usage, License, Contributing, Contact. "
    "Use Markdown formatting:\n\n"
)


def generate_summary(
    readme_text: str,
    model: str = "gpt-3.5-turbo",
    prompt_prefix: str | None = None,
) -> str:
    prompt = (prompt_prefix or DEFAULT_SUMMARY_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.3, max_tokens=200)


def suggest_improvements(
    readme_text: str,
    model: str = "gpt-3.5-turbo",
    prompt_prefix: str | None = None,
) -> str:
    prompt = (prompt_prefix or DEFAULT_SUGGEST_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.5, max_tokens=400)


def rewrite_readme(
    readme_text: str,
    model: str = "gpt-3.5-turbo",
    prompt_prefix: str | None = None,
    config: dict | None = None,
) -> str:
    """Rewrite the README using per-section prompt files, injecting repo context."""

    if config and config.get("sections"):
        output_md: list[str] = []

        # Title & Logo
        if project := config.get("project_name"):
            output_md.append(f"# {project}")
        if logo := config.get("logo_path"):
            output_md.append(f"![Logo]({logo})")

        # Badges
        if config.get("badges"):
            badges = [
                f"[![{b['name']}]({b['image_url']})]({b['link']})"
                for b in config["badges"]
            ]
            output_md.append(" ".join(badges))

        # Per-section generation
        repo_layout = generate_repo_layout()
        for sec in config["sections"]:
            if not sec.get("enabled"):
                continue

            name = sec["name"].lower()
            # Maintainers override (direct from config)
            if name == "maintainers" and config.get("maintainers"):
                lines = [f"- {m['name']} ({m['handle']})" for m in config["maintainers"]]
                output_md.append("## Maintainers\n" + "\n".join(lines))
                continue

            # Contact override (direct from config)
            if name == "contact" and (email := config.get("email")):
                output_md.append(f"## Contact\n- Email: {email}")
                continue

            # Load the prompt file
            pf = sec.get("prompt_file")
            if pf and Path(pf).exists():
                prompt_text = Path(pf).read_text(encoding="utf-8")
                # Inject repo layout context
                if repo_layout:
                    prompt_text = repo_layout + "\n\n" + prompt_text
                section_md = ask_openai(
                    prompt_text, model=model, temperature=0.7, max_tokens=1024
                ).strip()
                output_md.append(section_md)

        return "\n\n".join(output_md)

    # Fallback: single-shot rewrite
    prompt_body = (prompt_prefix or DEFAULT_REWRITE_PROMPT) + readme_text
    full_prompt = f"{README_ORDER_MESSAGE}\n\n{prompt_body}"
    return ask_openai(
        full_prompt, model=model, temperature=0.7, max_tokens=1920
    )
