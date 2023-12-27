def test_convert_pydantic_to_guidance_output_template_nested() -> None:
    output_str = pydantic_to_guidance_output_template(TestNestedModel)
    assert output_str == EXPECTED_NESTED_STR
