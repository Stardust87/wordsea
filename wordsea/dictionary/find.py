import argparse
import json
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

import wordsea

TEMPLATES_PATH = Path(wordsea.__file__).parent / "dictionary" / "templates"


def find_word(
    word: str, path: str = "/mnt/Sidra/wiktionary/raw-wiktextract-data-clean.json"
):
    matched = []
    with open(path, encoding="utf-8") as f:
        for line in tqdm(f):
            data = json.loads(line)
            if "translations" in data:
                del data["translations"]

            if data["word"] == word:
                matched.append(data)

    return matched


def render_definition(entries) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template("definition.html")
    return template.render(entries=entries)


def render_prompt(word: str, definition: str) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template("prompt.html")
    return template.render(word=word, definition=definition)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str)
    args = parser.parse_args()

    OUTPUT_PATH = Path("artifacts") / "words" / args.word
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    entries = find_word(
        args.word, path="/mnt/Sidra/wiktionary/raw-wiktextract-data-minimal.json"
    )
    html = render_definition(entries)
    with open(OUTPUT_PATH / "definition.html", "w") as f:
        f.write(html)

    html = re.sub(r"\s\s+", " ", html)
    html = html.replace("\n", "")
    prompt = render_prompt(args.word, html)

    with open(OUTPUT_PATH / "prompt.txt", "w") as f:
        f.write(prompt)
