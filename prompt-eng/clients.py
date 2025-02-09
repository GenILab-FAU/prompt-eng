import requests
from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from models import AIModel
from config import config_factory
import random
import logging

logger = logging.getLogger(__name__)

# interface for chatbot clients
class ChatbotClient(ABC):
    @abstractmethod
    def get_models(self) -> List[AIModel]:
        pass

    @abstractmethod
    def chat(self, message: str, model: AIModel, options: Dict[str, Any]) -> Tuple[int, str]:
        pass

    def set_system_prompt(self, prompt: str):
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
        # TODO : Implement Ollama client.
        else:
            raise ValueError(f"Unknown host: {host}")

        
class OpenWebUIClient(ChatbotClient):
    def __init__(self, host: str, bearer: str):
        self._host = host
        self._bearer = bearer
        self._system_prompt = ""

    # TODO : Maybe considering making options a type, that way it can be validated and consistent
    # between client implementations.
    def _parse_options(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Filter out the options dict to only include the options that are implemented by this client."""

        implemented_options = {}
        for key, value in options.items():
            if key in {"temperature", "max_tokens"}:
                implemented_options[key] = value
        
        return implemented_options
    
    def set_system_prompt(self, prompt: str) -> None:
        if prompt:
            self._system_prompt = prompt

    def _generate_system_message(self) -> Dict[str,str]:
        if self._system_prompt:
            return {"role": "system", "content": self._system_prompt}
        else:
            return {}


    def _get_models(self) -> Dict[Any, Any]:
        """Get the list of available models from the server."""

        url = f"https://{self._host}/api/models"
        headers = {
            "Authorization": f"Bearer {self._bearer}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_models(self) -> List[AIModel]:
        """Get the list of available models from the server."""

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
        """Send a message to an LLM of your choice and get the response."""
        
        parsed_options = self._parse_options(options)
        start_time = datetime.now(timezone.utc)
        response_json = self._chat(message, model.name, parsed_options)
        end_time = datetime.now(timezone.utc)
        time_elapsed_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)
        
        # return first choice
        for choice in response_json["choices"]:
            try:
                return time_elapsed_in_milliseconds, choice["message"]["content"]
            except Exception as exc:
                return -1, str(exc)

    def _chat(self, message: str, model_name: str, options: Dict[str, Any] = {}):
        """Send a chat request to the API and get the response."""

        headers = {"Authorization": f"Bearer {self._bearer}"}
        url = f"https://{self._host}/api/chat/completions"
        post_body = {
            "model": model_name,
            "messages": [
                {"role": "user",
                 "content": message},
            ]
        }
        
        post_body.update(options)
        if self._system_prompt:
            post_body["messages"] = [self._generate_system_message()] + post_body["messages"]
        response = requests.post(url, json=post_body, headers=headers)
        response.raise_for_status()
        return response.json()

# this is just for ease of use, bootstraps the config and instantiates a model and a client
def bootstrap_client_and_model(model: str) -> Tuple[ChatbotClient, AIModel]:
    config = config_factory()
    client = ChatbotClientFactory.create_client(config)
    models = client.get_models()
    fallback_model = random.choice(models)
    picked_model = None
    for modl in models:
        if model == modl.name:
            picked_model = modl
            break
    if not picked_model:
        logger.warning(f"Model {model} not found. Using fallback model of {fallback_model.name} instead.")
        picked_model = fallback_model
    return client, picked_model

