def test_dict_save_load() -> None:
    memory = ChatMemoryBuffer.from_defaults(
        chat_history=[USER_CHAT_MESSAGE], token_limit=5
    )

    json_dict = memory.to_dict()

    new_memory = ChatMemoryBuffer.from_dict(json_dict)

    assert len(new_memory.get()) == 1
    assert new_memory.token_limit == 5
