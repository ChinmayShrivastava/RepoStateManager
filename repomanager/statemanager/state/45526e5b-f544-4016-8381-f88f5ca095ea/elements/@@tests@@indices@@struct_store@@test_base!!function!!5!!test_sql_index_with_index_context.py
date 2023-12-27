def test_sql_index_with_index_context(
    mock_service_context: ServiceContext,
    struct_kwargs: Tuple[Dict, Dict],
) -> None:
    """Test SQLStructStoreIndex."""
    # test setting table_context_dict
    engine = create_engine("sqlite:///:memory:")
    metadata_obj = MetaData()
    table_name = "test_table"
    Table(
        table_name,
        metadata_obj,
        Column("user_id", Integer, primary_key=True),
        Column("foo", String(16), nullable=False),
    )
    metadata_obj.create_all(engine)
    # NOTE: we can use the default output parser for this
    index_kwargs, _ = struct_kwargs
    docs = [Document(text="user_id:2,foo:bar"), Document(text="user_id:8,foo:hello")]
    sql_database = SQLDatabase(engine)
    table_context_dict = {"test_table": "test_table_context"}

    context_builder = SQLContextContainerBuilder(
        sql_database, context_dict=table_context_dict
    )
    context_index = context_builder.derive_index_from_context(
        SummaryIndex, ignore_db_schema=True
    )
    # NOTE: the response only contains the first line (metadata), since
    # with the mock patch, newlines are treated as separate calls.
    context_response = context_builder.query_index_for_context(
        context_index,
        "Context query?",
        query_tmpl="{orig_query_str}",
        store_context_str=True,
    )
    sql_context_container = context_builder.build_context_container(
        ignore_db_schema=True
    )
    print(context_response)
    assert (
        context_response == "Context query?:table_name: test_table:test_table_context"
    )
    assert sql_context_container.context_str == context_response

    index = SQLStructStoreIndex.from_documents(
        docs,
        sql_database=sql_database,
        table_name=table_name,
        sql_context_container=sql_context_container,
        service_context=mock_service_context,
        **index_kwargs
    )
    # just assert this runs
    sql_query_engine = NLStructStoreQueryEngine(index)
    sql_query_engine.query(QueryBundle("test_table:foo"))
