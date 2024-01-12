import argparse

import torch
from diffusers import (
    DiffusionPipeline,
    StableDiffusionXLPipeline,
    PixArtAlphaPipeline,
    ConsistencyDecoderVAE,
)


def get_pipeline(model: str):
    if model == "sdxl":
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.bfloat16,
            safety_checker=None,
        ).to("cuda")
    elif model == "pixart":
        pipe = PixArtAlphaPipeline.from_pretrained(
            "PixArt-alpha/PixArt-XL-2-512x512",
            torch_dtype=torch.bfloat16,
        )
        pipe.vae = ConsistencyDecoderVAE.from_pretrained(
            "openai/consistency-decoder", torch_dtype=torch.bfloat16
        )
        pipe = pipe.to("cuda")
    elif model == "playground":
        pipe = DiffusionPipeline.from_pretrained(
            "playgroundai/playground-v2-1024px-aesthetic",
            torch_dtype=torch.float16,
            use_safetensors=True,
            add_watermarker=False,
            variant="fp16",
        )
        pipe.to("cuda")

    else:
        raise ValueError(f"model not supported: {model}")

    return pipe


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str)
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default="pirate ship trapped in a cosmic maelstrom nebula",
    )
    parser.add_argument("-n", "--negative-prompt", type=str, default=None)
    parser.add_argument("-m", "--model", type=str, default="pixart")

    args = parser.parse_args()

    pipe = get_pipeline(args.model)

    generator = torch.Generator(device="cpu").manual_seed(1)
    images = pipe(
        args.prompt,
        negative_prompt=args.negative_prompt,
        num_inference_steps=60,
        generator=generator,
        guidance_scale=3.0,
        num_images_per_prompt=2,
    ).images

    for i, img in enumerate(images):
        img.save(f"artifacts/words/{args.word}/{args.model}_{i}.png")
