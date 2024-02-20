import io

import click
import torch
from tqdm import tqdm

from wordsea.db import Image, Mnemonic, MongoDB
from wordsea.gen import get_pipeline, parse_input_words


@click.command()
@click.argument("words", nargs=-1, type=str, required=True)
@click.option(
    "-m", "--model", type=str, default="playground", help="text2image model to use"
)
@click.option("-s", "--seed", type=int, help="random seed")
def imagine(words: list[str], model: str, seed: int) -> None:
    """Generate images for words.

    WORDS: (list[str]): words to generate images for - every entity can be either a word or a path to a file with words separated by newlines
    """

    words = parse_input_words(words)

    with MongoDB():
        incomplete_mnemonics = Mnemonic.objects(
            word__in=words, images__size=0
        ).order_by("word")

        if not incomplete_mnemonics:
            click.echo("all images are already generated")

        pipe = get_pipeline(model)

        generator = torch.Generator(device="cpu").manual_seed(
            torch.seed() if seed is None else seed
        )

        for mnemo in (pbar := tqdm(incomplete_mnemonics, desc="Generating images")):
            pbar.set_postfix_str(mnemo.word)
            mnemo.image_model = model

            output = pipe(  # type: ignore[operator]
                prompt=mnemo.prompt,
                num_inference_steps=20,
                generator=generator,
                guidance_scale=4.5,
                num_images_per_prompt=1,
                height=1024,
                width=1024,
            )

            for image in output.images:
                with io.BytesIO() as buf:
                    image.save(buf, format="webp", optimize=True, quality=85)
                    image_db = Image()
                    image_db.data.put(buf.getvalue(), content_type="image/webp")
                    mnemo.images.append(image_db)

            mnemo.save()
