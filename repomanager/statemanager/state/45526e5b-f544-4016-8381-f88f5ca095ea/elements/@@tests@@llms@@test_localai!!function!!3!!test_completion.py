def test_completion(MockSyncOpenAI: MagicMock) -> None:
    text = "placeholder"

    mock_instance = MockSyncOpenAI.return_value
    mock_instance.completions.create.return_value = mock_completion(text)

    llm = LocalAI(model="models/placeholder.gguf")

    response = llm.complete(
        "A long time ago in a galaxy far, far away", use_chat_completions=False
    )
    assert response.text == text
