def test_url_metadata() -> None:
    """Test simple web reader with metadata hook."""
    # Set up a reader to return the URL as metadata.
    reader = SimpleWebPageReader(metadata_fn=lambda url: {"url": url})
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    documents = reader.load_data([url])
    assert len(documents) == 1
    assert documents[0].metadata == {"url": url}
