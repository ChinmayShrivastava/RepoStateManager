def test_split_invalid_json() -> None:
    json_splitter = JSONNodeParser()
    input_text = Document(text='{"name": "John", "age": 30,}')
    result = json_splitter.get_nodes_from_documents([input_text])
    assert result == []
