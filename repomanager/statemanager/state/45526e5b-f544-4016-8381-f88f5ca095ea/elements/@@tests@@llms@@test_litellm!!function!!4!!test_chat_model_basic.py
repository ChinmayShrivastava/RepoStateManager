def test_chat_model_basic(monkeypatch: MonkeyPatch) -> None:
    with CachedOpenAIApiKeys(set_fake_key=True):
        monkeypatch.setattr(
            "llama_index.llms.litellm.completion_with_retry", mock_chat_completion
        )

        llm = LiteLLM(model="gpt-3.5-turbo")
        prompt = "test prompt"
        message = ChatMessage(role="user", content="test message")

        response = llm.complete(prompt)
        assert response.text == "\n\nThis is a test!"

        chat_response = llm.chat([message])
        assert chat_response.message.content == "\n\nThis is a test!"
