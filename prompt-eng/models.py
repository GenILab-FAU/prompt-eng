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
