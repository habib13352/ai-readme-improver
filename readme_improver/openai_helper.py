"""Lightweight OpenAI helper with logging and optional disk caching.

The response for each request is cached under ``.cache/`` by default to
avoid unnecessary API calls. Set the environment variable
``README_IMPROVER_CACHE=0`` to disable caching entirely.
"""

import hashlib
import json
import os
import time
import traceback
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from .logger import get_logger

try:
    from openai import RateLimitError
except Exception:  # pragma: no cover - openai may not be installed
    class RateLimitError(Exception):
        """Fallback when openai package is missing."""

logger = get_logger()

load_dotenv()

_openai_client = None
CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)
# Directory for JSON logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
# Set README_IMPROVER_CACHE=0 to disable caching
CACHE_ENABLED = os.getenv("README_IMPROVER_CACHE", "1") != "0"


def _get_client() -> "OpenAI":
    """Create the OpenAI client lazily."""
    global _openai_client
    if _openai_client is None:
        try:
            from openai import OpenAI  # type: ignore
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "The 'openai' package is required to use this tool. Install it via 'pip install openai'."
            ) from exc
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to your .env file or environment variables."
            )
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


# Rough USD cost per 1K tokens for supported models
MODEL_COST_PER_1K = {
    "gpt-3.5-turbo": 0.002,
}


def _estimate_cost(model: str, total_tokens: int) -> float:
    """Estimate API cost for a given model and token count.

    Args:
        model: Model name used for the request.
        total_tokens: Total tokens consumed by the request.

    Returns:
        Approximate USD cost based on predefined pricing.
    """

    price = MODEL_COST_PER_1K.get(model, 0)
    return (total_tokens / 1000) * price


def ask_openai(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
    max_tokens: int = 1280,
) -> str:
    """Send a prompt to OpenAI ChatCompletion with caching and detailed logging.

    The response is cached on disk to avoid unnecessary API calls.
    """

    cache_key = hashlib.sha256(f"{model}:{prompt}".encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.json"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"{timestamp}.json"

    try:
        if CACHE_ENABLED and cache_file.exists():
            with cache_file.open("r", encoding="utf-8") as f:
                content = json.load(f)["response"]
            usage = None
            elapsed = 0.0
        else:
            logger.info("\n----- OpenAI Request -----")
            logger.info(
                f"Model: {model} | Temperature: {temperature} | Max tokens: {max_tokens}"
            )
            logger.info("Prompt:\n" + prompt)

            start = time.time()
            client = _get_client()
            for attempt in range(3):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                    break
                except RateLimitError:
                    wait = 2 ** attempt
                    logger.warning("Rate limited by OpenAI, retrying in %ss", wait)
                    time.sleep(wait)
            else:
                raise RuntimeError("Exceeded OpenAI retry attempts")

            elapsed = time.time() - start

            content = response.choices[0].message.content.strip()
            finish_reason = response.choices[0].finish_reason
            usage = response.usage

            if usage:
                cost = _estimate_cost(model, usage.total_tokens)
                logger.info(
                    f"Tokens: prompt={usage.prompt_tokens} completion={usage.completion_tokens} "
                    f"total={usage.total_tokens}"
                )
                logger.info(f"Estimated cost: ${cost:.6f}")
            else:
                logger.info("Token usage unavailable")
            if finish_reason and finish_reason != "stop":
                logger.warning(f"Response truncated (finish_reason={finish_reason})")
            else:
                logger.info(f"Finish reason: {finish_reason}")
            logger.info(f"Elapsed time: {elapsed:.2f}s")
            logger.info("Response:\n" + content)
            logger.info("----- End Request -----\n")

            if CACHE_ENABLED:
                with cache_file.open("w", encoding="utf-8") as f:
                    json.dump({"response": content}, f)

        log_data = {
            "prompt": prompt,
            "response": content,
            "elapsed": elapsed,
            "usage": (
                {
                    "prompt_tokens": getattr(usage, "prompt_tokens", None),
                    "completion_tokens": getattr(usage, "completion_tokens", None),
                    "total_tokens": getattr(usage, "total_tokens", None),
                }
                if usage
                else None
            ),
        }
        with log_path.open("w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)

        return content
    except Exception:
        error_path = LOG_DIR / f"{timestamp}_error.json"
        with error_path.open("w", encoding="utf-8") as f:
            json.dump({"prompt": prompt, "error": traceback.format_exc()}, f, indent=2)
        raise
