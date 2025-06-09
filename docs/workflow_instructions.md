# Workflow Setup and Logging Guide

This guide explains how to set up a simple GitHub Actions workflow that installs dependencies, runs `run_improver.py`, and commits the resulting README.

## 1. Define the GitHub Actions Workflow

Create `.github/workflows/readme-improver.yml` containing a job that:
- Checks out the repository
- Sets up Python and installs `requirements.txt`
- Runs `python run_improver.py` with `OPENAI_API_KEY` provided
- Commits `README.improved.md` back to `README.md` and pushes the result

## 2. Logging in the Python Script

- Accept `--input`, `--output`, and `--log-dir` arguments.
- Create `--log-dir` if it does not exist.
- Capture the start time and end time of the OpenAI request.
- Store the prompt text, the entire API response, and usage statistics (if available) in `log_<UTC timestamp>.json` inside `logs/`.
- On error, write `<timestamp>_error.json` with the stack trace before re-raising the exception.

## 3. Example Codex Prompts

Example Codex prompts:

- "Create the workflow file with auto and manual triggers that installs requirements, runs the improver, checks for changes, and pushes updates."
- "Add logging in ai_readme_improver.py to record prompts, responses, timing, and usage."
- "Describe how to manually run the workflow from the Actions tab."

## 4. Verifying End-to-End Execution

1. **Local test**: Run `python run_improver.py` with your `OPENAI_API_KEY` set. Confirm that `README.improved.md` and `suggestions.md` appear and logs are written.
2. **PR-based test**:
   - Commit the workflow and updated script to a feature branch.
   - Open a pull request to `main`. The workflow should run automatically and push the improved README.
3. You can also trigger the job manually from the Actions tab.

With these pieces in place, you can reliably improve your README via GPT models while keeping a clear record of every API call.
This overview should help you quickly implement the pipeline and understand the key areas to customize. Feel free to adapt the workflow for other files or expand the logging as needed.
