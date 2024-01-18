from dataclasses import asdict, dataclass, field
from typing import Any

import requests

JSON_GRAMMAR = r"""root   ::= object
value  ::= object | array | string | number | ("true" | "false" | "null") ws

object ::=
"{" ws (
            string ":" ws value
    ("," ws string ":" ws value)*
)? "}" ws

array  ::=
"[" ws (
            value
    ("," ws value)*
)? "]" ws

string ::=
"\"" (
    [^"\\] |
    "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]) # escapes
)* "\"" ws

number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)? ws

# Optional space: by convention, applied in this grammar after literal chars when allowed
ws ::= ([ \t\n] ws)?"""


@dataclass
class LLMParams:
    n_predict: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    top_k: int = 40
    min_p: float = 0.02
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repeat_penalty: float = 1.0
    penalize_nl: bool = False
    stop: list[str] = field(default_factory=lambda: ["</s>"])


MixtralParams = LLMParams()


class LlamaCppAPI:
    def __init__(self, url: str) -> None:
        self.base_url = url

    def health(self) -> bool:
        res = requests.get(f"{self.base_url}/health").json()
        return res["status"] == "ok"

    def generate(self, prompt: str) -> dict[str, Any]:
        return requests.post(
            f"{self.base_url}/completion",
            json={"prompt": prompt, "grammar": JSON_GRAMMAR, **asdict(MixtralParams)},
        ).json()
