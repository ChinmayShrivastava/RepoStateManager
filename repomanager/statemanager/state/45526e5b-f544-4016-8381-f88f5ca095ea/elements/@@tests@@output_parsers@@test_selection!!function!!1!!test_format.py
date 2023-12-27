def test_format(output_parser: SelectionOutputParser) -> None:
    test_template = "Test prompt template with some {field} to fill in."
    new_test_template = output_parser.format(test_template)
    new_test_template.format(field="field")
