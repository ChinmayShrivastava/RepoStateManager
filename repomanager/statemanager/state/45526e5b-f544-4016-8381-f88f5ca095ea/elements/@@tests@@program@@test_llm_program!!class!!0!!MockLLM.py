class MockLLM(MagicMock):
    def complete(self, prompt: str) -> CompletionResponse:
        test_object = {"hello": "world"}
        text = json.dumps(test_object)
        return CompletionResponse(text=text)

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata()
