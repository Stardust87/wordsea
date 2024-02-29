import torch
from diffusers import (
    DiffusionPipeline,
    EulerDiscreteScheduler,
    StableDiffusionXLPipeline,
    UNet2DConditionModel,
)
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from sfast.compilers.diffusion_pipeline_compiler import CompilationConfig, compile


def get_pipeline(model: str, optimize: bool = True) -> DiffusionPipeline:
    match model:
        case "playground":
            pipe = DiffusionPipeline.from_pretrained(
                "playgroundai/playground-v2.5-1024px-aesthetic",
                torch_dtype=torch.float16,
                use_safetensors=True,
                add_watermarker=False,
                variant="fp16",
            )

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
    pipe.to("cuda")

    if optimize:
        config = CompilationConfig.Default()
        config.enable_xformers = True
        config.enable_triton = True
        config.enable_cuda_graph = True
        pipe = compile(pipe, config)

    return pipe
