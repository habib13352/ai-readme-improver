"""GitHub Action helper to post README suggestions as a pull request comment."""

import os
import sys
import subprocess
import json

GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")


def get_pr_number() -> str:
    """Extract the pull request number from the GitHub Actions event file."""

    with open(GITHUB_EVENT_PATH, "r") as f:
        payload = json.load(f)
    pr = payload.get("pull_request")
    if not pr:
        print("❌ Not triggered by a pull request. Exiting.")
        sys.exit(1)
    return str(pr.get("number"))


def main():
    """Post the contents of ``suggestions.md`` as a PR comment using ``gh``."""

    suggestions_file = "suggestions.md"
    if not os.path.exists(suggestions_file):
        print("❌ suggestions.md not found. Skipping comment.")
        return

    with open(suggestions_file, "r", encoding="utf-8") as f:
        body = f.read().strip()

    pr_number = get_pr_number()

    cmd = [
        "gh", "issue", "comment", pr_number,
        "--repo", REPO,
        "--body", body
    ]
    print(f"Posting feedback to PR #{pr_number}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Failed to post comment:", result.stderr)
    else:
        print("✅ Feedback posted successfully.")


if __name__ == "__main__":
    main()

