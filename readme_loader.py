def load_readme(path: str = "README.md") -> str:
    """Load the contents of a README file.

    Args:
        path: Path to the README file.

    Returns:
        The file contents as a string. If the file is missing, an empty
        string is returned and an error message is printed.
    """

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return ""
