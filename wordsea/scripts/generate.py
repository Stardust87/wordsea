import argparse
import json
from pathlib import Path

from tqdm import tqdm

from wordsea import LLAMACPP_URL, LOG_DIR, MINDICT_FILE
from wordsea.dictionary import find_words
from wordsea.dictionary.gen import (
    LlamaCppAPI,
    parse_input_words,
    render_definition,
    render_prompt,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="words to find - every entity can be either a word or a path to a file with words separated by newlines",
    )
    parser.add_argument("-m", "--model", type=str, default="mixtral")
    parser.add_argument(
        "-d",
        "--dictionary",
        type=str,
        help="dictionary path",
        default=MINDICT_FILE,
    )
    args = parser.parse_args()
    prompts_path = LOG_DIR / "prompts" / args.model
    prompts_path.mkdir(exist_ok=True)

    api = LlamaCppAPI(url=LLAMACPP_URL, model=args.model)
    if not api.health():
        raise RuntimeError("API is not healthy")

    words = parse_input_words(args.words)
    entries = find_words(words, path=Path(args.dictionary), silent=True)

    for word, entry in tqdm(
        entries.items(), total=len(entries), desc="Generating image prompts"
    ):
        html = render_definition(entry)
        prompt = render_prompt(word, html)

        answer = api.generate(word, prompt)
        if answer is None:
            continue

        with (prompts_path / f"{word}.json").open("w") as f:
            f.write(json.dumps(answer, indent=2))
