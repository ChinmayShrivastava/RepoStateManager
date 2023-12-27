def test_build_kg(
    _patch_extract_triplets: Any,
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test build knowledge graph."""
    index = KnowledgeGraphIndex.from_documents(
        documents, service_context=mock_service_context
    )
    # NOTE: in these unit tests, document text == triplets
    nodes = index.docstore.get_nodes(list(index.index_struct.node_ids))
    table_chunks = {n.get_content() for n in nodes}
    assert len(table_chunks) == 3
    assert "(foo, is, bar)" in table_chunks
    assert "(hello, is not, world)" in table_chunks
    assert "(Jane, is mother of, Bob)" in table_chunks

    # test that expected keys are present in table
    # NOTE: in mock keyword extractor, stopwords are not filtered
    assert index.index_struct.table.keys() == {
        "foo",
        "bar",
        "hello",
        "world",
        "Jane",
        "Bob",
    }

    # test ref doc info for three nodes, single doc
    all_ref_doc_info = index.ref_doc_info
    assert len(all_ref_doc_info) == 1
    for ref_doc_info in all_ref_doc_info.values():
        assert len(ref_doc_info.node_ids) == 3
