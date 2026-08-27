"""
BLUE PHANTOM :: STATUS SYNC
----------------------------
Pulls a live signal from the GitHub API (repo count, total stars) and
writes it into the LIVE STATUS UPLINK block in README.md, between the
BP:STATUS markers. Uses only the standard library — no pip installs
needed in the workflow.
"""

import json
import os
import random
import re
import urllib.request
from datetime import datetime, timezone

README_PATH = "README.md"
START_MARKER = "<!--BP:STATUS:START-->"
END_MARKER = "<!--BP:STATUS:END-->"

THREAT_LEVELS = [
    "🟢 GREEN — all systems nominal",
    "🔵 BLUE — monitoring active, no anomalies",
    "🟡 YELLOW — minor anomaly under review",
]


def get_username() -> str:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in repo:
        return repo.split("/", 1)[0]
    return os.environ.get("GITHUB_REPOSITORY_OWNER", "Salava-marquina")


def fetch_repos(username: str, token: str | None):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&type=owner"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "blue-phantom-status-sync")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_status_table() -> str:
    username = get_username()
    token = os.environ.get("GITHUB_TOKEN")

    try:
        repos = fetch_repos(username, token)
        repo_count = len(repos)
        star_count = sum(r.get("stargazers_count", 0) for r in repos)
        status = "ONLINE"
    except Exception:
        repo_count = "—"
        star_count = "—"
        status = "SIGNAL LOST (retry next cycle)"

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    threat_level = random.choice(THREAT_LEVELS)

    return (
        "| METRIC | VALUE |\n"
        "|:--|:--|\n"
        f"| 🛰️ STATUS | {status} |\n"
        f"| 🔐 REPOS MONITORED | {repo_count} |\n"
        f"| ⭐ SIGNALS DETECTED | {star_count} |\n"
        f"| 🌐 LAST UPLINK | {timestamp} |\n"
        f"| 🎯 THREAT LEVEL | {threat_level} |"
    )


def update_readme(new_block: str) -> None:
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    replacement = f"{START_MARKER}\n{new_block}\n{END_MARKER}"

    if not pattern.search(content):
        raise RuntimeError("BP:STATUS markers not found in README.md")

    content = pattern.sub(replacement, content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    table = build_status_table()
    update_readme(table)
    print("BLUE PHANTOM :: status uplink refreshed")
