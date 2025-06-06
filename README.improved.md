# AI README Improver

A CLI tool and GitHub Action that leverages OpenAI to analyze and enhance `README.md` files. It offers a concise summary, bullet-point recommendations, and a refined version of the README.

![demo](https://via.placeholder.com/600x200.png?text=AI+README+Improver+Demo)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Duplicate `.env.example` as `.env` and insert your `OPENAI_API_KEY`.

## Usage

Execute the CLI within the repository containing a `README.md`:

```bash
python main.py
```

The tool generates `suggestions.md` and `README.improved.md` with insights and an enhanced version of the README.

## GitHub Action Setup

Include the workflow below in `.github/workflows/readme-improver.yml` to automatically provide suggestions when a PR modifies `README.md`:

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

## Contributing

Please feel free to raise issues or PRs to adjust prompts or introduce new functionalities.

## License

[MIT](LICENSE)