def test_chat(MockSyncOpenAI: MagicMock) -> None:
    content = "placeholder"

    mock_instance = MockSyncOpenAI.return_value
    mock_instance.chat.completions.create.return_value = mock_chat_completion(content)

    llm = LocalAI(model="models/placeholder.gguf", globally_use_chat_completions=True)

    response = llm.chat([ChatMessage(role="user", content="test message")])
    assert response.message.content == content
