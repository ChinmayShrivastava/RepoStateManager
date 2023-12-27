def test_from_docs(
    mock_service_context: ServiceContext,
) -> None:
    """Test initialization via a list of documents."""
    mock_service_context.embed_model = MockEmbedding()
    documents = [
        Document(text="I can't carry it for you."),
        Document(text="But I can carry you!"),
    ]

    playground = Playground.from_docs(
        documents=documents, service_context=mock_service_context
    )

    assert len(playground.indices) == len(DEFAULT_INDEX_CLASSES)
    assert len(playground.retriever_modes) == len(DEFAULT_MODES)

    with pytest.raises(ValueError):
        playground = Playground.from_docs(
            documents=documents,
            retriever_modes={},
            service_context=mock_service_context,
        )
