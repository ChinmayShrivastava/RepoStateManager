def test_sql_index_async_query(
    allow_networking: Any,
    mock_service_context: ServiceContext,
    struct_kwargs: Tuple[Dict, Dict],
) -> None:
    """Test SQLStructStoreIndex."""
    index_kwargs, query_kwargs = struct_kwargs
    docs = [Document(text="user_id:2,foo:bar"), Document(text="user_id:8,foo:hello")]
    engine = create_engine("sqlite:///:memory:")
    metadata_obj = MetaData()
    table_name = "test_table"
    # NOTE: table is created by tying to metadata_obj
    Table(
        table_name,
        metadata_obj,
        Column("user_id", Integer, primary_key=True),
        Column("foo", String(16), nullable=False),
    )
    metadata_obj.create_all(engine)
    sql_database = SQLDatabase(engine)
    # NOTE: we can use the default output parser for this
    index = SQLStructStoreIndex.from_documents(
        docs,
        sql_database=sql_database,
        table_name=table_name,
        service_context=mock_service_context,
        **index_kwargs
    )

    sql_to_test = "SELECT user_id, foo FROM test_table"
    # query the index with SQL
    sql_query_engine = SQLStructStoreQueryEngine(index, **query_kwargs)
    task = sql_query_engine.aquery(sql_to_test)
    response = asyncio.run(task)
    assert str(response) == "[(2, 'bar'), (8, 'hello')]"

    # query the index with natural language
    nl_query_engine = NLStructStoreQueryEngine(index, **query_kwargs)
    task = nl_query_engine.aquery("test_table:user_id,foo")
    response = asyncio.run(task)
    assert str(response) == "[(2, 'bar'), (8, 'hello')]"

    nl_table_engine = NLSQLTableQueryEngine(index.sql_database)
    task = nl_table_engine.aquery("test_table:user_id,foo")
    response = asyncio.run(task)
    assert str(response) == "[(2, 'bar'), (8, 'hello')]"

    ## sql_only = True  ###
    # query the index with SQL
    sql_query_engine = SQLStructStoreQueryEngine(index, sql_only=True, **query_kwargs)
    task = sql_query_engine.aquery(sql_to_test)
    response = asyncio.run(task)
    assert str(response) == sql_to_test

    # query the index with natural language
    nl_query_engine = NLStructStoreQueryEngine(index, sql_only=True, **query_kwargs)
    task = nl_query_engine.aquery("test_table:user_id,foo")
    response = asyncio.run(task)
    assert str(response) == sql_to_test

    nl_table_engine = NLSQLTableQueryEngine(index.sql_database, sql_only=True)
    task = nl_table_engine.aquery("test_table:user_id,foo")
    response = asyncio.run(task)
    assert str(response) == sql_to_test
