class Provider(ABC):
    @property
    @abstractmethod
    def max_tokens_key(self) -> str:
        ...

    @abstractmethod
    def get_text_from_response(self, response: dict) -> str:
        ...

    def get_text_from_stream_response(self, response: dict) -> str:
        return self.get_text_from_response(response)

    def get_request_body(self, prompt: str, inference_parameters: dict) -> dict:
        return {"prompt": prompt, **inference_parameters}

    messages_to_prompt: Optional[Callable[[Sequence[ChatMessage]], str]] = None
    completion_to_prompt: Optional[Callable[[str], str]] = None
