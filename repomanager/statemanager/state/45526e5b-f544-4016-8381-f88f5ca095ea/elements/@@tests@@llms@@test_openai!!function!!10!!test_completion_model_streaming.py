def test_completion_model_streaming(MockSyncOpenAI: MagicMock) -> None:
    with CachedOpenAIApiKeys(set_fake_key=True):
        mock_instance = MockSyncOpenAI.return_value
        mock_instance.completions.create.return_value = mock_completion_stream_v1()

        llm = OpenAI(model="text-davinci-003")
        prompt = "test prompt"
        message = ChatMessage(role="user", content="test message")

        response_gen = llm.stream_complete(prompt)
        responses = list(response_gen)
        assert responses[-1].text == "12"

        mock_instance.completions.create.return_value = mock_completion_stream_v1()
        chat_response_gen = llm.stream_chat([message])
        chat_responses = list(chat_response_gen)
        assert chat_responses[-1].message.content == "12"
