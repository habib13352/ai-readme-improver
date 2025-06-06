from openai_helper import ask_openai


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

def rewrite_readme(readme_text: str, model: str = "gpt-3.5-turbo", prompt_prefix: str | None = None) -> str:
    prompt = (prompt_prefix or DEFAULT_REWRITE_PROMPT) + readme_text
    return ask_openai(prompt, model=model, temperature=0.7, max_tokens=1200)
