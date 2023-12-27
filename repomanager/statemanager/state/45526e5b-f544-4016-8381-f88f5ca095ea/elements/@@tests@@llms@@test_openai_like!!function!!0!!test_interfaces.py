def test_interfaces() -> None:
    llm = OpenAILike(model=STUB_MODEL_NAME, api_key=STUB_API_KEY)
    assert llm.class_name() == type(llm).__name__
    assert llm.model == STUB_MODEL_NAME
