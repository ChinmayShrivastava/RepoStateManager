def test_template_var_mappings() -> None:
    """Test template variable mappings."""
    qa_prompt_tmpl = """\
Here's some context:
{foo}
Given the context, please answer the final question:
{bar}
"""
    template_var_mappings = {
        "context_str": "foo",
        "query_str": "bar",
    }
    # try regular prompt template
    qa_prompt = PromptTemplate(
        qa_prompt_tmpl, template_var_mappings=template_var_mappings
    )
    fmt_prompt = qa_prompt.format(query_str="abc", context_str="def")
    assert (
        fmt_prompt
        == """\
Here's some context:
def
Given the context, please answer the final question:
abc
"""
    )
    # try partial format
    qa_prompt_partial = qa_prompt.partial_format(query_str="abc2")
    fmt_prompt_partial = qa_prompt_partial.format(context_str="def2")
    assert (
        fmt_prompt_partial
        == """\
Here's some context:
def2
Given the context, please answer the final question:
abc2
"""
    )

    # try chat prompt template
    # partial template var mapping
    template_var_mappings = {
        "context_str": "foo",
        "query_str": "bar",
    }
    chat_template = ChatPromptTemplate(
        message_templates=[
            ChatMessage(
                content="This is a system message with a {sys_param}",
                role=MessageRole.SYSTEM,
            ),
            ChatMessage(content="hello {foo} {bar}", role=MessageRole.USER),
        ],
        prompt_type=PromptType.CONVERSATION,
        template_var_mappings=template_var_mappings,
    )
    fmt_prompt = chat_template.format(
        query_str="abc", context_str="def", sys_param="sys_arg"
    )
    assert fmt_prompt == (
        "system: This is a system message with a sys_arg\n"
        "user: hello def abc\n"
        "assistant: "
    )
