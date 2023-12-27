def test_split_empty_text() -> None:
    json_splitter = JSONNodeParser()
    input_text = Document(text="")
    result = json_splitter.get_nodes_from_documents([input_text])
    assert result == []
