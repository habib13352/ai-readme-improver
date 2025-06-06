"""Utility for loading README files."""


def load_readme(path: str = "README.md") -> str:
    """Return the contents of ``path`` or an empty string if it doesn't exist."""

    try:
        # ``encoding='utf-8'`` allows reading files with emojis or other
        # non-ascii characters without errors.
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return ""
