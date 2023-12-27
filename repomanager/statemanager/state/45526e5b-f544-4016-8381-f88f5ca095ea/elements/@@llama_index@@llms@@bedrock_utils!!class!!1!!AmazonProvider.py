class AmazonProvider(Provider):
    max_tokens_key = "maxTokenCount"

    def get_text_from_response(self, response: dict) -> str:
        return response["results"][0]["outputText"]

    def get_text_from_stream_response(self, response: dict) -> str:
        return response["outputText"]

    def get_request_body(self, prompt: str, inference_parameters: dict) -> dict:
        return {
            "inputText": prompt,
            "textGenerationConfig": {**inference_parameters},
        }
