def test_template_output_parser(output_parser: BaseOutputParser) -> None:
    prompt_txt = "hello {text} {foo}"
    prompt = PromptTemplate(prompt_txt, output_parser=output_parser)

    prompt_fmt = prompt.format(text="world", foo="bar")
    assert prompt_fmt == "hello world bar\noutput_instruction"
