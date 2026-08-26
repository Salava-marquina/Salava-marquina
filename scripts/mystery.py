import random
import re
import pathlib

QUOTES = [
    "🔒 Mystery log: Compiling silence into syntax.",
    "🕶️ Location: unknown. Uptime: unknown. Curiosity: online.",
    "🛰️ Signal received. Decrypting intentions...",
    "🎭 The mask stays on. The commits don't.",
    "🐍 Somewhere, a script just ran itself again.",
    "🔍 Still watching. Still building.",
    "🧩 One more piece of the puzzle, pushed to main.",
]

README_PATH = pathlib.Path("README.md")
START = "<!--MYSTERY_START-->"
END = "<!--MYSTERY_END-->"


def main():
    text = README_PATH.read_text(encoding="utf-8")
    quote = random.choice(QUOTES)
    pattern = re.compile(f"{START}.*?{END}", re.DOTALL)

    if pattern.search(text) is None:
        raise SystemExit("Markers not found in README.md")

    replacement = f"{START}\n> {quote}\n{END}"
    new_text = pattern.sub(replacement, text)
    README_PATH.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    main()
