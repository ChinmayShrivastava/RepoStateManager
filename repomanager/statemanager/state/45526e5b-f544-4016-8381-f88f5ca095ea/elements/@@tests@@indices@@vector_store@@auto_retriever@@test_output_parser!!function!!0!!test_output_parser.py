def test_output_parser() -> None:
    output_str = """\
    ```json
    {
        "query": "test query str",
        "filters": [
            {
                "key": "director",
                "value": "Nolan"
            },
            {
                "key": "theme",
                "value": "sci-fi"
            }
        ],
        "top_k": 2
    }
    ```
    """

    parser = VectorStoreQueryOutputParser()
    output = parser.parse(output_str)
    structured_output = cast(StructuredOutput, output)
    assert isinstance(structured_output.parsed_output, VectorStoreQuerySpec)

    expected = VectorStoreQuerySpec(
        query="test query str",
        filters=[
            ExactMatchFilter(key="director", value="Nolan"),
            ExactMatchFilter(key="theme", value="sci-fi"),
        ],
        top_k=2,
    )
    assert structured_output.parsed_output == expected
