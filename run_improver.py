"""Command line entry point to generate README suggestions and rewrites."""

import argparse
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

from readme_improver.readme_loader import load_readme
from readme_improver.improver import (
    generate_summary,
    suggest_improvements,
    rewrite_readme,
    load_config,
)
from readme_improver.logger import get_logger
from readme_improver.archive import archive_old_files


logger = get_logger()


def main(argv=None):
    """Run the CLI."""
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(prog="ai-readme-improver")
    parser.add_argument("--readme", default="README.md", help="Path to README")
    parser.add_argument(
        "--suggestions", default="suggestions.md", help="Suggestions output file"
    )
    parser.add_argument(
        "--improved", default="README.improved.md", help="Improved README output file"
    )
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model")
    parser.add_argument("--logo", help="Path or URL for a project logo")
    parser.add_argument("--email", help="Contact email address for the README")
    parser.add_argument(
        "--badge",
        action="append",
        metavar="SPEC",
        help="Badge spec 'name,image_url,link' (repeatable)",
    )
    parser.add_argument(
        "--extra-section",
        action="append",
        metavar="SPEC",
        help="Extra section 'Title:Content' (repeatable)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    config = load_config(args.config)
    env_email = os.getenv("README_EMAIL")
    if env_email:
        config["email"] = env_email
    env_logo = os.getenv("README_LOGO")
    if env_logo:
        config["logo_path"] = env_logo

    if args.logo:
        config["logo_path"] = args.logo
    if args.email:
        config["email"] = args.email

    if args.badge:
        badges = []
        for spec in args.badge:
            parts = [p.strip() for p in spec.split(",")]
            if len(parts) == 3:
                badges.append({"name": parts[0], "image_url": parts[1], "link": parts[2]})
            else:
                logger.warning("Ignoring invalid badge spec: %s", spec)
        if badges:
            config["badges"] = badges

    if args.extra_section:
        extras = []
        for spec in args.extra_section:
            if ":" in spec:
                title, content = spec.split(":", 1)
                extras.append({"title": title.strip(), "content": content.strip()})
            else:
                logger.warning("Ignoring invalid extra section spec: %s", spec)
        if extras:
            config.setdefault("extra_sections", [])
            config["extra_sections"].extend(extras)

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        logger.error("OPENAI_API_KEY is not set. Falling back to original README.")

    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    archive_dir = archive_old_files(timestamp)

    readme_path = archive_dir / Path(args.readme).name
    if not readme_path.exists():
        logger.error("❌ Error: %s not found.", readme_path)
        return

    readme_text = load_readme(str(readme_path))
    if not readme_text.strip():
        logger.warning("⚠️ README is empty. Exiting.")
        return

    if openai_key:
        logger.info("🔹 Generating TL;DR summary...")
        summary = generate_summary(readme_text, args.model)
        logger.info("\n--- TL;DR SUMMARY ---\n%s\n----------------------\n", summary)

        logger.info("🔹 Generating improvement suggestions...")
        suggestions = suggest_improvements(readme_text, args.model)
        logger.info(
            "\n--- IMPROVEMENT SUGGESTIONS ---\n%s\n--------------------------------\n",
            suggestions,
        )
    else:
        summary = "OPENAI_API_KEY not provided; using original README."
        suggestions = "No suggestions generated."

    with open(args.suggestions, "w", encoding="utf-8") as f:
        f.write("# 🤖 AI README Improver Feedback\n\n")
        f.write("## TL;DR Summary\n\n")
        f.write(summary.strip() + "\n\n")
        f.write("## Improvement Suggestions\n\n")
        f.write(suggestions.strip() + "\n\n")
        f.write("---\n*Powered by [OpenAI](https://openai.com)*\n")
    logger.info("✅ Wrote feedback to %s", args.suggestions)

    logger.info("🔹 Generating rewritten README → %s", args.improved)
    if openai_key:
        improved = rewrite_readme(readme_text, args.model, config=config)
    else:
        improved = readme_text
    with open(args.improved, "w", encoding="utf-8") as f:
        f.write(improved)
    logger.info("✅ Saved improved version to %s\n", args.improved)


if __name__ == "__main__":
    main()
