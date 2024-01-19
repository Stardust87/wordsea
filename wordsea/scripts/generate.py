import argparse
import json
import logging
from pathlib import Path

from tqdm import tqdm

from wordsea import LLAMACPP_URL, LOG_DIR, MINDICT_FILE
from wordsea.dictionary import find_words
from wordsea.dictionary.gen import (
    LlamaCppAPI,
    is_response_correct,
    parse_input_words,
    render_definition,
    render_prompt,
)

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.ERROR,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="words to find - every entity can be either a word or a path to a file with words separated by newlines",
    )
    parser.add_argument(
        "-d",
        "--dictionary",
        type=str,
        help="dictionary path",
        default=MINDICT_FILE,
    )
    args = parser.parse_args()

    api = LlamaCppAPI(url=LLAMACPP_URL)
    if not api.health():
        raise RuntimeError("API is not healthy")

    words = parse_input_words(args.words)
    entries = find_words(words, path=Path(args.dictionary), silent=True)

    for word, entry in tqdm(
        entries.items(), total=len(entries), desc="Generating image prompts"
    ):
        html = render_definition(entry)
        prompt = render_prompt(word, html)
        res = api.generate(prompt)
        answer = json.loads(res["content"])

        if not is_response_correct(answer):
            logging.error(
                f"For following word: `{word}` response was not correct and will be skipped. Response: `{answer}`"
            )
            continue

        answer["word"] = word

        prompts_path = LOG_DIR / "prompts"
        prompts_path.mkdir(exist_ok=True)

        with (prompts_path / f"{word}.json").open("w") as f:
            f.write(json.dumps(answer, indent=2))
