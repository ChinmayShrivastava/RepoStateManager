def test_validation() -> None:
    """Test validation of indices and modes."""
    with pytest.raises(ValueError):
        _ = Playground(indices=["VectorStoreIndex"])  # type: ignore

    with pytest.raises(ValueError):
        _ = Playground(
            indices=[VectorStoreIndex, SummaryIndex, TreeIndex]  # type: ignore
        )

    with pytest.raises(ValueError):
        _ = Playground(indices=[])  # type: ignore

    with pytest.raises(TypeError):
        _ = Playground(retriever_modes={})  # type: ignore
