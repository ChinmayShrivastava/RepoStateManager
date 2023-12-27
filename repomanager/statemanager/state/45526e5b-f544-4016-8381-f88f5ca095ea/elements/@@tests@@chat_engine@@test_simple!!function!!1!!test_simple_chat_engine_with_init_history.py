def test_simple_chat_engine_with_init_history(
    mock_service_context: ServiceContext,
) -> None:
    engine = SimpleChatEngine.from_defaults(
        service_context=mock_service_context,
        chat_history=[
            ChatMessage(role=MessageRole.USER, content="test human message"),
            ChatMessage(role=MessageRole.ASSISTANT, content="test ai message"),
        ],
    )

    response = engine.chat("new human message")
    assert (
        str(response) == "user: test human message\nassistant: test ai message\n"
        "user: new human message\nassistant: "
    )
