#!/usr/bin/env python
from __future__ import annotations

"""Generate a high level architecture summary for the repository."""

import ast
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "architecture.md"


def iter_python_files() -> Iterable[Path]:
    """Yield all relevant Python files within the repository."""
    for path in ROOT.rglob("*.py"):
        if any(part in {".venv", "__pycache__"} for part in path.parts):
            continue
        yield path


def extract_module_info(path: Path, all_files: list[Path]):
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    module_doc = (ast.get_docstring(tree) or "").strip().splitlines()
    purpose = module_doc[0] if module_doc else "No module docstring"

    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_doc = (ast.get_docstring(node) or "").strip().splitlines()
            first_line = func_doc[0] if func_doc else ""
            args = [a.arg for a in node.args.args if a.arg != "self"]
            returns = (
                ast.unparse(node.returns).strip() if node.returns else ""
            )
            functions.append({
                "name": node.name,
                "doc": first_line,
                "args": args,
                "returns": returns,
            })

    module_name = path.with_suffix("").as_posix().replace("/", ".")
    package, _, basename = module_name.rpartition(".")
    patterns = [
        rf"\bfrom\s+{re.escape(module_name)}\s+import\b",
        rf"\bimport\s+{re.escape(module_name)}\b",
    ]
    if package:
        patterns.append(
            rf"\bfrom\s+{re.escape(package)}\s+import\s+{re.escape(basename)}\b"
        )

    usage_paths = []
    for other in all_files:
        if other == path:
            continue
        text_other = other.read_text(encoding="utf-8")
        if any(re.search(p, text_other) for p in patterns):
            usage_paths.append(other.relative_to(ROOT).as_posix())

    # Check workflows and scripts for direct references
    for wf in ROOT.rglob("*.yml"):
        if path.name in wf.read_text(encoding="utf-8"):
            usage_paths.append(wf.relative_to(ROOT).as_posix())

    return {
        "path": path.relative_to(ROOT).as_posix(),
        "purpose": purpose,
        "functions": functions,
        "used_in": sorted(usage_paths),
    }


def generate_markdown(modules: list[dict]) -> str:
    lines = ["# Project Architecture", ""]
    for info in sorted(modules, key=lambda x: x["path"]):
        lines.append(f"## {info['path']}")
        lines.append(f"**Purpose:** {info['purpose']}")
        func_names = [f["name"] + "()" for f in info["functions"]]
        lines.append(f"**Key Functions:** {', '.join(func_names) if func_names else 'None'}")
        io_details = []
        for f in info["functions"]:
            sig = f"{f['name']}({', '.join(f['args'])})"
            if f["returns"]:
                sig += f" -> {f['returns']}"
            if f["doc"]:
                sig += f" - {f['doc']}"
            io_details.append(sig)
        if io_details:
            lines.append("**Inputs/Outputs:**")
            for det in io_details:
                lines.append(f"- {det}")
        used = info["used_in"]
        if used:
            lines.append(f"**Used in:** {', '.join(used)}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    all_files = list(iter_python_files())
    modules = [extract_module_info(p, all_files) for p in all_files]
    md = generate_markdown(modules)
    DOC_PATH.write_text(md, encoding="utf-8")
    print(f"Wrote architecture documentation to {DOC_PATH}")


if __name__ == "__main__":
    main()
