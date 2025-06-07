# Workflow Setup and Logging Guide

This guide explains how to set up a GitHub Actions workflow that runs automatically or manually, logs each API call to disk, and provides prompts and tests to ensure everything works.

## 1. Define the GitHub Actions Workflow

The repository needs a workflow file (for example, `.github/workflows/improve_readme.yml`) with these key features:

- **Automatic trigger**: run whenever a pull request modifies `README.md` or `ai_readme_improver.py` so that improvements are always reviewed.
- **Manual trigger**: enable `workflow_dispatch` so you can start a job through the Actions tab at any time.
- **Workflow steps**: checkout the repo, set up Python, install requirements, run the script, and commit the updated README and logs if anything changed.
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

1. **Local test**: Run `python ai_readme_improver.py --input README.md --output README.test.md --log-dir logs_test` with your OpenAI API key set. Confirm that `README.test.md` appears and a log file is written in `logs_test`.
2. **PR-based test**:
   - Commit the workflow and updated script to a feature branch.
   - Open a pull request to `main`. The workflow should run automatically, produce an improved README, and create logs.
3. You can also trigger the job manually from the Actions tab and inspect the logs for JSON files with prompts, responses, and timing info.

With these pieces in place, you can reliably improve your README via GPT models while keeping a clear record of every API call.
This overview should help you quickly implement the pipeline and understand the key areas to customize. Feel free to adapt the workflow for other files or expand the logging as needed.
