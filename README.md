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

The CLI can analyse the `README.md` in the current directory or any other folder.

1. **Activate your environment** (if not already):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key** by copying `.env.example` to `.env` and filling
   in `OPENAI_API_KEY`.

3. **Run the CLI**:

   ```bash
   python main.py            # analyse README.md in the current directory
   python main.py path/to/project  # or point to another folder
   python main.py /path/to/README.md  # or a specific file
   ```

The script creates `suggestions.md` and `README.improved.md` next to the target README.

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
      - run: pip install openai python-dotenv markdown2
      - run: echo "OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}" >> $GITHUB_ENV
      - run: python main.py
      - run: python post_comment.py
```

## Contributing

Feel free to open issues or PRs to tweak prompts or add new features.

## License

[MIT](LICENSE)
