def test_model_streaming() -> None:
    credentials = {"url": "https://thisisa.fake.url/", "apikey": "fake_api_key"}
    project_id = "fake_project_id"

    test_prompt = "This is a test"
    llm = WatsonX(
        model_id="ibm/granite-13b-instruct-v1",
        credentials=credentials,
        project_id=project_id,
    )

    response_gen = llm.stream_complete(test_prompt)
    response = list(response_gen)

    assert response[-1].text == "\n\nThis is indeed a test"

    message = ChatMessage(role="user", content=test_prompt)
    chat_response_gen = llm.stream_chat([message])
    chat_response = list(chat_response_gen)
    assert chat_response[-1].message.content == "\n\nThis is indeed a test"
