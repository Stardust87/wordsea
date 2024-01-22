import argparse
import json
from pathlib import Path

from wordsea import LOG_DIR, MINDICT_FILE
from wordsea.dictionary import find_words
from wordsea.gen import parse_input_words, render_definition


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find words in JSON dictionary cleaned using `wordsea clean`.",
    )
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="words to find - every entity can be either a word or a path to a file with words separated by newlines",
    )
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
        default=MINDICT_FILE,
    )
    args = parser.parse_args()

    words = parse_input_words(args.words)
    entries = find_words(words, path=Path(args.dictionary))
    if args.log:
        print(json.dumps(entries, indent=2))

    def_path = LOG_DIR / "definitions"
    def_path.mkdir(exist_ok=True)

    for word, entry in entries.items():
        html = render_definition(entry)
        with (def_path / f"{word}.html").open("w") as f:
            f.write(html)
