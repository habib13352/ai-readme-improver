from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ARCHIVE_ROOT = Path("oldreadme")


def archive_old_files(timestamp: str | None = None) -> Path:
    """Archive existing generated files under a timestamped folder.

    Parameters
    ----------
    timestamp:
        Optional timestamp string to use for the archive directory. If not
        provided, the current UTC time is used.

    Returns
    -------
    Path
        The path to the created archive directory.
    """
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

    archive_dir = ARCHIVE_ROOT / timestamp
    archive_dir.mkdir(parents=True, exist_ok=True)

    for name in ["README.md", "README.improved.md", "suggestions.md"]:
        path = Path(name)
        if path.exists():
            shutil.move(str(path), archive_dir / path.name)

    return archive_dir
