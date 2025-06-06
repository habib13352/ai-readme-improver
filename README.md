# AI README Improver

AI README Improver is a powerful CLI tool and GitHub Action designed to enhance and optimize `README.md` files using OpenAI technology. It offers a succinct TL;DR summary, actionable bullet-point suggestions, and a refined version of the README document.

![demo](https://via.placeholder.com/600x200.png?text=AI+README+Improver+Demo)

## Installation

To install AI README Improver, follow these steps:

```bash
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Remember to copy the `.env.example` file to `.env` and insert your `OPENAI_API_KEY`. The script will not run successfully if this key is not provided.

## Usage

Execute the CLI tool within the repository containing a `README.md` file with the following command:

```bash
python main.py
```

Upon running the script, two additional files, `suggestions.md` and `README.improved.md`, will be generated, offering feedback and an enhanced version of the README.

Comprehensive logs for each execution are stored in `logs/run_YYYYMMDD_HHMMSS.log`, capturing OpenAI prompts, responses, token usage, estimated costs, and timing details. When run in GitHub Actions, these logs are uploaded as an artifact for later download.

## GitHub Action Setup

To configure the GitHub Action for automated feedback on `README.md` changes in pull requests, add the workflow below to `.github/workflows/readme-improver.yml`:

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
      - uses: actions/upload-artifact@v4
        with:
          name: readme-improver-logs
          path: logs
      - run: python post_comment.py
```

## Contributing

Contributions in the form of issue reports or pull requests to enhance prompts or introduce new functionalities are welcome.

## License

This project is licensed under the [MIT License](LICENSE).