def test_guidance_pydantic_program() -> None:
    class TestModel(BaseModel):
        test_attr: str

    program = GuidancePydanticProgram(
        output_cls=TestModel,
        prompt_template_str="This is a test prompt with a {{test_input}}.",
        guidance_llm=MockLLM(),
    )

    assert program.output_cls == TestModel

    output = program(test_input="test_arg")
    assert isinstance(output, TestModel)
