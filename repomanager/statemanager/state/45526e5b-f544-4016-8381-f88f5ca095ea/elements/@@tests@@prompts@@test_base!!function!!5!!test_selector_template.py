def test_selector_template() -> None:
    default_template = PromptTemplate("hello {text} {foo}")
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

    selector_template = SelectorPromptTemplate(
        default_template=default_template,
        conditionals=[
            (lambda llm: isinstance(llm, MockLLM), chat_template),
        ],
    )

    partial_template = selector_template.partial_format(text="world", foo="bar")

    prompt = partial_template.format()
    assert prompt == "hello world bar"

    messages = partial_template.format_messages(llm=MockLLM(), sys_param="sys_arg")
    assert messages[0] == ChatMessage(
        content="This is a system message with a sys_arg", role=MessageRole.SYSTEM
    )
