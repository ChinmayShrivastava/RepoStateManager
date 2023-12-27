def test_split_valid_dict_json() -> None:
    json_splitter = JSONNodeParser()
    input_text = Document(text='{"name": "John", "age": 30}')
    result = json_splitter.get_nodes_from_documents([input_text])
    assert len(result) == 1
    assert result[0].text == "name John\nage 30"
