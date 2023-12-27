def test_to_lc_messages() -> None:
    lc_messages: List[BaseMessage] = [
        SystemMessage(content="test system message"),
        HumanMessage(content="test human message"),
        AIMessage(content="test ai message"),
        FunctionMessage(content="test function message", name="test function"),
    ]

    messages = from_lc_messages(lc_messages)

    for i in range(len(messages)):
        assert messages[i].content == lc_messages[i].content
