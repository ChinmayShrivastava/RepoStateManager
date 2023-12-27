class AnthropicProvider(Provider):
    max_tokens_key = "max_tokens_to_sample"

    def __init__(self) -> None:
        self.messages_to_prompt = messages_to_anthropic_prompt
        self.completion_to_prompt = completion_to_anthopic_prompt

    def get_text_from_response(self, response: dict) -> str:
        return response["completion"]
