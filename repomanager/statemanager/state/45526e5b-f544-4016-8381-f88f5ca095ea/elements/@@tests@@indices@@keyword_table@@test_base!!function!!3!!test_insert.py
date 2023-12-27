def test_insert(
    documents: List[Document],
    mock_service_context: ServiceContext,
) -> None:
    """Test insert."""
    table = SimpleKeywordTableIndex([], service_context=mock_service_context)
    assert len(table.index_struct.table.keys()) == 0
    table.insert(documents[0])
    nodes = table.docstore.get_nodes(list(table.index_struct.node_ids))
    table_chunks = {n.get_content() for n in nodes}
    assert "Hello world." in table_chunks
    assert "This is a test." in table_chunks
    assert "This is another test." in table_chunks
    assert "This is a test v2." in table_chunks
    # test that expected keys are present in table
    # NOTE: in mock keyword extractor, stopwords are not filtered
    assert table.index_struct.table.keys() == {
        "this",
        "hello",
        "world",
        "test",
        "another",
        "v2",
        "is",
        "a",
        "v2",
    }

    # test insert with doc_id
    document1 = Document(text="This is", id_="test_id1")
    document2 = Document(text="test v3", id_="test_id2")
    table = SimpleKeywordTableIndex([])
    table.insert(document1)
    table.insert(document2)
    chunk_index1_1 = next(iter(table.index_struct.table["this"]))
    chunk_index1_2 = next(iter(table.index_struct.table["is"]))
    chunk_index2_1 = next(iter(table.index_struct.table["test"]))
    chunk_index2_2 = next(iter(table.index_struct.table["v3"]))
    nodes = table.docstore.get_nodes(
        [chunk_index1_1, chunk_index1_2, chunk_index2_1, chunk_index2_2]
    )
    assert nodes[0].ref_doc_id == "test_id1"
    assert nodes[1].ref_doc_id == "test_id1"
    assert nodes[2].ref_doc_id == "test_id2"
    assert nodes[3].ref_doc_id == "test_id2"
