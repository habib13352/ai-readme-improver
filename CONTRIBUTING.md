# Contributing Guide

## How to report issues

Please use [GitHub Issues](https://github.com/username/ai-readme-improver/issues) to report bugs or request features. Include steps to reproduce and any relevant logs.

## How to submit pull requests

1. Fork the repository and create a new branch.
2. Make your changes with tests and documentation.
3. Ensure the test suite passes with `pytest`.
4. Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.
5. Open a pull request describing your changes.

## Coding style guidelines

- Run `black` for formatting.
- Lint with `flake8`.
- Keep functions small and documented.

## Commit message conventions

This project follows Conventional Commits. Examples:

- `feat: add new option`
- `fix: correct CLI error`
- `docs: update readme`

## How to run tests locally

```bash
pip install -r requirements.txt
pytest
```

## How PRs are reviewed and merged

Maintainers review each PR for style, tests and documentation. If approved, the PR is squashed and merged into `main`.
