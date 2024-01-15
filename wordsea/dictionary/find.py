import argparse
import json
import re
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

import wordsea
import logging
import argparse
import json
import re
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

import wordsea

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.WARNING,
)

TEMPLATES_PATH = Path(wordsea.__file__).parent / "dictionary" / "templates"


def find_words(
    words: list[str],
    path: Path,
):
    info_path = path.parent / (path.stem + "-info.csv")
    info = pd.read_csv(info_path)

    words_info = info[info["word"].isin(words)]
    not_found = set(words) - set(words_info.word.unique().tolist())
    if not_found:
        logging.warning(f"The following words were not found: {', '.join(not_found)}")

    line_indices = sorted(words_info.id.tolist())

    matched = []
    with open(path, encoding="utf-8") as f:
        for idx, line in enumerate(tqdm(f)):
            if idx == line_indices[0]:
                matched.append(line)
                line_indices.pop(0)
                if not line_indices:
                    break

    words_info.loc[:, ["data"]] = matched
    found_words = {
        word: [json.loads(line) for line in group.data]
        for word, group in words_info.groupby("word")
    }

    return found_words


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
    parser.add_argument("words", nargs="+", type=str, help="words to find")
    parser.add_argument(
        "-o", "--output", type=str, help="output path", default="artifacts"
    )
    parser.add_argument(
        "-d",
        "--dictionary",
        type=str,
        help="dictionary path",
        default="/mnt/Sidra/wiktionary/debug-wiktextract-minimal.json",
    )
    args = parser.parse_args()

    OUTPUT_PATH = Path(args.output)
    DEF_PATH = OUTPUT_PATH / "definitions"
    PROMPTS_PATH = OUTPUT_PATH / "prompts"
    DEF_PATH.mkdir(parents=True, exist_ok=True)
    PROMPTS_PATH.mkdir(parents=True, exist_ok=True)

    entries = find_words(args.words, path=Path(args.dictionary))

    for word, entry in entries.items():
        html = render_definition(entry)
        with open(DEF_PATH / f"{word}.html", "w") as f:
            f.write(html)

        html = re.sub(r"\s\s+", " ", html)
        html = html.replace("\n", "")
        prompt = render_prompt(word, html)

        with open(PROMPTS_PATH / f"{word}.md", "w") as f:
            f.write(prompt)
