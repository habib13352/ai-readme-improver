import argparse
import logging
import os
import sys

from readme_loader import load_readme
from improver import generate_summary, suggest_improvements, rewrite_readme


def main(argv=None):
    """Run the CLI."""
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="AI README Improver")
    parser.add_argument("--readme", default="README.md", help="Path to README")
    parser.add_argument("--suggestions", default="suggestions.md", help="Suggestions output file")
    parser.add_argument("--improved", default="README.improved.md", help="Improved README output file")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model to use")
    parser.add_argument("--summary-prompt", default=None, help="Override summary prompt")
    parser.add_argument("--suggest-prompt", default=None, help="Override suggestion prompt")
    parser.add_argument("--rewrite-prompt", default=None, help="Override rewrite prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(message)s")

    readme_path = args.readme
    if not os.path.exists(readme_path):
        logging.error("❌ Error: %s not found.", readme_path)
        return

    readme_text = load_readme(readme_path)
    if not readme_text.strip():
        logging.warning("⚠️ README is empty. Exiting.")
        return

    logging.info("🔹 Generating TL;DR summary...")
    summary = generate_summary(readme_text, args.model, args.summary_prompt)
    logging.info("\n--- TL;DR SUMMARY ---\n%s\n----------------------\n", summary)

    logging.info("🔹 Generating improvement suggestions...")
    suggestions = suggest_improvements(readme_text, args.model, args.suggest_prompt)
    logging.info("\n--- IMPROVEMENT SUGGESTIONS ---\n%s\n--------------------------------\n", suggestions)

    with open(args.suggestions, "w", encoding="utf-8") as f:
        f.write("# 🤖 AI README Improver Feedback\n\n")
        f.write("## TL;DR Summary\n\n")
        f.write(summary.strip() + "\n\n")
        f.write("## Improvement Suggestions\n\n")
        f.write(suggestions.strip() + "\n\n")
        f.write("---\n*Powered by [OpenAI](https://openai.com)*\n")
    logging.info("✅ Wrote feedback to %s", args.suggestions)

    logging.info("🔹 Generating rewritten README → %s", args.improved)
    improved = rewrite_readme(readme_text, args.model, args.rewrite_prompt)
    with open(args.improved, "w", encoding="utf-8") as f:
        f.write(improved)
    logging.info("✅ Saved improved version to %s\n", args.improved)


if __name__ == "__main__":
    main()
