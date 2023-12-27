def test_vertex_generate_code() -> None:
    llm = Vertex(model="code-bison")
    output = llm.complete("generate a python method that says foo:", temperature=0.4)
    assert isinstance(output, CompletionResponse)
