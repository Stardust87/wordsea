from typing import Any

import torch
from diffusers import (  # type: ignore[attr-defined]
    DiffusionPipeline,
    EulerDiscreteScheduler,
    StableCascadeDecoderPipeline,
    StableCascadePriorPipeline,
    StableDiffusionXLPipeline,
    UNet2DConditionModel,
)
from huggingface_hub import hf_hub_download


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

        case "lightning":
            base = "stabilityai/stable-diffusion-xl-base-1.0"
            repo = "ByteDance/SDXL-Lightning"
            ckpt = "sdxl_lightning_4step_unet.pth"

            unet = UNet2DConditionModel.from_config(
                UNet2DConditionModel.load_config(base, subfolder="unet")
            ).to("cuda", torch.bfloat16)
            unet.load_state_dict(
                torch.load(hf_hub_download(repo, ckpt), map_location="cuda")
            )
            pipe = StableDiffusionXLPipeline.from_pretrained(
                base, unet=unet, torch_dtype=torch.bfloat16, variant="fp16"
            )

            pipe.scheduler = EulerDiscreteScheduler.from_config(
                pipe.scheduler.config, timestep_spacing="trailing"
            )

        case _:
            raise ValueError(f"model not supported: {model}")

    pipe.set_progress_bar_config(disable=True)
    return pipe.to("cuda")
