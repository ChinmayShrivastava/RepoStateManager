class MockChatLLM(MagicMock):
    def chat(self, prompt: str) -> ChatResponse:
        test_object = {"hello": "chat"}
        text = json.dumps(test_object)
        return ChatResponse(
            message=ChatMessage(role=MessageRole.ASSISTANT, content=text)
        )

    @property
    def metadata(self) -> LLMMetadata:
        metadata = LLMMetadata()
        metadata.is_chat_model = True
        return metadata
