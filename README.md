# AI README Enhancer

*Generate polished READMEs with a single command.*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) ![build](https://img.shields.io/badge/build-passing-brightgreen)

![Demo](https://via.placeholder.com/600x200.png?text=AI+README+Enhancer+Demo)

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
6. [Contact](#contact)

## Installation

To install AI README Enhancer, please follow these steps:

1. Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # For Windows: .venv\Scripts\activate
    ```
2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Copy the `.env.example` file to `.env` and insert your `OPENAI_API_KEY`. The script will not function correctly without this key.

## Usage

Run the CLI tool within the repository that contains a `README.md` file using the following command:

```bash
python main.py
```

### Quick Start

```bash
python -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
python main.py
```

Upon execution, two new files, `suggestions.md` and `README.improved.md`, will be generated, providing feedback and an enhanced version of the README.

Detailed logs for each run are saved in `logs/run_YYYYMMDD_HHMMSS.log`, capturing OpenAI prompts, responses, token usage, estimated costs, and timing information. If executed in GitHub Actions, these logs are uploaded as an artifact for future reference.

## GitHub Action Setup

To set up the GitHub Action for automated feedback on changes to `README.md` in pull requests, add the following workflow to `.github/workflows/readme-enhancer.yml`:

```yaml
name: "AI README Enhancer CI"
on:
  pull_request:
    paths: ["README.md"]
jobs:
  enhance-readme:
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
          name: readme-enhancer-logs
          path: logs
      - run: python post_comment.py
```

## Contributing

We welcome contributions in the form of issue reports or pull requests to enhance prompts or introduce new features.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or feedback, feel free to reach out to us at [email@example.com](mailto:email@example.com).
