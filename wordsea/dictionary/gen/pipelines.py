import torch
from diffusers import (
    ConsistencyDecoderVAE,
    DiffusionPipeline,
    DPMSolverMultistepScheduler,
    PixArtAlphaPipeline,
    StableDiffusionXLPipeline,
)


def get_pipeline(model: str) -> DiffusionPipeline:
    match model:
        case "sdxl":
            pipe = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.bfloat16,
                safety_checker=None,
            )

        case "pixart":
            pipe = PixArtAlphaPipeline.from_pretrained(
                "PixArt-alpha/PixArt-XL-2-512x512",
                torch_dtype=torch.bfloat16,
            )
            pipe.vae = ConsistencyDecoderVAE.from_pretrained(
                "openai/consistency-decoder", torch_dtype=torch.bfloat16
            )

        case "playground":
            pipe = DiffusionPipeline.from_pretrained(
                "playgroundai/playground-v2-1024px-aesthetic",
                torch_dtype=torch.bfloat16,
                use_safetensors=True,
                add_watermarker=False,
                variant="fp16",
            )

        case _:
            raise ValueError(f"model not supported: {model}")

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    return pipe.to("cuda")
