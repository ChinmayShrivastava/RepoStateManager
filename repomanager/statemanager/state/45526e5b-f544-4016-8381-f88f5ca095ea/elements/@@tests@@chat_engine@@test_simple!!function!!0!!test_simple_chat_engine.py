def test_simple_chat_engine(
    mock_service_context: ServiceContext,
) -> None:
    engine = SimpleChatEngine.from_defaults(service_context=mock_service_context)

    engine.reset()
    response = engine.chat("Test message 1")
    assert str(response) == "user: Test message 1\nassistant: "

    response = engine.chat("Test message 2")
    assert (
        str(response)
        == "user: Test message 1\nassistant: user: Test message 1\nassistant: \n"
        "user: Test message 2\nassistant: "
    )

    engine.reset()
    response = engine.chat("Test message 3")
    assert str(response) == "user: Test message 3\nassistant: "
