import torch
from diffusers import (
    DiffusionPipeline,
    EulerDiscreteScheduler,
    StableDiffusionXLPipeline,
    UNet2DConditionModel,
)
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file


def get_pipeline(model: str) -> DiffusionPipeline:
    torch.backends.cuda.matmul.allow_tf32 = True

    match model:
        case "playground":
            pipe = DiffusionPipeline.from_pretrained(
                "playgroundai/playground-v2.5-1024px-aesthetic",
                torch_dtype=torch.bfloat16,
                use_safetensors=True,
                add_watermarker=False,
                variant="fp16",
            )

            pipe.fuse_qkv_projections()

        case "lightning":
            base = "stabilityai/stable-diffusion-xl-base-1.0"
            repo = "ByteDance/SDXL-Lightning"
            ckpt = "sdxl_lightning_8step_unet.safetensors"

            unet = UNet2DConditionModel.from_config(
                UNet2DConditionModel.load_config(base, subfolder="unet")
            ).to("cuda", torch.bfloat16)
            unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device="cuda"))
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
