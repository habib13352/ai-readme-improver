from openai_helper import ask_openai

def generate_summary(readme_text: str) -> str:
    prompt = (
        "You are an AI assistant that reads README files. "
        "Provide a concise TL;DR summary of the following README (2–3 lines):\n\n"
        f"{readme_text}"
    )
    return ask_openai(prompt, temperature=0.3, max_tokens=200)

def suggest_improvements(readme_text: str) -> str:
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
    prompt = (
        "You are an expert technical writer tasked with rewriting a project README. "
        "Ensure it is professional and clear. "
        "Include the sections Title, Short Description, Installation, Usage, License, Contributing, and Contact. "
        "Add extra sections only if they will genuinely help the reader. "
        "Feel free to use creative Markdown formatting such as tables, callouts, or code blocks when appropriate. "
        "Rewrite the README below:\n\n"
        f"{readme_text}"
    )
    return ask_openai(prompt, temperature=0.7, max_tokens=1920)
