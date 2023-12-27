def test_multi_modal_llm_program() -> None:
    """Test Multi Modal LLM Pydantic program."""
    output_parser = PydanticOutputParser(output_cls=TestModel)
    multi_modal_llm_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=output_parser,
        prompt_template_str="This is a test prompt with a {test_input}.",
        multi_modal_llm=MockMultiModalLLM(),
        image_documents=[ImageDocument()],
    )
    # mock Multi Modal llm
    obj_output = multi_modal_llm_program(test_input="hello")
    assert isinstance(obj_output, TestModel)
    assert obj_output.hello == "world"
