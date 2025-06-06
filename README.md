# README Improver

![Logo](assets/logo.png)

*Generate polished READMEs with a single command.*

[Leer en Español](README.es.md)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) ![build](https://img.shields.io/badge/build-passing-brightgreen)

README Improver is a command-line interface (CLI) tool and GitHub Action that leverages OpenAI technology to enhance and optimize `README.md` files. It provides a concise TL;DR summary, actionable bullet-point suggestions, and a polished version of the README document.

## Features

- 📄 Auto-generates a TL;DR summary and improvement suggestions
- 📝 Produces a fully rewritten README with modern Markdown styling
- 🧩 Works locally or as a GitHub Action

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [GitHub Action Setup](#github-action-setup)
4. [Contributing](#contributing)
5. [License](#license)
6. [Maintainers](#maintainers)
7. [Acknowledgements](#acknowledgements)
8. [Contact](#contact)

## Installation

Follow these steps to install README Improver:

1. Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # For Windows: .venv\Scripts\activate
    ```

2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY` for successful execution.

## Usage

Run the CLI tool within the repository containing a `README.md` file using the command:
```bash
python main.py
```

After execution, `suggestions.md` and `README.improved.md` will be generated, providing feedback and an enhanced README version. Detailed logs are stored in `logs/run_YYYYMMDD_HHMMSS.log`, including OpenAI prompts, responses, costs, and timing details. In GitHub Actions, logs are uploaded as artifacts for retrieval.

### Quick Start

```bash
python -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
python main.py
```

## GitHub Action Setup

Configure the GitHub Action for automated feedback on `README.md` changes in pull requests by adding the following workflow to `.github/workflows/readme-improver.yml`:

```yaml
name: "README Improver CI"
on:
  pull_request:
    paths: ["README.md"]
jobs:
  improve-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: pip install "openai>=1.0" python-dotenv markdown2
      - run: echo "OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}" >> $GITHUB_ENV
      - run: python main.py
      - name: Replace README with improved version
        run: |
          mv README.improved.md README.md
          rm suggestions.md
      - name: Commit improved README
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --cached --quiet || git commit -m "chore: apply AI-suggested README improvements"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: actions/upload-artifact@v4
        with:
          name: readme-improver-logs
          path: logs
      - run: python post_comment.py
```

## Contributing

Contributions, such as issue reports or pull requests to enhance prompts or introduce new features, are encouraged.

## License

This project is licensed under the [MIT License](LICENSE).

## Maintainers

- Alice Johnson (@alicej)
- Bob Smith (@bobsmith)

## Acknowledgements

Thanks to OpenAI and the community for feedback.

## Contact

- Email: you@example.com