class MockMultiModalLLM(MagicMock):
    def complete(
        self, prompt: str, image_documents: Sequence[ImageDocument]
    ) -> CompletionResponse:
        test_object = {"hello": "world"}
        text = json.dumps(test_object)
        return CompletionResponse(text=text)

    @property
    def metadata(self) -> MultiModalLLMMetadata:
        return MultiModalLLMMetadata()
