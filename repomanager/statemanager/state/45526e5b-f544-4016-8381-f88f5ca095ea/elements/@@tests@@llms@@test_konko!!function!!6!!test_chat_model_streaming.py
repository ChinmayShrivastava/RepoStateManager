def test_chat_model_streaming(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "llama_index.llms.konko.completion_with_retry", mock_chat_completion_stream
    )
    llm = Konko(model="meta-llama/Llama-2-13b-chat-hf")
    message = ChatMessage(role="user", content="test message")
    chat_response_gen = llm.stream_chat([message])
    chat_responses = list(chat_response_gen)
    assert chat_responses[-1].message.content is not None
