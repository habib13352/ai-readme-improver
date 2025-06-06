import os
import sys
from readme_loader import load_readme
from improver import generate_summary, suggest_improvements, rewrite_readme


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print(f"❌ Error: {readme_path} not found.")
        return

    readme_text = load_readme(readme_path)
    if not readme_text.strip():
        print("⚠️ README is empty. Exiting.")
        return

    print("🔹 Generating TL;DR summary...")
    summary = generate_summary(readme_text)
    print("\n--- TL;DR SUMMARY ---\n")
    print(summary)
    print("\n----------------------\n")

    print("🔹 Generating improvement suggestions...")
    suggestions = suggest_improvements(readme_text)
    print("\n--- IMPROVEMENT SUGGESTIONS ---\n")
    print(suggestions)
    print("\n--------------------------------\n")

    with open("suggestions.md", "w", encoding="utf-8") as f:
        f.write("# 🤖 AI README Improver Feedback\n\n")
        f.write("## TL;DR Summary\n\n")
        f.write(summary.strip() + "\n\n")
        f.write("## Improvement Suggestions\n\n")
        f.write(suggestions.strip() + "\n\n")
        f.write("---\n*Powered by [OpenAI](https://openai.com)*\n")
    print("✅ Wrote feedback to suggestions.md")

    print("🔹 Generating rewritten README → README.improved.md")
    improved = rewrite_readme(readme_text)
    with open("README.improved.md", "w", encoding="utf-8") as f:
        f.write(improved)
    print("✅ Saved improved version to README.improved.md\n")


if __name__ == "__main__":
    main()
