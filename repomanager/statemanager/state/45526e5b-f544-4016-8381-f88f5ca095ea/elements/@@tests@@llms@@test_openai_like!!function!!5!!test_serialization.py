def test_serialization() -> None:
    llm = OpenAILike(
        model=STUB_MODEL_NAME,
        is_chat_model=True,
        max_tokens=42,
        context_window=43,
        tokenizer=StubTokenizer(),
    )

    serialized = llm.to_dict()
    # Check OpenAI base class specifics
    assert "api_key" not in serialized
    assert serialized["max_tokens"] == 42
    # Check OpenAILike subclass specifics
    assert serialized["context_window"] == 43
    assert serialized["is_chat_model"]
