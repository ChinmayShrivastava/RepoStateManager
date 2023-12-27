def test_langchain_template() -> None:
    lc_template = LangchainTemplate.from_template("hello {text} {foo}")
    template = LangchainPromptTemplate(lc_template)

    template_fmt = template.partial_format(foo="bar")
    assert isinstance(template, LangchainPromptTemplate)

    assert template_fmt.format(text="world") == "hello world bar"

    assert template_fmt.format_messages(text="world") == [
        ChatMessage(content="hello world bar", role=MessageRole.USER)
    ]

    ## check with more fields set + partial format
    template_2 = LangchainPromptTemplate(
        lc_template, template_var_mappings={"text2": "text"}
    )
    template_2_partial = template_2.partial_format(foo="bar")
    assert template_2_partial.format(text2="world2") == "hello world2 bar"
