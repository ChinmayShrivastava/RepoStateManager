def test_chat_model_basic_non_openai_model(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "llama_index.llms.konko.completion_with_retry", mock_chat_completion
    )
    llm = Konko(model="meta-llama/Llama-2-13b-chat-hf")
    prompt = "test prompt"
    message = ChatMessage(role="user", content="test message")

    response = llm.complete(prompt)
    assert response.text is not None

    chat_response = llm.chat([message])
    assert chat_response.message.content is not None
