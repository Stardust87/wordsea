import torch
from diffusers import DiffusionPipeline


def get_pipeline(model: str, compile: bool = False) -> DiffusionPipeline:
    torch.backends.cuda.matmul.allow_tf32 = True
    if compile:
        torch._inductor.config.conv_1x1_as_mm = True
        torch._inductor.config.coordinate_descent_tuning = True
        torch._inductor.config.epilogue_fusion = False
        torch._inductor.config.coordinate_descent_check_all_directions = True

    match model:
        case "playground":
            pipe = DiffusionPipeline.from_pretrained(
                "playgroundai/playground-v2-1024px-aesthetic",
                torch_dtype=torch.bfloat16,
                use_safetensors=True,
                add_watermarker=False,
                variant="fp16",
            )

            if compile:
                pipe.unet.to(memory_format=torch.channels_last)
                pipe.unet = torch.compile(
                    pipe.unet, mode="max-autotune", fullgraph=True
                )

            pipe.fuse_qkv_projections()

        case _:
            raise ValueError(f"model not supported: {model}")

    return pipe.to("cuda")
