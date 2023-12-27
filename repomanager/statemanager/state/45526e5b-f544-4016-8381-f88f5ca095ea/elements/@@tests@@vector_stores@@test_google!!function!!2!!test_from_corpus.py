def test_from_corpus(mock_get_corpus: MagicMock) -> None:
    # Arrange
    mock_get_corpus.return_value = genai.Corpus(name="corpora/123")

    # Act
    store = GoogleVectorStore.from_corpus(corpus_id="123")

    # Assert
    assert store.corpus_id == "123"
