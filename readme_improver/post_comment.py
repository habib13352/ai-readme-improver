"""Utilities for posting README improvement suggestions to pull requests."""

import os
import sys
import subprocess
import json

GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")


def get_pr_number() -> str:
    """Extract the pull request number from the GitHub event payload."""
    if not GITHUB_EVENT_PATH or not os.path.exists(GITHUB_EVENT_PATH):
        print("❌ GITHUB_EVENT_PATH not set or file missing.")
        sys.exit(1)

    with open(GITHUB_EVENT_PATH, "r", encoding="utf-8") as f:
        payload = json.load(f)
    pr = payload.get("pull_request")
    if not pr:
        print("❌ Not triggered by a pull request. Exiting.")
        sys.exit(1)
    return str(pr.get("number"))


def main():
    """Post README improvement suggestions as a PR comment."""

    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN not set. Cannot post comment.")
        return

    suggestions_file = "suggestions.md"
    if not os.path.exists(suggestions_file):
        print("❌ suggestions.md not found. Skipping comment.")
        return

    with open(suggestions_file, "r", encoding="utf-8") as f:
        body = f.read().strip()

    pr_number = get_pr_number()
    if not REPO:
        print("❌ GITHUB_REPOSITORY not set.")
        return

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
