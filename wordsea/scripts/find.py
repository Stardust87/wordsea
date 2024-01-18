import argparse
import json
from pathlib import Path

from wordsea.dictionary import find_words
from wordsea.dictionary.gen import render_definition, render_prompt


def main():
    parser = argparse.ArgumentParser(
        description="Find words in JSON dictionary cleaned using `wordsea clean`.",
    )
    parser.add_argument("words", nargs="+", type=str, help="words to find")
    parser.add_argument("-s", "--save", type=str, help="path to save found entries")
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="log found entries in console",
    )

    parser.add_argument(
        "-d",
        "--dictionary",
        type=str,
        help="dictionary path",
        default="/mnt/Sidra/wiktionary/raw-wiktextract-data-minimal.json",
    )
    args = parser.parse_args()

    entries = find_words(args.words, path=Path(args.dictionary))
    if args.log:
        print(json.dumps(entries, indent=2))

    if args.save:
        OUTPUT_PATH = Path(args.save)
        DEF_PATH = OUTPUT_PATH / "definitions"
        PROMPTS_PATH = OUTPUT_PATH / "prompts"
        DEF_PATH.mkdir(parents=True, exist_ok=True)
        PROMPTS_PATH.mkdir(parents=True, exist_ok=True)

        for word, entry in entries.items():
            html = render_definition(entry)
            with open(DEF_PATH / f"{word}.html", "w") as f:
                f.write(html)

            prompt = render_prompt(word, html)
            with open(PROMPTS_PATH / f"{word}.md", "w") as f:
                f.write(prompt)
