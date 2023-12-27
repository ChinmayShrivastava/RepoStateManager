def test_template() -> None:
    """Test partial format."""
    prompt_txt = "hello {text} {foo}"
    prompt = PromptTemplate(prompt_txt)

    prompt_fmt = prompt.partial_format(foo="bar")
    assert isinstance(prompt_fmt, PromptTemplate)

    assert prompt_fmt.format(text="world") == "hello world bar"

    assert prompt_fmt.format_messages(text="world") == [
        ChatMessage(content="hello world bar", role=MessageRole.USER)
    ]
