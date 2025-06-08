from .logger import get_logger


logger = get_logger()


def load_readme(path: str = "README.md") -> str:
    """Load the contents of a README file.

    Args:
        path: Path to the README file.

    Returns:
        The file contents as a string. If the file is missing, an empty
        string is returned and an error message is logged.
    """

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("%s not found.", path)
        return ""
