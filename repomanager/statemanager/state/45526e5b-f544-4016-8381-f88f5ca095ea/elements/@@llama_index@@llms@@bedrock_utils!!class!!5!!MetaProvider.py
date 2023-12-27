class MetaProvider(Provider):
    max_tokens_key = "max_gen_len"

    def __init__(self) -> None:
        self.messages_to_prompt = messages_to_llama_prompt
        self.completion_to_prompt = completion_to_llama_prompt

    def get_text_from_response(self, response: dict) -> str:
        return response["generation"]
