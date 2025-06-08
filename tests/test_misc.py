import os
from pathlib import Path

import readme_improver.openai_helper as openai_helper
from readme_improver.logger import get_logger
from readme_improver.improver import load_config, build_prompt


class DummyClient:
    def __init__(self, text="ok"):
        self.text = text
        self.calls = 0
        self.chat = self
        self.completions = self

    def create(self, model, messages, temperature, max_tokens):
        self.calls += 1

        class R:
            choices = [
                type(
                    "C",
                    (),
                    {
                        "message": type("M", (), {"content": self.text})(),
                        "finish_reason": "stop",
                    },
                )
            ]
            usage = type(
                "U", (), {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}
            )

        return R()


def test_build_prompt():
    cfg = {
        "logo_path": "logo.png",
        "email": "a@b.com",
        "extra_sections": [{"title": "More", "content": "Stuff"}],
    }
    prompt = build_prompt("readme", cfg)
    assert "logo.png" in prompt
    assert "## Contact" in prompt
    assert "More" in prompt


def test_load_config(tmp_path):
    p = tmp_path / "cfg.yaml"
    p.write_text("a: 1", encoding="utf-8")
    assert load_config(str(p)) == {"a": 1}
    assert load_config(str(tmp_path / "missing.yaml")) == {}


def test_get_logger_singleton():
    l1 = get_logger()
    l2 = get_logger()
    assert l1 is l2


def test_ask_openai_caching(tmp_path, monkeypatch):
    dummy = DummyClient("answer")
    monkeypatch.setattr(openai_helper, "_get_client", lambda: dummy)
    monkeypatch.setattr(openai_helper, "CACHE_DIR", Path(tmp_path))
    result1 = openai_helper.ask_openai("hi", model="test")
    result2 = openai_helper.ask_openai("hi", model="test")
    assert result1 == "answer"
    assert result2 == "answer"
    assert dummy.calls == 1
