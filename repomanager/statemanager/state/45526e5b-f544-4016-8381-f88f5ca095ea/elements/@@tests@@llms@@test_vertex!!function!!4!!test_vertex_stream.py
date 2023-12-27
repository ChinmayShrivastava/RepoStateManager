def test_vertex_stream() -> None:
    llm = Vertex()
    outputs = list(llm.stream_complete("Please say foo:"))
    assert isinstance(outputs[0].text, str)
