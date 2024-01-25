import torch
from diffusers import DiffusionPipeline


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

        case _:
            raise ValueError(f"model not supported: {model}")

    pipe.set_progress_bar_config(disable=True)
    return pipe.to("cuda")
