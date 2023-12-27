def test_completion_model_basic(MockSyncOpenAI: MagicMock) -> None:
    with CachedOpenAIApiKeys(set_fake_key=True):
        mock_instance = MockSyncOpenAI.return_value
        mock_instance.completions.create.return_value = mock_completion_v1()

        llm = OpenAI(model="text-davinci-003")
        prompt = "test prompt"
        message = ChatMessage(role="user", content="test message")

        response = llm.complete(prompt)
        assert response.text == "\n\nThis is indeed a test"

        chat_response = llm.chat([message])
        assert chat_response.message.content == "\n\nThis is indeed a test"
