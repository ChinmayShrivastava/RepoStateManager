def test_retreiver_tool() -> None:
    doc1 = Document(
        text=("# title1:Hello world.\n" "This is a test.\n"),
        metadata={"file_path": "/data/personal/essay.md"},
    )

    doc2 = Document(
        text=("# title2:This is another test.\n" "This is a test v2."),
        metadata={"file_path": "/data/personal/essay.md"},
    )
    service_context = ServiceContext.from_defaults(
        llm=None, embed_model=MockEmbedding(embed_dim=1)
    )
    vs_index = VectorStoreIndex.from_documents(
        [doc1, doc2], service_context=service_context
    )
    vs_retriever = vs_index.as_retriever()
    vs_ret_tool = RetrieverTool(
        retriever=vs_retriever,
        metadata=ToolMetadata(
            name="knowledgebase",
            description="test",
        ),
    )
    output = vs_ret_tool.call("arg1", "arg2", key1="v1", key2="v2")
    formated_doc = (
        "file_path = /data/personal/essay.md\n"
        "# title1:Hello world.\n"
        "This is a test."
    )
    assert formated_doc in output.content
