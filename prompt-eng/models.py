from dataclasses import dataclass

# need to choose common features here between ollama API
# and openwebUI API

# ollama schema example 
# {
#   "models": [
#     {
#       "name": "codellama:13b",
#       "modified_at": "2023-11-04T14:56:49.277302595-07:00",
#       "size": 7365960935,
#       "digest": "9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
#       "details": {
#         "format": "gguf",
#         "family": "llama",
#         "families": null,
#         "parameter_size": "13B",
#         "quantization_level": "Q4_0"
#       }
#     }
# ]
# }

# openwebui schema example
# {
#   "data": [
#     {
#       "id": "llava:latest",
#       "name": "llava:latest",
#       "object": "model",
#       "created": 1739075156,
#       "owned_by": "ollama",
#       "ollama": {
#         "name": "llava:latest",
#         "model": "llava:latest",
#         "modified_at": "2025-01-29T02:25:19.238242652Z",
#         "size": 4733363377,
#         "digest": "8dd30f6b0cb19f555f2c7a7ebda861449ea2cc76bf1f44e262931f45fc81d081",
#         "details": {
#           "parent_model": "",
#           "format": "gguf",
#           "family": "llama",
#           "families": [
#             "llama",
#             "clip"
#           ],
#           "parameter_size": "7B",
#           "quantization_level": "Q4_0"
#         },
#         "urls": [
#           0
#         ]
#       }
#     }
#   ]
# }
@dataclass
class AIModel():
    name: str
    parameter_size: str

# for a description of what these do
# https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
# used semanticly meaningful names for things when possible
@dataclass
class ModelOptions():
    max_tokens: int | None = None
    temperature: float | None = None
    top_k: int | None = None
    top_p: float | None = None
    context_window_size: int | None = None
    seed: int | None = None

    def validate(self):
        if self.temperature:
            if not isinstance(self.temperature, float):
                raise TypeError(f"temperature must be of type float not type {self.temperature}.")
            if self.temperature < 0 or self.temperature > 1:
                raise ValueError(f"temperature must be between 0 and 1, {self.temperature} is not a valid value")
        
        if self.max_tokens:
            if not isinstance(self.max_tokens, int):
                raise TypeError(f"max_tokens must be of type int not type {self.max_tokens}.")
        
        if self.top_k:
            if not isinstance(self.top_k, int):
                raise TypeError(f"top_k must be of type int not type {self.top_k}.")
            if self.top_k < 0 or self.top_k > 100:
                raise ValueError(f"top_k must be between 0 and 100, {self.top_k} is not a valid value")
        
        if self.top_p:
            if not isinstance(self.top_p, float):
                raise TypeError(f"top_p must be of type float not type {self.top_p}.")
            if self.top_p < 0 or self.top_p > 1:
                raise ValueError(f"top_p must be between 0 and 1, {self.top_p} is not a valid value")
        
        if self.context_window_size:
            if not isinstance(self.context_window_size, int):
                raise TypeError(f"context_window_size must be of type int not type {self.context_window_size}.")
        
        if self.seed:
            if not isinstance(self.seed, int):
                raise TypeError(f"seed must be of type int not type {self.seed}.")
            








            

