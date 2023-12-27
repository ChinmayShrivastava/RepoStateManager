def test_model_basic() -> None:
    credentials = {"url": "https://thisisa.fake.url/", "apikey": "fake_api_key"}
    project_id = "fake_project_id"

    test_prompt = "This is a test"
    llm = WatsonX(
        model_id="ibm/granite-13b-instruct-v1",
        credentials=credentials,
        project_id=project_id,
    )

    response = llm.complete(test_prompt)
    assert response.text == "\n\nThis is indeed a test"

    message = ChatMessage(role="user", content=test_prompt)
    chat_response = llm.chat([message])
    assert chat_response.message.content == "\n\nThis is indeed a test"
