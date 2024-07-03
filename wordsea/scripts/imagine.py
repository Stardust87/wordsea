import io
from typing import Optional

import click
import torch
from tqdm import tqdm

from wordsea.db import Image, Mnemonic, MongoDB
from wordsea.gen import get_pipeline, parse_input_words

PARAMETERS = {
    "playground": {
        "num_inference_steps": 50,
        "guidance_scale": 7.0,
    },
}


@click.command()
@click.argument("words", nargs=-1, type=str, required=False)
@click.option(
    "-m", "--model", type=str, default="playground", help="text2image model to use"
)
@click.option("-s", "--seed", type=int, help="random seed")
def imagine(words: Optional[list[str]], model: str, seed: int) -> None:
    """Generate image for words.

    WORDS: (list[str]): words to generate image for - every entity can be either a word or a path to a file with words separated by newlines
    """

    with MongoDB():
        if words:
            words = parse_input_words(words)
            incomplete_mnemonics = Mnemonic.objects(
                word__in=words, image__exists=False
            ).order_by("word")
        else:
            incomplete_mnemonics = Mnemonic.objects(image__exists=False).order_by(
                "word"
            )

        if not incomplete_mnemonics:
            click.echo("all images are already generated")
            return

        pipe = get_pipeline(model)

        generator = torch.Generator(device="cpu").manual_seed(
            torch.seed() if seed is None else seed
        )

        for mnemo in (pbar := tqdm(incomplete_mnemonics, desc="Generating images")):
            pbar.set_postfix_str(mnemo.word)
            mnemo.image_model = model

            image = pipe(  # type: ignore[operator]
                prompt=mnemo.prompt,
                generator=generator,
                num_images_per_prompt=1,
                height=1024,
                width=1024,
                **PARAMETERS[model],
            ).images[0]

            with io.BytesIO() as buf:
                image = image.resize((768, 768))
                image.save(buf, format="webp", optimize=True, quality=85)
                image_db = Image()
                image_db.data.put(buf.getvalue(), content_type="image/webp")
                mnemo.image = image_db

            mnemo.save()
