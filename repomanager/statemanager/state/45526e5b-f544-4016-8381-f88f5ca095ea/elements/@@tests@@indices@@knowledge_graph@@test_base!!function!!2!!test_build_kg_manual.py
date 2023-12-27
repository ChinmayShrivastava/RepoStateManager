def test_build_kg_manual(
    _patch_extract_triplets: Any,
    mock_service_context: ServiceContext,
) -> None:
    """Test build knowledge graph."""
    index = KnowledgeGraphIndex([], service_context=mock_service_context)
    tuples = [
        ("foo", "is", "bar"),
        ("hello", "is not", "world"),
        ("Jane", "is mother of", "Bob"),
    ]
    nodes = [TextNode(text=str(tup)) for tup in tuples]
    for tup, node in zip(tuples, nodes):
        # add node
        index.add_node([tup[0], tup[2]], node)
        # add triplet
        index.upsert_triplet(tup)

    # NOTE: in these unit tests, document text == triplets
    docstore_nodes = index.docstore.get_nodes(list(index.index_struct.node_ids))
    table_chunks = {n.get_content() for n in docstore_nodes}
    assert len(table_chunks) == 3
    assert "('foo', 'is', 'bar')" in table_chunks
    assert "('hello', 'is not', 'world')" in table_chunks
    assert "('Jane', 'is mother of', 'Bob')" in table_chunks

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

    # test upsert_triplet_and_node
    index = KnowledgeGraphIndex([], service_context=mock_service_context)
    tuples = [
        ("foo", "is", "bar"),
        ("hello", "is not", "world"),
        ("Jane", "is mother of", "Bob"),
    ]
    nodes = [TextNode(text=str(tup)) for tup in tuples]
    for tup, node in zip(tuples, nodes):
        index.upsert_triplet_and_node(tup, node)

    # NOTE: in these unit tests, document text == triplets
    docstore_nodes = index.docstore.get_nodes(list(index.index_struct.node_ids))
    table_chunks = {n.get_content() for n in docstore_nodes}
    assert len(table_chunks) == 3
    assert "('foo', 'is', 'bar')" in table_chunks
    assert "('hello', 'is not', 'world')" in table_chunks
    assert "('Jane', 'is mother of', 'Bob')" in table_chunks

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

    # try inserting same node twice
    index = KnowledgeGraphIndex([], service_context=mock_service_context)
    node = TextNode(text=str(("foo", "is", "bar")), id_="test_node")
    index.upsert_triplet_and_node(tup, node)
    index.upsert_triplet_and_node(tup, node)
