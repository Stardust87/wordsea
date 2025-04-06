import os
from enum import StrEnum
from pathlib import Path

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
LLAMACPP_URL = os.getenv("LLAMACPP_URL", "http://localhost:8080")

LOGS_PATH = Path(os.getenv("LOGS_PATH", "logs"))
LOGS_PATH.mkdir(parents=True, exist_ok=True)


class PromptModel(StrEnum):
    GEMMA3 = "gemma3"
    GEMMA2 = "gemma2"
    MISTRAL_NEMO = "mistral-nemo"


class ImageModel(StrEnum):
    FLUX_SCHNELL = "flux-schnell"
    PLAYGROUND = "playground"
