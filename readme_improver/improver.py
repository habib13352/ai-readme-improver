"""High level helpers to talk to the OpenAI API for README updates."""

from __future__ import annotations

import os
from typing import Any

import yaml

from .openai_helper import ask_openai
from .logger import get_logger

logger = get_logger()


def load_config(path: str = "config.yaml") -> dict[str, Any]:
    """Load configuration values from a YAML file.

    Args:
        path: Path to the configuration file.

    Returns:
        Parsed configuration as a dictionary. If the file does not exist,
        an empty dictionary is returned.
    """

    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_config(cfg: dict[str, Any]) -> bool:
    """Validate configuration values.

    The current implementation requires ``project_name``, ``email`` and
    ``logo_path`` to be present.  It also verifies referenced files exist
    and that badge/section entries contain the expected keys.

    Args:
        cfg: Parsed configuration dictionary.

    Returns:
        ``True`` if the configuration is valid, ``False`` otherwise.
    """

    ok = True
    required = ["project_name", "email", "logo_path"]
    for field in required:
        if not cfg.get(field):
            logger.error("Missing required config value: %s", field)
            ok = False

    logo = cfg.get("logo_path")
    if logo and not os.path.exists(logo):
        logger.error("Logo file not found: %s", logo)
        ok = False

    for i, badge in enumerate(cfg.get("badges", []), 1):
        for key in ("name", "image_url", "link"):
            if key not in badge:
                logger.error("Badge #%d missing '%s'", i, key)
                ok = False

    for i, section in enumerate(cfg.get("extra_sections", []), 1):
        for key in ("title", "content"):
            if key not in section:
                logger.error("Extra section #%d missing '%s'", i, key)
                ok = False

    return ok


def build_prompt(readme_text: str, config: dict[str, Any]) -> str:
    """Construct the prompt for the rewrite request.

    Args:
        readme_text: Current README contents.
        config: Configuration values controlling extra sections and branding.

    Returns:
        The formatted prompt string to send to the OpenAI API.
    """

    logo_block = ""
    if config.get("logo_path"):
        logo_block = f"![Logo]({config['logo_path']})"

    contact_section = ""
    if config.get("email"):
        contact_section = f"## Contact\n- Email: {config['email']}"

    sections = [
        f"## {s['title']}\n{s['content']}\n" for s in config.get("extra_sections", [])
    ]
    extra_sections_md = "\n".join(sections)

    return f"""
You are ChatGPT. Improve the project's README.md with these rules:
1. Insert logo (if provided) at the very top:
   {logo_block}
2. Include any extra sections specified in the config:
   {extra_sections_md}
3. Ensure a “Contact” section with the email is at the bottom:
   {contact_section}
4. Provide a short TL;DR summary and bullet-point suggestions, then output the fully-rewritten README.md.
5. Only use maintainer names and other details explicitly provided in the config or current README. Do not invent additional data.

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


def generate_summary(
    readme_text: str, model: str = "gpt-3.5-turbo", prompt_prefix: str | None = None
) -> str:
    """Generate a TL;DR summary of the README.

    Args:
        readme_text: The README content to summarize.
        model: OpenAI model name.
        prompt_prefix: Optional custom prompt prefix.

    Returns:
        The summary text produced by the OpenAI API.
    """

    prompt = (prompt_prefix or DEFAULT_SUMMARY_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.3, max_tokens=200)


def suggest_improvements(
    readme_text: str, model: str = "gpt-3.5-turbo", prompt_prefix: str | None = None
) -> str:
    """Provide improvement suggestions for the README.

    Args:
        readme_text: README content to analyze.
        model: OpenAI model name.
        prompt_prefix: Optional prompt prefix.

    Returns:
        Suggested improvements generated by the OpenAI API.
    """

    prompt = (prompt_prefix or DEFAULT_SUGGEST_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.5, max_tokens=400)


def rewrite_readme(
    readme_text: str,
    model: str = "gpt-3.5-turbo",
    prompt_prefix: str | None = None,
    config: dict | None = None,
) -> str:
    """Rewrite the README using OpenAI.

    Args:
        readme_text: Source README text.
        model: OpenAI model name.
        prompt_prefix: Optional custom prompt prefix.
        config: Optional configuration dict for custom sections.

    Returns:
        The rewritten README content returned by OpenAI.
    """

    if config:
        prompt = build_prompt(readme_text, config)
    else:
        prompt = (prompt_prefix or DEFAULT_REWRITE_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.7, max_tokens=1920)
