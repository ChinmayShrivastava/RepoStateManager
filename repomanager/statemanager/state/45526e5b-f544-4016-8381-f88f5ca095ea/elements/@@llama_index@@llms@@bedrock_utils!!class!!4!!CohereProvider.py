class CohereProvider(Provider):
    max_tokens_key = "max_tokens"

    def get_text_from_response(self, response: dict) -> str:
        return response["generations"][0]["text"]
