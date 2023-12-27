def test_model_basic(
    model: str, complete_request: str, response_body: str, chat_request: str
) -> None:
    llm = Bedrock(
        model=model,
        profile_name=None,
        aws_region_name="us-east-1",
        aws_access_key_id="test",
    )

    bedrock_stubber = Stubber(llm._client)

    # response for llm.complete()
    bedrock_stubber.add_response(
        "invoke_model",
        get_invoke_model_response(response_body),
        {"body": complete_request, "modelId": model},
    )
    # response for llm.chat()
    bedrock_stubber.add_response(
        "invoke_model",
        get_invoke_model_response(response_body),
        {"body": chat_request, "modelId": model},
    )

    bedrock_stubber.activate()

    test_prompt = "test prompt"
    response = llm.complete(test_prompt)
    assert response.text == "\n\nThis is indeed a test"

    message = ChatMessage(role="user", content=test_prompt)
    chat_response = llm.chat([message])
    assert chat_response.message.content == "\n\nThis is indeed a test"

    bedrock_stubber.deactivate()
