from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path

from readme_improver.improver import (
    generate_summary,
    suggest_improvements,
    rewrite_readme,
    load_config,
)
from readme_improver.readme_loader import load_readme


ARCHIVE_ROOT = Path("oldreadme")
CONFIG_PATH = "readme-improver.config.yaml"


def archive_previous(timestamp: str) -> Path:
    """Move existing generated files into a timestamped archive directory."""
    archive_dir = ARCHIVE_ROOT / timestamp
    archive_dir.mkdir(parents=True, exist_ok=True)
    for name in ["README.md", "SUGGESTED_README.md", "README_SUGGESTIONS.md"]:
        path = Path(name)
        if path.exists():
            shutil.move(str(path), archive_dir / path.name)
    return archive_dir


def generate_files(readme_text: str, cfg: dict) -> None:
    """Generate updated README, suggestions and save them."""
    summary = generate_summary(readme_text)
    suggestions = suggest_improvements(readme_text)
    improved = rewrite_readme(readme_text, config=cfg)

    Path("SUGGESTED_README.md").write_text(improved, encoding="utf-8")
    Path("README.md").write_text(improved, encoding="utf-8")

    suggestion_content = (
        "# 🤖 AI README Improver Feedback\n\n"
        "## TL;DR Summary\n\n"
        f"{summary}\n\n"
        "## Improvement Suggestions\n\n"
        f"{suggestions}\n\n"
        "---\n*Powered by [OpenAI](https://openai.com)*\n"
    )
    Path("README_SUGGESTIONS.md").write_text(suggestion_content, encoding="utf-8")


def main() -> None:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    archive_dir = archive_previous(timestamp)

    readme_src = archive_dir / "README.md"
    readme_text = load_readme(str(readme_src))
    if not readme_text.strip():
        print("No README content found to process.")
        return

    cfg = load_config(CONFIG_PATH)
    generate_files(readme_text, cfg)


if __name__ == "__main__":
    main()
