def test_streaming() -> None:
    llm = TestLLM()

    prompt = "test prompt"
    message = ChatMessage(role="user", content="test message")

    llm.stream_complete(prompt)
    llm.stream_chat([message])
