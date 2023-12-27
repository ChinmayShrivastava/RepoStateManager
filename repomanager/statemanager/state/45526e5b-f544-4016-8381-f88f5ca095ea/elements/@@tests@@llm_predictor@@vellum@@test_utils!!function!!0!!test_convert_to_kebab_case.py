def test_convert_to_kebab_case(input_string: str, expected: str) -> None:
    assert convert_to_kebab_case(input_string) == expected
