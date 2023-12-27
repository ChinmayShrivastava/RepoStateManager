def test_split_valid_json() -> None:
    json_splitter = JSONNodeParser()
    input_text = Document(
        text='[{"name": "John", "age": 30}, {"name": "Alice", "age": 25}]'
    )
    result = json_splitter.get_nodes_from_documents([input_text])
    assert len(result) == 2
    assert result[0].text == "name John\nage 30"
    assert result[1].text == "name Alice\nage 25"
