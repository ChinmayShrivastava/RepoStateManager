def test_get_when_initial_tokens_exceed_limit_raises_value_error() -> None:
    # Given some initial tokens exceeding token_limit
    initial_tokens = 50
    memory = ChatMemoryBuffer.from_defaults(token_limit=initial_tokens - 1)

    # When I get the chat history from the memory
    with pytest.raises(ValueError) as error:
        memory.get(initial_tokens)

    # Then a value error should be raised
    assert str(error.value) == "Initial token count exceeds token limit"
