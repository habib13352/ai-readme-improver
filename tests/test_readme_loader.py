import os
from readme_loader import load_readme

def test_load_readme_not_found(tmp_path):
    path = tmp_path / "missing.md"
    assert load_readme(str(path)) == ""

def test_load_readme(tmp_path):
    p = tmp_path / "README.md"
    p.write_text("hello", encoding="utf-8")
    assert load_readme(str(p)) == "hello"
