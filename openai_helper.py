import hashlib
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

def _get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Add it to your .env or environment variables"
        )
    return key

_CACHE_DIR = Path(".cache")
_CACHE_DIR.mkdir(exist_ok=True)

def ask_openai(
    prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.5, max_tokens: int = 800
) -> str:
    """Send a prompt to OpenAI ChatCompletion with simple on-disk caching.

    The OpenAI package is imported lazily so unit tests can patch this function
    without requiring the dependency to be installed.
    """

    cache_key = hashlib.sha256(f"{model}:{prompt}".encode("utf-8")).hexdigest()
    cache_file = _CACHE_DIR / f"{cache_key}.json"
    if cache_file.exists():
        with cache_file.open("r", encoding="utf-8") as f:
            return json.load(f)["response"]

    try:
        import openai  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "The 'openai' package is required to use this tool. Install it via 'pip install openai'."
        ) from exc

    openai.api_key = _get_api_key()
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except openai.error.OpenAIError as exc:
        raise RuntimeError(f"OpenAI API request failed: {exc}") from exc

    text = response.choices[0].message.content.strip()
    with cache_file.open("w", encoding="utf-8") as f:
        json.dump({"response": text}, f)
    return text
