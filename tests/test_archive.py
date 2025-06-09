import os
from pathlib import Path
from readme_improver import archive


def test_archive_old_files(tmp_path, monkeypatch):
    # Set up temp working directory with files
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("r", encoding="utf-8")
    (tmp_path / "README.improved.md").write_text("i", encoding="utf-8")
    (tmp_path / "suggestions.md").write_text("s", encoding="utf-8")

    monkeypatch.setattr(archive, "ARCHIVE_ROOT", tmp_path / "old")
    archive_dir = archive.archive_old_files("2025-01-01-00-00")

    assert archive_dir == tmp_path / "old" / "2025-01-01-00-00"
    assert (archive_dir / "README.md").exists()
    assert (archive_dir / "README.improved.md").exists()
    assert (archive_dir / "suggestions.md").exists()
    # Original files should be removed
    assert not (tmp_path / "README.md").exists()
    assert not (tmp_path / "README.improved.md").exists()
    assert not (tmp_path / "suggestions.md").exists()
