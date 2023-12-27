def test_chat_template_output_parser(output_parser: BaseOutputParser) -> None:
    chat_template = ChatPromptTemplate(
        message_templates=[
            ChatMessage(
                content="This is a system message with a {sys_param}",
                role=MessageRole.SYSTEM,
            ),
            ChatMessage(content="hello {text} {foo}", role=MessageRole.USER),
        ],
        prompt_type=PromptType.CONVERSATION,
        output_parser=output_parser,
    )

    messages = chat_template.format_messages(
        text="world", foo="bar", sys_param="sys_arg"
    )
    assert (
        messages[0].content
        == "This is a system message with a sys_arg\noutput_instruction"
    )
