def test_vertex_generate() -> None:
    llm = Vertex(model="text-bison")
    output = llm.complete("hello", temperature=0.4, candidate_count=2)
    assert isinstance(output, CompletionResponse)
