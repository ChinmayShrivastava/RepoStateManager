def test_interfaces() -> None:
    llm = LocalAI(model="placeholder")
    assert llm.class_name() == type(llm).__name__
    assert llm.model == "placeholder"
