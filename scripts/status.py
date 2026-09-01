import random
import re
import pathlib
from datetime import datetime, timezone

FOCUS_LINES = [
    "Compiling silence into syntax.",
    "Mapping networks, one packet at a time.",
    "Some builds stay classified — for now.",
    "Reverse-engineering my own bad habits.",
    "Status: heads down, low profile.",
    "Progress is quiet. Commits aren't.",
]

README_PATH = pathlib.Path("README.md")


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(f"{start}.*?{end}", re.DOTALL)
    if pattern.search(text) is None:
        raise SystemExit(f"Markers {start} / {end} not found in README.md")
    return pattern.sub(f"{start}\n{replacement}\n{end}", text)


def main():
    text = README_PATH.read_text(encoding="utf-8")

    focus = random.choice(FOCUS_LINES)
    text = replace_between(
        text, "<!--FOCUS_START-->", "<!--FOCUS_END-->",
        f"**Current focus:** _{focus}_",
    )

    synced = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text = replace_between(
        text, "<!--SYNCED_START-->", "<!--SYNCED_END-->", synced,
    )

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    stats_img = (
        f'<img src="https://streak-stats.demolab.com/?user=Salava-marquina'
        f'&theme=midnight-purple&hide_border=false'
        f'&cache_bust={today}" alt="Streak stats" />'
    )
    text = replace_between(
        text, "<!--STATS_START-->", "<!--STATS_END-->", stats_img,
    )

    README_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()