def test_from_documents(
    mock_get_document: MagicMock,
    mock_batch_create_chunk: MagicMock,
    mock_create_document: MagicMock,
    mock_create_corpus: MagicMock,
) -> None:
    from google.api_core import exceptions as gapi_exception

    def fake_create_corpus(request: genai.CreateCorpusRequest) -> genai.Corpus:
        return request.corpus

    # Arrange
    mock_get_document.side_effect = gapi_exception.NotFound("")
    mock_create_corpus.side_effect = fake_create_corpus
    mock_create_document.return_value = genai.Document(name="corpora/123/documents/456")
    mock_batch_create_chunk.side_effect = [
        genai.BatchCreateChunksResponse(
            chunks=[
                genai.Chunk(name="corpora/123/documents/456/chunks/777"),
            ]
        ),
        genai.BatchCreateChunksResponse(
            chunks=[
                genai.Chunk(name="corpora/123/documents/456/chunks/888"),
            ]
        ),
    ]

    # Act
    index = GoogleIndex.from_documents(
        [
            Document(text="Hello, my darling"),
            Document(text="Goodbye, my baby"),
        ]
    )

    # Assert
    assert mock_create_corpus.call_count == 1
    create_corpus_request = mock_create_corpus.call_args.args[0]
    assert create_corpus_request.corpus.name == f"corpora/{index.corpus_id}"

    create_document_request = mock_create_document.call_args.args[0]
    assert create_document_request.parent == f"corpora/{index.corpus_id}"

    assert mock_batch_create_chunk.call_count == 2

    first_batch_request = mock_batch_create_chunk.call_args_list[0].args[0]
    assert (
        first_batch_request.requests[0].chunk.data.string_value == "Hello, my darling"
    )

    second_batch_request = mock_batch_create_chunk.call_args_list[1].args[0]
    assert (
        second_batch_request.requests[0].chunk.data.string_value == "Goodbye, my baby"
    )
