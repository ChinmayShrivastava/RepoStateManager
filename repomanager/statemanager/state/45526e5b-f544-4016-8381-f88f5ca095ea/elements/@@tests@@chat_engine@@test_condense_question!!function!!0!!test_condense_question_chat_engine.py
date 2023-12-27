def test_condense_question_chat_engine(
    mock_service_context: ServiceContext,
) -> None:
    query_engine = Mock(spec=BaseQueryEngine)
    query_engine.query.side_effect = lambda x: Response(response=x)
    engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        service_context=mock_service_context,
    )

    engine.reset()
    response = engine.chat("Test message 1")
    assert str(response) == "{'question': 'Test message 1', 'chat_history': ''}"

    response = engine.chat("Test message 2")
    assert str(response) == (
        "{'question': 'Test message 2', 'chat_history': \"user: Test message 1"
        "\\nassistant: {'question': 'Test message 1', 'chat_history': ''}\"}"
    )

    engine.reset()
    response = engine.chat("Test message 3")
    assert str(response) == "{'question': 'Test message 3', 'chat_history': ''}"
