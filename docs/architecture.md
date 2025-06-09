# Project Architecture

## main.py

**Purpose:** No module docstring
**Key Functions:** None

## `readme_improver/__init__.py`

**Purpose:** Utilities for the ai-readme-improver package.
**Key Functions:** None

## readme_improver/improver.py

**Purpose:** No module docstring
**Key Functions:** load_config(), build_prompt(), generate_summary(), suggest_improvements(), rewrite_readme()
**Inputs/Outputs:**

- load_config(path) -> dict[str, Any] - Load configuration values from a YAML file.
- build_prompt(readme_text, config) -> str - Construct the prompt for the rewrite request.
- generate_summary(readme_text, model, prompt_prefix) -> str - Generate a TL;DR summary of the README.
- suggest_improvements(readme_text, model, prompt_prefix) -> str - Provide improvement suggestions for the README.
- rewrite_readme(readme_text, model, prompt_prefix, config) -> str - Rewrite the README using OpenAI.
**Used in:** .github/workflows/readme-improver.yml

## readme_improver/logger.py

**Purpose:** No module docstring
**Key Functions:** get_logger()
**Inputs/Outputs:**

- get_logger() -> logging.Logger - Return a configured logger writing to file and console.

## readme_improver/openai_helper.py

**Purpose:** No module docstring
**Key Functions:** _get_client(), _estimate_cost(), ask_openai()
**Inputs/Outputs:**

- _get_client() -> 'OpenAI' - Create the OpenAI client lazily.
- _estimate_cost(model, total_tokens) -> float - Estimate API cost for a given model and token count.
- ask_openai(prompt, model, temperature, max_tokens) -> str - Send a prompt to OpenAI ChatCompletion with caching. Writes request and response details to JSON files under `logs/`.

## readme_improver/post_comment.py

**Purpose:** No module docstring
**Key Functions:** get_pr_number(), main()
**Inputs/Outputs:**

- get_pr_number() -> str - Extract the pull request number from the GitHub event payload.
- main() - Post README improvement suggestions as a PR comment.
**Used in:** .github/workflows/readme-improver.yml

## readme_improver/readme_loader.py

**Purpose:** No module docstring
**Key Functions:** load_readme()
**Inputs/Outputs:**

- load_readme(path) -> str - Load the contents of a README file.

## run_improver.py

**Purpose:** No module docstring
**Key Functions:** main()
**Inputs/Outputs:**

- main(argv) - Run the CLI.
**Used in:** .github/workflows/readme-improver.yml

## scripts/generate_architecture_md.py

**Purpose:** No module docstring
**Key Functions:** iter_python_files(), extract_module_info(), generate_markdown(), main()
**Inputs/Outputs:**

- iter_python_files() -> Iterable[Path] - Yield all relevant Python files within the repository.
- extract_module_info(path, all_files)
- generate_markdown(modules) -> str
- main() -> None

## scripts/update_readme.py

**Purpose:** No module docstring
**Key Functions:** archive_previous(), generate_files(), main()
**Inputs/Outputs:**

- archive_previous(timestamp) -> Path - Move existing generated files into a timestamped archive directory.
- generate_files(readme_text, cfg) -> None - Generate updated README, suggestions and save them.
- main() -> None
**Used in:** .github/workflows/auto-docs.yml

## `tests/__init__.py`

**Purpose:** No module docstring
**Key Functions:** None

## tests/test_improver.py

**Purpose:** No module docstring
**Key Functions:** dummy_ask(), test_generate_summary(), test_suggest_improvements(), test_rewrite_readme()
**Inputs/Outputs:**

- dummy_ask(prompt, model, temperature, max_tokens)
- test_generate_summary(monkeypatch)
- test_suggest_improvements(monkeypatch)
- test_rewrite_readme(monkeypatch)

## tests/test_misc.py

**Purpose:** No module docstring
**Key Functions:** test_build_prompt(), test_load_config(), test_get_logger_singleton(), test_ask_openai_caching()
**Inputs/Outputs:**

- test_build_prompt()
- test_load_config(tmp_path)
- test_get_logger_singleton()
- test_ask_openai_caching(tmp_path, monkeypatch)

## tests/test_readme_loader.py

**Purpose:** No module docstring
**Key Functions:** test_load_readme_not_found(), test_load_readme()
**Inputs/Outputs:**

- test_load_readme_not_found(tmp_path)
- test_load_readme(tmp_path)
