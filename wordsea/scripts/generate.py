import argparse
import json

from tqdm import tqdm

from wordsea import LLAMACPP_URL, LOG_DIR
from wordsea.dictionary import find_words
from wordsea.gen import LlamaCppAPI, parse_input_words, render_definition, render_prompt


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
        "-u", "--update", action="store_true", help="whether to update existing prompts"
    )
    args = parser.parse_args()
    prompts_path = LOG_DIR / "prompts" / args.model
    prompts_path.mkdir(exist_ok=True, parents=True)

    words = parse_input_words(args.words)
    if not args.update:
        words = [word for word in words if not (prompts_path / f"{word}.json").exists()]
    if not words:
        print("All prompts are already generated")
        return

    api = LlamaCppAPI(url=LLAMACPP_URL, model=args.model)
    if not api.health():
        raise RuntimeError("API is not healthy")

    entries = find_words(words)

    pbar = tqdm(entries.items(), total=len(entries), desc="Generating image prompts")
    for word, entry in pbar:
        pbar.set_postfix_str(word)
        html = render_definition(entry)
        prompt = render_prompt(word, html)

        answer = api.generate(word, prompt)
        if answer is None:
            continue

        with (prompts_path / f"{word}.json").open("w") as f:
            f.write(json.dumps(answer, indent=2, ensure_ascii=False))
