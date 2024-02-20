from typing import Any

import torch
from diffusers import (  # type: ignore[attr-defined]
    DiffusionPipeline,
    StableCascadeDecoderPipeline,
    StableCascadePriorPipeline,
)


class StableCascadePipeline:
    def __init__(self) -> None:
        self.prior = StableCascadePriorPipeline.from_pretrained(
            "stabilityai/stable-cascade-prior", torch_dtype=torch.bfloat16
        )
        self.decoder = StableCascadeDecoderPipeline.from_pretrained(
            "stabilityai/stable-cascade", torch_dtype=torch.float16
        )

    def set_progress_bar_config(self, disable: bool) -> None:
        self.prior.set_progress_bar_config(disable=disable)
        self.decoder.set_progress_bar_config(disable=disable)

    def to(self, device: str) -> "StableCascadePipeline":
        self.prior.to(device)
        self.decoder.to(device)
        return self

    def __call__(self, **kwargs: dict[str, Any]) -> torch.Tensor:
        prior_output = self.prior(**kwargs)
        return self.decoder(
            prior_output.image_embeddings.half(),
            prompt=kwargs["prompt"],
            negative_prompt=kwargs.get("negative_prompt", None),
            output_type="pil",
            num_inference_steps=10,
            guidance_scale=0.0,
        )


def get_pipeline(model: str) -> DiffusionPipeline:
    torch.backends.cuda.matmul.allow_tf32 = True

    match model:
        case "playground":
            pipe = DiffusionPipeline.from_pretrained(
                "playgroundai/playground-v2-1024px-aesthetic",
                torch_dtype=torch.bfloat16,
                use_safetensors=True,
                add_watermarker=False,
                variant="fp16",
            )

            pipe.fuse_qkv_projections()

        case "cascade":
            pipe = StableCascadePipeline()

        case _:
            raise ValueError(f"model not supported: {model}")

    pipe.set_progress_bar_config(disable=True)
    return pipe.to("cuda")
