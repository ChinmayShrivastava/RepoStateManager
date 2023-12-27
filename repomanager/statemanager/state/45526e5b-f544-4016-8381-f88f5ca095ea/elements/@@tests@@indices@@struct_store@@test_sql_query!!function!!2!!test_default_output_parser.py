def test_default_output_parser() -> None:
    """Test default output parser."""
    test_str = "user_id:2\n" "foo:bar\n" ",,testing:testing2..\n" "number:123,456,789\n"
    fields = default_output_parser(test_str)
    assert fields == {
        "user_id": "2",
        "foo": "bar",
        "testing": "testing2",
        "number": "123456789",
    }
