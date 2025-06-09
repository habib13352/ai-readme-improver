import json
from pathlib import Path
import subprocess

from readme_improver import post_comment


def test_post_comment_missing_file(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"number": 1}}))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("GITHUB_TOKEN", "t")
    monkeypatch.setenv("GITHUB_REPOSITORY", "r")
    monkeypatch.setattr(post_comment, "GITHUB_EVENT_PATH", str(event))
    monkeypatch.setattr(post_comment, "GITHUB_TOKEN", "t")
    monkeypatch.setattr(post_comment, "REPO", "r")
    post_comment.main()
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_post_comment_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "suggestions.md").write_text("body", encoding="utf-8")
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"number": 2}}))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("GITHUB_TOKEN", "t")
    monkeypatch.setenv("GITHUB_REPOSITORY", "r")
    monkeypatch.setattr(post_comment, "GITHUB_EVENT_PATH", str(event))
    monkeypatch.setattr(post_comment, "GITHUB_TOKEN", "t")
    monkeypatch.setattr(post_comment, "REPO", "r")

    called = {}

    def fake_run(cmd, capture_output, text):
        called["cmd"] = cmd
        class R:
            returncode = 0
            stderr = ""
        return R()

    monkeypatch.setattr(subprocess, "run", fake_run)
    post_comment.main()
    assert called["cmd"][0] == "gh"
