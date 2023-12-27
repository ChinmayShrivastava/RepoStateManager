def test_chat_template() -> None:
    chat_template = ChatPromptTemplate(
        message_templates=[
            ChatMessage(
                content="This is a system message with a {sys_param}",
                role=MessageRole.SYSTEM,
            ),
            ChatMessage(content="hello {text} {foo}", role=MessageRole.USER),
        ],
        prompt_type=PromptType.CONVERSATION,
    )

    partial_template = chat_template.partial_format(sys_param="sys_arg")
    messages = partial_template.format_messages(text="world", foo="bar")

    assert messages[0] == ChatMessage(
        content="This is a system message with a sys_arg", role=MessageRole.SYSTEM
    )

    assert partial_template.format(text="world", foo="bar") == (
        "system: This is a system message with a sys_arg\n"
        "user: hello world bar\n"
        "assistant: "
    )
