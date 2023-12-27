def test_delete(
    mock_get_corpus: MagicMock,
    mock_delete_document: MagicMock,
) -> None:
    # Arrange
    mock_get_corpus.return_value = genai.Corpus(name="corpora/123")

    # Act
    store = GoogleVectorStore.from_corpus(corpus_id="123")
    store.delete(ref_doc_id="doc-456")

    # Assert
    delete_document_request = mock_delete_document.call_args.args[0]
    assert delete_document_request == genai.DeleteDocumentRequest(
        name="corpora/123/documents/doc-456",
        force=True,
    )
