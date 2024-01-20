import argparse
import json

import torch

from wordsea import LOG_DIR
from wordsea.dictionary.gen import get_pipeline, parse_input_words


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="words to find - every entity can be either a word or a path to a file with words separated by newlines",
    )
    parser.add_argument("-m", "--model", type=str, default="playground")
    parser.add_argument("-p", "--prompts", type=str, default="mixtral")
    parser.add_argument("-s", "--seed", type=int, default=42)
    parser.add_argument("-c", "--compile", action="store_true")

    args = parser.parse_args()
    images_path = LOG_DIR / "images" / f"{args.prompts}-{args.model}"
    images_path.mkdir(exist_ok=True, parents=True)

    words = parse_input_words(args.words)
    words_paths = [
        path
        for path in (LOG_DIR / "prompts" / args.prompts).glob("*.json")
        if path.stem in words
    ]
    words_paths = sorted(words_paths, key=lambda p: p.stem)

    pipe = get_pipeline(args.model, compile=args.compile)
    generator = torch.Generator(device="cpu").manual_seed(args.seed)
    for word_path in words_paths:
        with word_path.open() as f:
            answer = json.load(f)
            prompt = answer["prompt"]
            word = answer["word"]

        images = pipe(  # type: ignore[operator]
            prompt,
            num_inference_steps=30,
            generator=generator,
            guidance_scale=4.5,
            num_images_per_prompt=2,
        ).images

        for i, img in enumerate(images):
            img.save(images_path / f"{word}_{i}.png")
