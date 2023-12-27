def test_get_set_compare(
    mock_service_context: ServiceContext,
) -> None:
    """Test basic comparison of indices."""
    mock_service_context.embed_model = MockEmbedding()
    documents = [Document(text="They're taking the Hobbits to Isengard!")]

    indices = [
        VectorStoreIndex.from_documents(
            documents=documents, service_context=mock_service_context
        ),
        SummaryIndex.from_documents(documents, service_context=mock_service_context),
        TreeIndex.from_documents(
            documents=documents, service_context=mock_service_context
        ),
    ]

    playground = Playground(indices=indices)  # type: ignore

    assert len(playground.indices) == 3

    results = playground.compare("Who is?", to_pandas=False)
    assert len(results) > 0
    assert len(results) <= 3 * len(DEFAULT_MODES)

    playground.indices = [
        VectorStoreIndex.from_documents(
            documents=documents, service_context=mock_service_context
        )
    ]

    assert len(playground.indices) == 1
