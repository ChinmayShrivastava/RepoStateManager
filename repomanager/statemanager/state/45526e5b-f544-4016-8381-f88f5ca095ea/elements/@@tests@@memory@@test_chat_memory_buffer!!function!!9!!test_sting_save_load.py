def test_sting_save_load() -> None:
    memory = ChatMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE], token_limit=5
    )

    json_str = memory.to_string()

    new_memory = ChatMemoryBuffer.from_string(json_str)

    assert len(new_memory.get()) == 1
    assert new_memory.token_limit == 5
