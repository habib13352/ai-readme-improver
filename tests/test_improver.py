from readme_improver.improver import (
    generate_summary,
    suggest_improvements,
    rewrite_readme,
)


def dummy_ask(prompt, model="gpt-3.5-turbo", temperature=0.5, max_tokens=800):
    return f"RESPONSE: {prompt[:20]}"


def test_generate_summary(monkeypatch):
    monkeypatch.setattr("readme_improver.improver.ask_openai", dummy_ask)
    result = generate_summary("Readme")
    assert "RESPONSE" in result


def test_suggest_improvements(monkeypatch):
    monkeypatch.setattr("readme_improver.improver.ask_openai", dummy_ask)
    result = suggest_improvements("Readme")
    assert "RESPONSE" in result


def test_rewrite_readme(monkeypatch):
    monkeypatch.setattr("readme_improver.improver.ask_openai", dummy_ask)
    result = rewrite_readme("Readme")
    assert "RESPONSE" in result
