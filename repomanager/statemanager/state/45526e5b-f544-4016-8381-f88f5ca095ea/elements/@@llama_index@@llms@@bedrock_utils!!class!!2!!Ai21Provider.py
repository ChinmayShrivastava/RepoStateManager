class Ai21Provider(Provider):
    max_tokens_key = "maxTokens"

    def get_text_from_response(self, response: dict) -> str:
        return response["completions"][0]["data"]["text"]
