import argparse
import json
from pathlib import Path

import torch

from wordsea.dictionary.gen import get_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logs-path", type=str, default="artifacts/logs")
    parser.add_argument("-m", "--model", type=str, default="pixart")
    parser.add_argument("-s", "--seed", type=int, default=42)

    args = parser.parse_args()
    output_path = Path(f"artifacts/images/{args.model}")
    output_path.mkdir(exist_ok=True, parents=True)

    words_paths = Path(args.logs_path).glob("*.json")
    words_paths = sorted(words_paths, key=lambda p: p.stem)

    pipe = get_pipeline(args.model)
    generator = torch.Generator(device="cpu").manual_seed(args.seed)
    for word_path in words_paths:
        with open(word_path) as f:
            answer = json.load(f)
            prompt = answer["prompt"]
            word = answer["word"]

        images = pipe(
            prompt,
            num_inference_steps=45,
            generator=generator,
            guidance_scale=4.5,
            num_images_per_prompt=2,
            height=1024,
            width=1024,
        ).images

        for i, img in enumerate(images):
            img.save(output_path / f"{word}_{i}.png")


if __name__ == "__main__":
    main()
