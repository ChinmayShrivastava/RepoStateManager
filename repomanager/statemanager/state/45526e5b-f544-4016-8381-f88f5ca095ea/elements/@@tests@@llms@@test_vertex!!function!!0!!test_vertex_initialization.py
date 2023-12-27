def test_vertex_initialization() -> None:
    llm = Vertex()
    assert llm.class_name() == "Vertex"
    assert llm.model == llm._client._model_id
