def test_chat_model_streaming(MockSyncOpenAI: MagicMock) -> None:
    with CachedOpenAIApiKeys(set_fake_key=True):
        mock_instance = MockSyncOpenAI.return_value
        mock_instance.chat.completions.create.return_value = (
            mock_chat_completion_stream_v1()
        )

        llm = OpenAI(model="gpt-3.5-turbo")
        prompt = "test prompt"
        message = ChatMessage(role="user", content="test message")

        response_gen = llm.stream_complete(prompt)
        responses = list(response_gen)
        assert responses[-1].text == "\n\n2"

        mock_instance.chat.completions.create.return_value = (
            mock_chat_completion_stream_v1()
        )
        chat_response_gen = llm.stream_chat([message])
        chat_responses = list(chat_response_gen)
        assert chat_responses[-1].message.content == "\n\n2"
        assert chat_responses[-1].message.role == "assistant"
