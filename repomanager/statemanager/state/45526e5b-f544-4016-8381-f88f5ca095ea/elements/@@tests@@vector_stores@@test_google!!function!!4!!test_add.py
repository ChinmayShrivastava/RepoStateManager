def test_add(
    mock_get_corpus: MagicMock,
    mock_get_document: MagicMock,
    mock_create_document: MagicMock,
    mock_batch_create_chunks: MagicMock,
) -> None:
    from google.api_core import exceptions as gapi_exception

    # Arrange
    # We will use a max requests per batch to be 2.
    # Then, we send 3 requests.
    # We expect to have 2 batches where the last batch has only 1 request.
    genaix._MAX_REQUEST_PER_CHUNK = 2
    mock_get_corpus.return_value = genai.Corpus(name="corpora/123")
    mock_get_document.side_effect = gapi_exception.NotFound("")
    mock_create_document.return_value = genai.Document(name="corpora/123/documents/456")
    mock_batch_create_chunks.side_effect = [
        genai.BatchCreateChunksResponse(
            chunks=[
                genai.Chunk(name="corpora/123/documents/456/chunks/777"),
                genai.Chunk(name="corpora/123/documents/456/chunks/888"),
            ]
        ),
        genai.BatchCreateChunksResponse(
            chunks=[
                genai.Chunk(name="corpora/123/documents/456/chunks/999"),
            ]
        ),
    ]

    # Act
    store = GoogleVectorStore.from_corpus(corpus_id="123")
    response = store.add(
        [
            TextNode(
                text="Hello my baby",
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id="456",
                        metadata={"file_name": "Title for doc 456"},
                    )
                },
                metadata={"position": 100},
            ),
            TextNode(
                text="Hello my honey",
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id="456",
                        metadata={"file_name": "Title for doc 456"},
                    )
                },
                metadata={"position": 200},
            ),
            TextNode(
                text="Hello my ragtime gal",
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(
                        node_id="456",
                        metadata={"file_name": "Title for doc 456"},
                    )
                },
                metadata={"position": 300},
            ),
        ]
    )

    # Assert
    assert response == [
        "corpora/123/documents/456/chunks/777",
        "corpora/123/documents/456/chunks/888",
        "corpora/123/documents/456/chunks/999",
    ]

    create_document_request = mock_create_document.call_args.args[0]
    assert create_document_request == genai.CreateDocumentRequest(
        parent="corpora/123",
        document=genai.Document(
            name="corpora/123/documents/456",
            display_name="Title for doc 456",
            custom_metadata=[
                genai.CustomMetadata(
                    key="file_name",
                    string_value="Title for doc 456",
                ),
            ],
        ),
    )

    assert mock_batch_create_chunks.call_count == 2
    mock_batch_create_chunks_calls = mock_batch_create_chunks.call_args_list

    first_batch_create_chunks_request = mock_batch_create_chunks_calls[0].args[0]
    assert first_batch_create_chunks_request == genai.BatchCreateChunksRequest(
        parent="corpora/123/documents/456",
        requests=[
            genai.CreateChunkRequest(
                parent="corpora/123/documents/456",
                chunk=genai.Chunk(
                    data=genai.ChunkData(string_value="Hello my baby"),
                    custom_metadata=[
                        genai.CustomMetadata(
                            key="position",
                            numeric_value=100,
                        ),
                    ],
                ),
            ),
            genai.CreateChunkRequest(
                parent="corpora/123/documents/456",
                chunk=genai.Chunk(
                    data=genai.ChunkData(string_value="Hello my honey"),
                    custom_metadata=[
                        genai.CustomMetadata(
                            key="position",
                            numeric_value=200,
                        ),
                    ],
                ),
            ),
        ],
    )

    second_batch_create_chunks_request = mock_batch_create_chunks_calls[1].args[0]
    assert second_batch_create_chunks_request == genai.BatchCreateChunksRequest(
        parent="corpora/123/documents/456",
        requests=[
            genai.CreateChunkRequest(
                parent="corpora/123/documents/456",
                chunk=genai.Chunk(
                    data=genai.ChunkData(string_value="Hello my ragtime gal"),
                    custom_metadata=[
                        genai.CustomMetadata(
                            key="position",
                            numeric_value=300,
                        ),
                    ],
                ),
            ),
        ],
    )
