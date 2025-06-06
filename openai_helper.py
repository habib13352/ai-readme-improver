import hashlib
import json
import os
from pathlib import Path

import openai
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

def ask_openai(prompt: str, model="gpt-3.5-turbo", temperature=0.5, max_tokens=800) -> str:
    """Send a prompt to OpenAI ChatCompletion with simple on-disk caching."""

    cache_key = hashlib.sha256(f"{model}:{prompt}".encode("utf-8")).hexdigest()
    cache_file = _CACHE_DIR / f"{cache_key}.json"
    if cache_file.exists():
        with cache_file.open("r", encoding="utf-8") as f:
            return json.load(f)["response"]

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
