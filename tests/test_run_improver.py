from pathlib import Path

from run_improver import main


def test_run_improver_creates_improved(tmp_path, monkeypatch):
    # Set up temp directory with a README
    monkeypatch.chdir(tmp_path)
    readme = tmp_path / "README.md"
    readme.write_text("original", encoding="utf-8")

    # Ensure OPENAI_API_KEY is not set and use temp archive directory
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    main(["--archive-dir", str(tmp_path / "old")])

    improved = tmp_path / "README.improved.md"
    assert improved.exists()
    assert improved.read_text(encoding="utf-8") == "original"
    assert (tmp_path / "old").exists()
    # suggestions.md should also be created
    assert (tmp_path / "suggestions.md").exists()
