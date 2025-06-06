"""Functions that interact with OpenAI to analyse and rewrite README files."""

from openai_helper import ask_openai

def generate_summary(readme_text: str) -> str:
    """Return a short TL;DR summary of ``readme_text`` using OpenAI."""

    prompt = (
        "You are an AI assistant that reads README files. "
        "Provide a concise TL;DR summary of the following README (2–3 lines):\n\n"
        f"{readme_text}"
    )
    return ask_openai(prompt, temperature=0.3, max_tokens=200)

def suggest_improvements(readme_text: str) -> str:
    """Return bullet-point suggestions to enhance ``readme_text``."""

    prompt = (
        "You are an expert technical writer. "
        "Suggest specific improvements for this README. "
        "Mention missing sections (Installation, Usage, License, etc.), "
        "clarity of language, badge additions, and SEO keywords. "
        "Output as bullet points:\n\n"
        f"{readme_text}"
    )
    return ask_openai(prompt, temperature=0.5, max_tokens=400)

def rewrite_readme(readme_text: str) -> str:
    """Return a rewritten version of ``readme_text`` with common sections."""

    prompt = (
        "You are an AI that rewrites project README files to be more professional, clear, and complete. "
        "Rewrite the following README, ensuring it includes these sections: "
        "Title, Short Description, Installation, Usage, License, Contributing, Contact. "
        "Use Markdown formatting:\n\n"
        f"{readme_text}"
    )
    return ask_openai(prompt, temperature=0.7, max_tokens=1200)

