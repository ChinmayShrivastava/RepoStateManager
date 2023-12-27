def test_serialization() -> None:
    llm = LocalAI(model="models/placeholder.gguf", max_tokens=42, context_window=43)

    serialized = llm.to_dict()
    # Check OpenAI base class specifics
    assert serialized["max_tokens"] == 42
    # Check LocalAI subclass specifics
    assert serialized["context_window"] == 43
