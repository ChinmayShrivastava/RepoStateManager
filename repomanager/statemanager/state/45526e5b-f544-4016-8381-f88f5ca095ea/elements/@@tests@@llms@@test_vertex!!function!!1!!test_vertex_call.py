def test_vertex_call() -> None:
    llm = Vertex(temperature=0)
    output = llm.complete("Say foo:")
    assert isinstance(output.text, str)
