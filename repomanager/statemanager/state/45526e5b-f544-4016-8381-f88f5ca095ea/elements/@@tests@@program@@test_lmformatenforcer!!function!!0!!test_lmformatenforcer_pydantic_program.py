def test_lmformatenforcer_pydantic_program() -> None:
    class TestModel(BaseModel):
        test_attr: str

    prompt = "This is a test prompt with a {test_input}."
    generated_text = '{"test_attr": "blue"}'
    test_value = "test_arg"

    llm = MagicMock(spec=HuggingFaceLLM)
    llm.complete.return_value = CompletionResponse(text=generated_text)
    llm.generate_kwargs = {}

    program = LMFormatEnforcerPydanticProgram(
        output_cls=TestModel, prompt_template_str=prompt, llm=llm
    )

    output = program(test_input=test_value)
    assert isinstance(output, TestModel)
    assert output.test_attr == "blue"
