# AI README Improver

A CLI tool and GitHub Action that uses OpenAI to analyze and improve `README.md` files. It provides a short TL;DR summary, bullet-point suggestions, and a fully rewritten version of the README.

![demo](https://via.placeholder.com/600x200.png?text=AI+README+Improver+Demo)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.

## Usage

Run the CLI in the repository that contains a `README.md`:

```bash
python main.py
```

The script creates `suggestions.md` and `README.improved.md` with feedback and a polished version of the README.

## GitHub Action Setup

Add the workflow below to `.github/workflows/readme-improver.yml` to automatically post suggestions when a PR modifies `README.md`:

```yaml
name: "AI README Improver CI"
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
      - run: python post_comment.py
```

### Auto-update README

If you also want the improved README committed automatically, add a second
workflow like this:

```yaml
name: "AI README Auto Update"
on:
  workflow_dispatch:
permissions:
  contents: write
jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: pip install "openai>=1.0" python-dotenv markdown2
      - run: echo "OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}" >> $GITHUB_ENV
      - run: python main.py
      - run: |
          mkdir -p readme-archive
          timestamp=$(date +'%Y%m%d_%H%M%S')
          cp README.md "readme-archive/README.$timestamp.md"
          cp README.improved.md README.md
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "chore: auto update README"
          file_pattern: "README.md readme-archive/*"
```

## Contributing

Feel free to open issues or PRs to tweak prompts or add new features.

## License

[MIT](LICENSE)
