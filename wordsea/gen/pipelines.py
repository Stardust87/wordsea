import gc

import diffusers
import torch
from diffusers import DiffusionPipeline
from transformers import T5EncoderModel

from wordsea.constants import ImageModel


def flush():
    gc.collect()
    torch.cuda.empty_cache()


class LowMemoryFluxPipeline:
    def __init__(self):
        self.t5_encoder = T5EncoderModel.from_pretrained(
            "black-forest-labs/FLUX.1-schnell",
            subfolder="text_encoder_2",
            revision="refs/pr/7",
            torch_dtype=torch.bfloat16,
        )
        self.text_encoder = diffusers.DiffusionPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-schnell",
            text_encoder_2=self.t5_encoder,
            transformer=None,
            vae=None,
            revision="refs/pr/7",
        )
        self.pipeline = diffusers.DiffusionPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-schnell",
            torch_dtype=torch.bfloat16,
            revision="refs/pr/1",
            text_encoder_2=None,
            text_encoder=None,
        )
        self.pipeline.enable_model_cpu_offload()
        self.pipeline.set_progress_bar_config(disable=True)

    def encode_text(self, prompt: str) -> tuple[torch.Tensor, torch.Tensor]:
        (
            prompt_embeds,
            pooled_prompt_embeds,
            _,
        ) = self.text_encoder.encode_prompt(
            prompt=prompt, prompt_2=None, max_sequence_length=256
        )

        return prompt_embeds, pooled_prompt_embeds

    @torch.inference_mode()
    def inference(
        self,
        prompt,
        num_inference_steps=5,
        guidance_scale=0.0,
        num_images_per_prompt=1,
        width=768,
        height=768,
        generator=None,
    ):
        self.text_encoder.to("cuda")
        prompt_embeds, pooled_prompt_embeds = self.encode_text(prompt)
        self.text_encoder.to("cpu")
        flush()
        output = self.pipeline(
            prompt_embeds=prompt_embeds.bfloat16(),
            pooled_prompt_embeds=pooled_prompt_embeds.bfloat16(),
            width=width,
            height=height,
            guidance_scale=guidance_scale,
            num_images_per_prompt=num_images_per_prompt,
            num_inference_steps=num_inference_steps,
            generator=generator,
        )
        return output

    def __call__(self, *args, **kwargs):
        return self.inference(*args, **kwargs)


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
        case ImageModel.FLUX_SCHNELL:
            pipe = LowMemoryFluxPipeline()
        case _:
            raise ValueError(f"model not supported: {model}")

    if model != ImageModel.FLUX_SCHNELL:
        pipe.set_progress_bar_config(disable=True)
        pipe.to("cuda")

    return pipe
