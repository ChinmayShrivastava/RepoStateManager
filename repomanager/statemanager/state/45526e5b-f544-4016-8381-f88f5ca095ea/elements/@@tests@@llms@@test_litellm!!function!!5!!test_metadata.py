def test_metadata() -> None:
    llm = LiteLLM(model="gpt-3.5-turbo")
    assert isinstance(llm.metadata.context_window, int)
