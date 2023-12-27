def test_function_mappings() -> None:
    """Test function mappings."""
    test_prompt_tmpl = """foo bar {abc} {xyz}"""

    ## PROMPT 1
    # test a format function that uses values of both abc and def
    def _format_abc(**kwargs: Any) -> str:
        """Given kwargs, output formatted variable."""
        return f"{kwargs['abc']}-{kwargs['xyz']}"

    test_prompt = PromptTemplate(
        test_prompt_tmpl, function_mappings={"abc": _format_abc}
    )
    assert test_prompt.format(abc="123", xyz="456") == "foo bar 123-456 456"

    # test partial
    test_prompt_partial = test_prompt.partial_format(xyz="456")
    assert test_prompt_partial.format(abc="789") == "foo bar 789-456 456"

    ## PROMPT 2
    # test a format function that only depends on values of xyz
    def _format_abc_2(**kwargs: Any) -> str:
        """Given kwargs, output formatted variable."""
        return f"{kwargs['xyz']}"

    test_prompt_2 = PromptTemplate(
        test_prompt_tmpl, function_mappings={"abc": _format_abc_2}
    )
    assert test_prompt_2.format(xyz="456") == "foo bar 456 456"

    # test that formatting abc itself will throw an error
    with pytest.raises(KeyError):
        test_prompt_2.format(abc="123")

    ## PROMPT 3 - test prompt with template var mappings
    def _format_prompt_key1(**kwargs: Any) -> str:
        """Given kwargs, output formatted variable."""
        return f"{kwargs['prompt_key1']}-{kwargs['prompt_key2']}"

    template_var_mappings = {
        "prompt_key1": "abc",
        "prompt_key2": "xyz",
    }
    test_prompt_3 = PromptTemplate(
        test_prompt_tmpl,
        template_var_mappings=template_var_mappings,
        # NOTE: with template mappings, needs to use the source variable names,
        # not the ones being mapped to in the template
        function_mappings={"prompt_key1": _format_prompt_key1},
    )
    assert (
        test_prompt_3.format(prompt_key1="678", prompt_key2="789")
        == "foo bar 678-789 789"
    )

    ### PROMPT 4 - test chat prompt template
    chat_template = ChatPromptTemplate(
        message_templates=[
            ChatMessage(
                content="This is a system message with a {sys_param}",
                role=MessageRole.SYSTEM,
            ),
            ChatMessage(content="hello {abc} {xyz}", role=MessageRole.USER),
        ],
        prompt_type=PromptType.CONVERSATION,
        function_mappings={"abc": _format_abc},
    )
    fmt_prompt = chat_template.format(abc="tmp1", xyz="tmp2", sys_param="sys_arg")
    assert fmt_prompt == (
        "system: This is a system message with a sys_arg\n"
        "user: hello tmp1-tmp2 tmp2\n"
        "assistant: "
    )
