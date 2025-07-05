import gc

import torch
from diffusers import DiffusionPipeline, FluxPipeline
from torchao.quantization import float8_dynamic_activation_float8_weight, quantize_

from wordsea.config import ImageModel


def flush() -> None:
    gc.collect()
    torch.cuda.empty_cache()


def get_fast_flux_pipeline(repo: str) -> FluxPipeline:
    pipe = FluxPipeline.from_pretrained(
        repo,
        torch_dtype=torch.bfloat16,
    )

    pipe.vae.to(memory_format=torch.channels_last)

    pipe.transformer.fuse_qkv_projections()
    pipe.vae.fuse_qkv_projections()

    quantize_(
        pipe.transformer,
        float8_dynamic_activation_float8_weight(),
    )

    pipe.to("cuda")

    config = torch._inductor.config
    config.conv_1x1_as_mm = True  # treat 1x1 convolutions as matrix muls
    # adjust autotuning algorithm
    config.coordinate_descent_tuning = True
    config.coordinate_descent_check_all_directions = True
    config.epilogue_fusion = False  # do not fuse pointwise ops into matmuls

    pipe.transformer = torch.compile(
        pipe.transformer, mode="reduce-overhead", fullgraph=True
    )
    pipe.vae.decode = torch.compile(
        pipe.vae.decode, mode="max-autotune", fullgraph=True
    )

    return pipe


def get_pipeline(model: ImageModel) -> DiffusionPipeline:
    match model:
        case ImageModel.PLAYGROUND:
            pipe = DiffusionPipeline.from_pretrained(
                "playgroundai/playground-v2.5-1024px-aesthetic",
                torch_dtype=torch.float16,
                use_safetensors=True,
                add_watermarker=False,
                variant="fp16",
            )
            pipe.to("cuda")
        case ImageModel.FLUX_SCHNELL:
            pipe = get_fast_flux_pipeline("black-forest-labs/FLUX.1-schnell")
        case ImageModel.FLUX_DEV:
            pipe = get_fast_flux_pipeline("black-forest-labs/FLUX.1-dev")
        case _:
            raise ValueError(f"model not supported: {model}")

    pipe.vae.enable_slicing()
    pipe.vae.enable_tiling()
    pipe.set_progress_bar_config(disable=True)
    pipe.to("cuda")

    return pipe
