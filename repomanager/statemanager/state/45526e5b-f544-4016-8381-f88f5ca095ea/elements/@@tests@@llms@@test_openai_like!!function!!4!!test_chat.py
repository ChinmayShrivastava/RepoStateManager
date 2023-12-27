def test_chat(MockSyncOpenAI: MagicMock) -> None:
    content = "placeholder"

    mock_instance = MockSyncOpenAI.return_value
    mock_instance.chat.completions.create.return_value = mock_chat_completion(content)

    llm = OpenAILike(
        model=STUB_MODEL_NAME, is_chat_model=True, tokenizer=StubTokenizer()
    )

    response = llm.chat([ChatMessage(role=MessageRole.USER, content="test message")])
    assert response.message.content == content
    mock_instance.chat.completions.create.assert_called_once_with(
        messages=[{"role": MessageRole.USER, "content": "test message"}],
        stream=False,
        model=STUB_MODEL_NAME,
        temperature=0.1,
    )
