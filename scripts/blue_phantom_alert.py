"""
BLUE PHANTOM :: SENTINEL WATCH
-------------------------------
Reads the outcome of the Status Uplink workflow run (passed in via the
WORKFLOW_CONCLUSION env var) and appends a line to the INTEL LOG in
README.md. Keeps only the most recent 5 entries.
"""

import os
import re
from datetime import datetime, timezone

README_PATH = "README.md"
START_MARKER = "<!--BP:ALERTLOG:START-->"
END_MARKER = "<!--BP:ALERTLOG:END-->"
MAX_ENTRIES = 5

CONCLUSION_LINES = {
    "success": "🟢 OPERATION SUCCESSFUL — systems secured",
    "failure": "🔴 SECURITY ALERT — anomaly detected, investigate immediately",
    "cancelled": "🟡 OPERATION ABORTED — mission cancelled",
    "timed_out": "🟠 OPERATION TIMED OUT — uplink unresponsive",
}


def build_entry() -> str:
    conclusion = os.environ.get("WORKFLOW_CONCLUSION", "unknown")
    label = CONCLUSION_LINES.get(conclusion, f"⚪ OPERATION CONCLUDED — status: {conclusion}")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"- `{timestamp}` — {label}"


def update_readme(new_entry: str) -> None:
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r"(.*?)" + re.escape(END_MARKER),
        re.DOTALL,
    )
    match = pattern.search(content)
    if not match:
        raise RuntimeError("BP:ALERTLOG markers not found in README.md")

    existing_block = match.group(1).strip()
    existing_lines = [
        line for line in existing_block.splitlines()
        if line.strip().startswith("- `")
    ]

    updated_lines = [new_entry] + existing_lines
    updated_lines = updated_lines[:MAX_ENTRIES]

    replacement = f"{START_MARKER}\n" + "\n".join(updated_lines) + f"\n{END_MARKER}"
    content = pattern.sub(replacement, content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    entry = build_entry()
    update_readme(entry)
    print("BLUE PHANTOM :: intel log updated")
