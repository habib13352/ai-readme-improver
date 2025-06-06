from __future__ import annotations

import os
import yaml
from jinja2 import Environment, FileSystemLoader

from openai_helper import ask_openai


def load_config(path: str = "config.yaml") -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_prompt(readme_text: str, config: dict) -> str:
    logo_block = ""
    if config.get("logo_path"):
        logo_block = f"![Logo]({config['logo_path']})"

    contact_section = ""
    if config.get("email"):
        contact_section = f"## Contact\n- Email: {config['email']}"

    extra_sections_md = ""
    for section in config.get("extra_sections", []):
        extra_sections_md += f"## {section['title']}\n{section['content']}\n\n"

    return f"""
You are ChatGPT. Improve the project's README.md with these rules:
1. Insert logo (if provided) at the very top:
   {logo_block}
2. Include any extra sections specified in the config:
   {extra_sections_md}
3. Ensure a “Contact” section with the email is at the bottom:
   {contact_section}
4. Provide a short TL;DR summary and bullet-point suggestions, then output the fully-rewritten README.md.

Here is the current README.md:
{readme_text}
"""


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


def generate_summary(readme_text: str, model: str = "gpt-3.5-turbo", prompt_prefix: str | None = None) -> str:
    prompt = (prompt_prefix or DEFAULT_SUMMARY_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.3, max_tokens=200)


def suggest_improvements(readme_text: str, model: str = "gpt-3.5-turbo", prompt_prefix: str | None = None) -> str:
    prompt = (prompt_prefix or DEFAULT_SUGGEST_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.5, max_tokens=400)


def rewrite_readme(
    readme_text: str,
    model: str = "gpt-3.5-turbo",
    prompt_prefix: str | None = None,
    config: dict | None = None,
) -> str:
    if config:
        prompt = build_prompt(readme_text, config)
    else:
        prompt = (prompt_prefix or DEFAULT_REWRITE_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.7, max_tokens=1920)
