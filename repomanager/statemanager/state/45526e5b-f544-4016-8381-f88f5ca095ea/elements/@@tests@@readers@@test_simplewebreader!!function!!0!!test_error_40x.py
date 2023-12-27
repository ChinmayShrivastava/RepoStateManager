def test_error_40x() -> None:
    """Test simple web reader for 40x error."""
    # Generate a random URL that doesn't exist.
    url_that_doesnt_exist = "https://{url}.{tld}"
    reader = SimpleWebPageReader()
    with pytest.raises(Exception):
        reader.load_data(
            [
                url_that_doesnt_exist.format(
                    url="".join(choice(string.ascii_lowercase) for _ in range(10)),
                    tld="".join(choice(string.ascii_lowercase) for _ in range(3)),
                )
            ]
        )
