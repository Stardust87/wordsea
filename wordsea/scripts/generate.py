import argparse
import json
from pathlib import Path

from tqdm import tqdm

from wordsea.dictionary import find_words
from wordsea.dictionary.gen import render_definition, render_prompt, LlamaCppAPI


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("words", nargs="+", type=str, help="words to find")
    # TODO: load from file
    parser.add_argument(
        "-d",
        "--dictionary",
        type=str,
        help="dictionary path",
        default="/mnt/Sidra/wiktionary/raw-wiktextract-data-minimal.json",
    )
    args = parser.parse_args()

    api = LlamaCppAPI(url="http://localhost:8080")
    if not api.health():
        raise RuntimeError("API is not healthy")

    entries = find_words(args.words, path=Path(args.dictionary), silent=True)
    # print(entries)

    for word, entry in tqdm(
        entries.items(), total=len(entries), desc="Generating image prompts"
    ):
        html = render_definition(entry)
        prompt = render_prompt(word, html)
        res = api.generate(prompt)

        answer = json.loads(res["content"])
        answer["word"] = word

        with open(f"artifacts/logs/{word}.json", "w") as f:
            f.write(json.dumps(answer, indent=2))

        # TODO: check if answer has correct keys


if __name__ == "__main__":
    main()
