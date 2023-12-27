def test_convert_pydantic_to_guidance_output_template_simple() -> None:
    output_str = pydantic_to_guidance_output_template(TestSimpleModel)
    assert output_str == EXPECTED_SIMPLE_STR
