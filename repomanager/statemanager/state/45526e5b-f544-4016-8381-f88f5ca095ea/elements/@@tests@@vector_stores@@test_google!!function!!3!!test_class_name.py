def test_class_name() -> None:
    # Act
    class_name = GoogleVectorStore.class_name()

    # Assert
    assert class_name == "GoogleVectorStore"
