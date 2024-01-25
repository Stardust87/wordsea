import argparse
import io
import logging

import torch
from tqdm import tqdm

from wordsea.db import Image, Mnemonic, MongoDB
from wordsea.gen import get_pipeline, parse_input_words


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "words",
        nargs="+",
        type=str,
        help="words to find - every entity can be either a word or a path to a file with words separated by newlines",
    )

    parser.add_argument("-m", "--model", type=str, default="playground")
    parser.add_argument("-s", "--seed", type=int, default=42)

    args = parser.parse_args()
    words = parse_input_words(args.words)

    with MongoDB():
        incomplete_mnemonics = Mnemonic.objects(
            word__in=words, images__size=0
        ).order_by("word")

        if not incomplete_mnemonics:
            logging.info("all images are already generated")

        pipe = get_pipeline(args.model)
        generator = torch.Generator(device="cpu").manual_seed(args.seed)

        for mnemo in (pbar := tqdm(incomplete_mnemonics, desc="Generating images")):
            pbar.set_postfix_str(mnemo.word)
            mnemo.image_model = args.model

            output = pipe(  # type: ignore[operator]
                mnemo.prompt,
                num_inference_steps=30,
                generator=generator,
                guidance_scale=4.5,
                num_images_per_prompt=2,
            )

            for image in output.images:
                with io.BytesIO() as buf:
                    image.save(buf, format="JPEG")
                    image_db = Image()
                    image_db.data.put(buf.getvalue(), content_type="image/jpeg")
                    mnemo.images.append(image_db)

            mnemo.save()
