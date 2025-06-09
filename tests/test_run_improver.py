import os
from pathlib import Path

from run_improver import main


def test_run_improver_creates_improved(tmp_path, monkeypatch):
    # Set up temp directory with a README
    monkeypatch.chdir(tmp_path)
    readme = tmp_path / "README.md"
    readme.write_text("original", encoding="utf-8")

    # Ensure OPENAI_API_KEY is not set and archive dir uses temp path
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("readme_improver.archive.ARCHIVE_ROOT", tmp_path / "old")

    main([])

    improved = tmp_path / "README.improved.md"
    assert improved.exists()
    assert improved.read_text(encoding="utf-8") == "original"
    assert (tmp_path / "old").exists()
