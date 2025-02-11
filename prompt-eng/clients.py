import requests
from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from models import AIModel, ModelOptions
from config import config_factory
import logging


logger = logging.getLogger(__name__)

# interface for chatbot clients
class ChatbotClient(ABC):
    @abstractmethod
    def get_models(self) -> List[AIModel]:
        pass

    @abstractmethod
    def chat_completion(self, message: str, model: AIModel, options: ModelOptions | None) -> Tuple[int, str]:
        pass

    def set_system_prompt(self, prompt: str) -> None:
        if prompt:
            self._system_prompt = prompt

    # this format is currently the same for both APIS, consider overriding if your client has different requirements.
    def _generate_system_message(self) -> Dict[str,str]:
        if self._system_prompt:
            return {"role": "system", "content": self._system_prompt}
        else:
            return {}


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
        else:
            return OllamaClient(host=host)

        
class OpenWebUIClient(ChatbotClient):
    def __init__(self, host: str, bearer: str):
        self._host = host
        self._bearer = bearer
        self._system_prompt = ""

    # TODO : Maybe considering making options a type, that way it can be validated and consistent
    # between client implementations.
    def _parse_options(self, options: ModelOptions | None) -> Dict[str, Any]:
        """Parse the generic options type into params for the specific API"""

        implemented_options = {}
        options.validate()
        if options.context_window_size:
            implemented_options["num_ctx"] = options.context_window_size
        if options.max_tokens:
            implemented_options["max_tokens"] = options.max_tokens
        if options.top_k:
            implemented_options["top_k"] = options.top_k
        if options.top_p:
            implemented_options["top_p"] = options.top_p
        if options.temperature:
            implemented_options["temperature"] = options.temperature
        if options.seed:
            implemented_options["seed"] = options.seed

        return implemented_options

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

    def chat_completion(self, message: str, model: AIModel, options: ModelOptions | None = None) -> Tuple[int, str]:
        """Send a message to an LLM of your choice and get the response."""
        
        start_time = datetime.now(timezone.utc)
        response_json = self._chat(message, model.name, options)
        end_time = datetime.now(timezone.utc)
        time_elapsed_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)
        
        # return first choice
        for choice in response_json["choices"]:
            try:
                return time_elapsed_in_milliseconds, choice["message"]["content"]
            except Exception as exc:
                return -1, str(exc)

    def _chat(self, message: str, model_name: str, options: ModelOptions | None = None):
        """Send a chat request to the API and get the response."""

        headers = {"Authorization": f"Bearer {self._bearer}"}
        url = f"https://{self._host}/api/chat/completions"
        post_body = {
            "model": model_name,
            "messages": [
                {"role": "user",
                 "content": message}
            ]
        }
        
        post_body.update(self._parse_options(options) if options else {})
        if self._system_prompt:
            post_body["messages"] = [self._generate_system_message()] + post_body["messages"]
        response = requests.post(url, json=post_body, headers=headers)
        response.raise_for_status()
        return response.json()
    
class OllamaClient(ChatbotClient):
    def __init__(self, host: str):
        self._host = host
        self._system_prompt = ""

    def chat_completion(self, message: str, model: AIModel, options: ModelOptions | None = None) -> Tuple[int, str]:
        """Send a chat request to the API and get the response."""
        start_time = datetime.now(timezone.utc)
        response = self._chat(message, model.name, options)
        end_time = datetime.now(timezone.utc)
        time_taken_in_ms = (end_time - start_time).total_seconds() * 1000
        return time_taken_in_ms, response["message"]["content"]


    def _chat(self, message: str, model_name: str, options: ModelOptions | None = None) -> Dict[str,str]:
        """Send a chat request to the API and get the response."""
        url = f"http://{self._host}/api/chat"
        post_body = {
            "model": model_name,
            "messages": [
                {
                "role": "user",
                "content": message
                }
            ],
            "stream": False
        }
        post_body.update(self._parse_options(options) if options else {})
        if self._system_prompt:
            post_body["messages"] = [self._generate_system_message()] + post_body["messages"]
        breakpoint()
        response = requests.post(url, json=post_body, timeout=600)
        response.raise_for_status()
        return response.json()

    # reference https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
    def _parse_options(self, options: ModelOptions) -> None:
        """Converts generic options into API specfic options"""
        nested_options: Dict[str, Any] = {}
        options.validate()

        if options.max_tokens:
            nested_options["num_predict"] = options.max_tokens
        if options.temperature:
            nested_options["temperature"] = options.temperature
        if options.top_p:
            nested_options["top_p"] = options.top_p
        if options.seed:
            nested_options["seed"] = options.seed
        if options.top_k:
            nested_options["top_k"] = options.top_k
        if options.context_window_size:
            nested_options["num_ctx"] = options.context_window_size
        if nested_options:
            return {"options": nested_options}

        return {}
   
    def get_models(self) -> List[AIModel]:  
        """Get a list of available models. API CALL"""
        data = self._get_models()
        return [AIModel(name=model["name"],parameter_size=model["details"]["parameter_size"]) for model in data["models"]]

    def _get_models(self):
        """Get a list of available models."""
        url = f"http://{self._host}/api/tags"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def set_system_prompt(self, prompt):
        if prompt:
            self._system_prompt = prompt
        

def bootstrap_client_and_model(preferred_model: str = "") -> Tuple[ChatbotClient, AIModel]:
    """Generic bootstrapper to load config, create client with factory, and provide a model
        you can optionally provide a preferred model by providing it as the function arg"""
    config = config_factory()
    client = ChatbotClientFactory.create_client(config)
    models = client.get_models()
    fallback_model = _get_smallest_model(models)
    picked_model = None
    for modl in models:
        if preferred_model == modl.name:
            picked_model = modl
            break
    if not picked_model and preferred_model:
        logger.warning(f"Model {preferred_model} not found. Using fallback model of {fallback_model.name} instead.")
        picked_model = fallback_model
    picked_model = picked_model if picked_model else fallback_model
    return client, picked_model

def _get_smallest_model(models: List[AIModel]):
    """Get the smallest model in the list of models by parameter size"""
    # TODO : Pretty sure this whole function could be a one liner.
    # But would that be too expressive and hard to read?
    smallest = 9999999
    chosen_model = None
    for model in models:
        size = float(model.parameter_size.strip("B"))
        if size < smallest:
            smallest = size
            chosen_model = model
    
    return chosen_model
