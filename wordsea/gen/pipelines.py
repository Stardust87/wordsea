import gc

import torch
from diffusers import AutoModel, DiffusionPipeline, FluxPipeline
from diffusers import BitsAndBytesConfig as DiffusersBitsAndBytesConfig
from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig
from transformers import T5EncoderModel

from wordsea.config import ImageModel


def flush() -> None:
    gc.collect()
    torch.cuda.empty_cache()


def get_flux_8bit_pipeline(repo: str) -> FluxPipeline:
    torch._dynamo.config.capture_dynamic_output_shape_ops = True

    text_encoder_2_8bit = T5EncoderModel.from_pretrained(
        repo,
        subfolder="text_encoder_2",
        quantization_config=TransformersBitsAndBytesConfig(load_in_8bit=True),
        torch_dtype=torch.bfloat16,
    )

    transformer_8bit = AutoModel.from_pretrained(
        repo,
        subfolder="transformer",
        quantization_config=DiffusersBitsAndBytesConfig(load_in_8bit=True),
        torch_dtype=torch.bfloat16,
    )

    # transformer_8bit.compile(mode="max-autotune", fullgraph=True)

    pipe = FluxPipeline.from_pretrained(
        repo,
        transformer=transformer_8bit,
        text_encoder_2=text_encoder_2_8bit,
        torch_dtype=torch.bfloat16,
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
            pipe = get_flux_8bit_pipeline("black-forest-labs/FLUX.1-schnell")
        case ImageModel.FLUX_DEV:
            pipe = get_flux_8bit_pipeline("black-forest-labs/FLUX.1-dev")
        case _:
            raise ValueError(f"model not supported: {model}")

    pipe.vae.enable_slicing()
    pipe.vae.enable_tiling()
    pipe.set_progress_bar_config(disable=True)
    pipe.to("cuda")

    return pipe
