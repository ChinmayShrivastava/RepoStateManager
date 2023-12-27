def test_sql_index_nodes(
    mock_service_context: ServiceContext,
    struct_kwargs: Tuple[Dict, Dict],
) -> None:
    """Test SQLStructStoreIndex with nodes."""
    engine = create_engine("sqlite:///:memory:")
    metadata_obj = MetaData()
    table_name = "test_table"
    test_table = Table(
        table_name,
        metadata_obj,
        Column("user_id", Integer, primary_key=True),
        Column("foo", String(16), nullable=False),
    )
    metadata_obj.create_all(engine)
    # NOTE: we can use the default output parser for this
    index_kwargs, _ = struct_kwargs

    # try with different parent ids
    nodes = [
        TextNode(
            text="user_id:2,foo:bar",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test1")},
        ),
        TextNode(
            text="user_id:8,foo:hello",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test2")},
        ),
    ]
    sql_database = SQLDatabase(engine, metadata=metadata_obj)
    index = SQLStructStoreIndex(
        nodes,
        sql_database=sql_database,
        table_name=table_name,
        service_context=mock_service_context,
        **index_kwargs
    )
    assert isinstance(index, SQLStructStoreIndex)

    # test that both nodes are inserted
    stmt = select(test_table.c.user_id, test_table.c.foo)
    engine = index.sql_database.engine
    with engine.connect() as connection:
        results = connection.execute(stmt).fetchall()
        print(results)
        assert results == [(2, "bar"), (8, "hello")]

    _delete_table_items(engine, test_table)

    # try with same parent ids
    nodes = [
        TextNode(
            text="user_id:2,foo:bar",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test1")},
        ),
        TextNode(
            text="user_id:8,foo:hello",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test1")},
        ),
    ]
    sql_database = SQLDatabase(engine, metadata=metadata_obj)
    index = SQLStructStoreIndex(
        nodes,
        sql_database=sql_database,
        table_name=table_name,
        service_context=mock_service_context,
        **index_kwargs
    )
    assert isinstance(index, SQLStructStoreIndex)

    # test that only one node (the last one) is inserted
    stmt = select(test_table.c.user_id, test_table.c.foo)
    engine = index.sql_database.engine
    with engine.connect() as connection:
        results = connection.execute(stmt).fetchall()
        print(results)
        assert results == [(8, "hello")]
