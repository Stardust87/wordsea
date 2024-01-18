import argparse
import json
import logging
from pathlib import Path

from tqdm import tqdm

from wordsea.dictionary import find_words
from wordsea.dictionary.gen import (
    LlamaCppAPI,
    correct_response,
    render_definition,
    render_prompt,
)

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.ERROR,
)


def main():
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
        default="/mnt/Sidra/wiktionary/raw-wiktextract-data-minimal.json",
    )
    args = parser.parse_args()

    # api = LlamaCppAPI(url="http://localhost:8080")
    api = LlamaCppAPI(url="http://pop-os.local:8080")
    if not api.health():
        raise RuntimeError("API is not healthy")

    complete_words_list = []
    for word in args.words:
        if Path(word).exists():
            with open(word) as f:
                complete_words_list.extend(f.read().splitlines())
        else:
            complete_words_list.append(word)

    complete_words_list = list(set(complete_words_list))
    entries = find_words(complete_words_list, path=Path(args.dictionary), silent=True)

    for word, entry in tqdm(
        entries.items(), total=len(entries), desc="Generating image prompts"
    ):
        html = render_definition(entry)
        prompt = render_prompt(word, html)
        res = api.generate(prompt)
        answer = json.loads(res["content"])

        is_correct = correct_response(answer)
        if not is_correct:
            logging.error(
                f"For following word: `{word}` response was not correct and will be skipped. Response: `{answer}`"
            )
            continue

        answer["word"] = word

        LOGS_DIR = Path("artifacts/logs")
        LOGS_DIR.mkdir(exist_ok=True, parents=True)

        with open(LOGS_DIR / f"{word}.json", "w") as f:
            f.write(json.dumps(answer, indent=2))


if __name__ == "__main__":
    main()
