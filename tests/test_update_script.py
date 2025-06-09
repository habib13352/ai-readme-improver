import json
from datetime import datetime
from pathlib import Path

import scripts.update_readme as upd

class FakeDT(datetime):
    @classmethod
    def utcnow(cls):
        return cls(2025, 1, 1, 0, 0)

def test_update_readme_main(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("data", encoding="utf-8")
    (tmp_path / "config.yaml").write_text("", encoding="utf-8")

    monkeypatch.setattr(upd, "ARCHIVE_ROOT", tmp_path / "old")
    monkeypatch.setattr(upd, "datetime", FakeDT)
    monkeypatch.setattr(upd, "generate_summary", lambda t: "s")
    monkeypatch.setattr(upd, "suggest_improvements", lambda t: "i")
    monkeypatch.setattr(upd, "rewrite_readme", lambda t, config=None: t)

    upd.main()

    archived = tmp_path / "old" / "2025-01-01-00-00" / "README.md"
    assert archived.exists()
    assert (tmp_path / "README.improved.md").exists()
    assert (tmp_path / "suggestions.md").exists()
