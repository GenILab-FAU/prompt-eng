import requests
from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime
from models import AIModel

# interface for chatbot clients
class ChatbotClient(ABC):
    @abstractmethod
    def get_models(self) -> List[AIModel]:
        pass

    @abstractmethod
    def chat(self, message: str, model: AIModel, options: Dict[str, Any]) -> Tuple[int, str]:
        pass

# instead of trying to make all the decisions in the client, we can use a factory to create the appropriate client based on the configuration.
# this reduces the complexity of the client and makes it easier to add new clients in the future.
class ChatbotClientFactory():
    @staticmethod
    def create_client(config: Dict[str,str]) -> ChatbotClient:
        host = config["chatbot_api_host"]
        # TODO : We'll simply decide using the FAU host, and consider anything else to be
        # ollama client for now.
        if host == "chat.hpc.fau.edu":
            return OpenWebUIClient(host=host, bearer=config["bearer"])
        # TODO : Implment Ollama client.
        else:
            raise ValueError(f"Unknown host: {host}")

        
class OpenWebUIClient(ChatbotClient):
    def __init__(self, host: str, bearer: str):
        self.host = host
        self.bearer = bearer

    def _parse_options(self, options: Dict[str, Any]) -> Dict[str, Any]:
        implemented_options = {}
        for key, value in options.items():
            if key in {"temperature", "max_tokens"}:
                implemented_options[key] = value
        
        return implemented_options

    def _get_models(self) -> Dict[Any, Any]:
        url = f"https://{self.host}/api/models"
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_models(self) -> List[AIModel]:
        data = self._get_models()
        models = []
        for model_info in data["data"]:
            model = AIModel(
                name=model_info["name"],
                parameter_size=model_info["ollama"]["details"]["parameter_size"],
            )
            models.append(model)
        return models

    def chat(self, message: str, model: AIModel, options: Dict[str, Any] = {}) -> Tuple[int, str]:
        # deprecated time function, don't care
        parsed_options = self._parse_options(options)
        start_time = datetime.utcnow()
        response_json = self._chat(message, model.name, parsed_options)
        end_time = datetime.utcnow()
        time_elapsed_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)
        
        # return first choice
        for choice in response_json["choices"]:
            try:
                return time_elapsed_in_milliseconds, choice["message"]["content"]
            except Exception as exc:
                return -1, str(exc)

    def _chat(self, message: str, model_name: str, options: Dict[str, Any] = {}):
        headers = {"Authorization": f"Bearer {self.bearer}"}
        url = f"https://{self.host}/api/chat/completions"
        post_body = {
            "model": model_name,
            "messages": [
                {"role": "user",
                 "content": message},
            ]
        }
        post_body.update(options)
        response = requests.post(url, json=post_body, headers=headers)
        response.raise_for_status()
        return response.json()
