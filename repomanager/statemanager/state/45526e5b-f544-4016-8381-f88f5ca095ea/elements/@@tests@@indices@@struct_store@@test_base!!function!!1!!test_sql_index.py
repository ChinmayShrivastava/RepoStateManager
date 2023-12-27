def test_sql_index(
    mock_service_context: ServiceContext,
    struct_kwargs: Tuple[Dict, Dict],
) -> None:
    """Test SQLStructStoreIndex."""
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
    docs = [Document(text="user_id:2,foo:bar"), Document(text="user_id:8,foo:hello")]
    sql_database = SQLDatabase(engine, metadata=metadata_obj)
    index = SQLStructStoreIndex.from_documents(
        docs,
        sql_database=sql_database,
        table_name=table_name,
        service_context=mock_service_context,
        **index_kwargs
    )
    assert isinstance(index, SQLStructStoreIndex)

    # test that the document is inserted
    stmt = select(test_table.c.user_id, test_table.c.foo)
    engine = index.sql_database.engine
    with engine.connect() as connection:
        results = connection.execute(stmt).fetchall()
        print(results)
        assert results == [(2, "bar"), (8, "hello")]

    # try with documents with more text chunks
    _delete_table_items(engine, test_table)
    docs = [Document(text="user_id:2,foo:bar\nuser_id:8,foo:hello")]
    index = SQLStructStoreIndex.from_documents(
        docs, sql_database=sql_database, table_name=table_name, **index_kwargs
    )
    assert isinstance(index, SQLStructStoreIndex)
    # test that the document is inserted
    stmt = select(test_table.c.user_id, test_table.c.foo)
    engine = index.sql_database.engine
    with engine.begin() as connection:
        results = connection.execute(stmt).fetchall()
        assert results == [(8, "hello")]
