def test_model_streaming(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "llama_index.llms.bedrock.completion_with_retry",
        MockStreamCompletionWithRetry("test prompt").mock_stream_completion_with_retry,
    )
    llm = Bedrock(
        model="amazon.titan-text-express-v1",
        profile_name=None,
        aws_region_name="us-east-1",
        aws_access_key_id="test",
    )
    test_prompt = "test prompt"
    response_gen = llm.stream_complete(test_prompt)
    response = list(response_gen)
    assert response[-1].text == "\n\nThis is indeed a test"

    monkeypatch.setattr(
        "llama_index.llms.bedrock.completion_with_retry",
        MockStreamCompletionWithRetry(
            "user: test prompt\nassistant: "
        ).mock_stream_completion_with_retry,
    )
    message = ChatMessage(role="user", content=test_prompt)
    chat_response_gen = llm.stream_chat([message])
    chat_response = list(chat_response_gen)
    assert chat_response[-1].message.content == "\n\nThis is indeed a test"
