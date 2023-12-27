def test_messages_to_anthropic_prompt() -> None:
    messages = [
        ChatMessage(role=MessageRole.USER, content="Hello"),
    ]

    expected_prompt = "\n\nHuman: Hello\n\nAssistant: "
    actual_prompt = messages_to_anthropic_prompt(messages)
    assert actual_prompt == expected_prompt

    messages = [
        ChatMessage(role=MessageRole.USER, content="Hello"),
        ChatMessage(role=MessageRole.ASSISTANT, content="Continue this sentence"),
    ]

    expected_prompt = "\n\nHuman: Hello\n\nAssistant: Continue this sentence"
    actual_prompt = messages_to_anthropic_prompt(messages)
    assert actual_prompt == expected_prompt
