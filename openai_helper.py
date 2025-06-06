"""Helper utilities for sending prompts to OpenAI."""

import os
import openai
from dotenv import load_dotenv

# ``python-dotenv`` loads variables from a .env file so the API key can be
# stored locally without hard coding it into the script.
load_dotenv()

# Read the API key from the environment. ``load_dotenv`` above will populate
# it from a ``.env`` file if present.
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise RuntimeError("OPENAI_API_KEY not set in .env")

def ask_openai(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
    max_tokens: int = 800,
) -> str:
    """Send ``prompt`` to OpenAI and return the response text."""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


