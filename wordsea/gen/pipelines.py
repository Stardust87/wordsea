import torch
from diffusers import DiffusionPipeline
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
