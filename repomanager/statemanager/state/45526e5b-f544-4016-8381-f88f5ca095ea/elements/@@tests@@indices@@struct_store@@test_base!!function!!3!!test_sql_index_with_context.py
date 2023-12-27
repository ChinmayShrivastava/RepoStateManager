def test_sql_index_with_context(
    mock_service_context: ServiceContext,
    struct_kwargs: Tuple[Dict, Dict],
) -> None:
    """Test SQLStructStoreIndex."""
    # test setting table_context_dict
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
    sql_database = SQLDatabase(engine)
    table_context_dict = {"test_table": "test_table_context"}

    # test with ignore_db_schema=True
    sql_context_container = SQLContextContainerBuilder(
        sql_database, context_dict=table_context_dict
    ).build_context_container(ignore_db_schema=True)

    index = SQLStructStoreIndex.from_documents(
        docs,
        sql_database=sql_database,
        table_name=table_name,
        sql_context_container=sql_context_container,
        service_context=mock_service_context,
        **index_kwargs
    )
    assert isinstance(index, SQLStructStoreIndex)
    assert index.sql_context_container.context_dict == table_context_dict
    _delete_table_items(engine, test_table)

    # test with ignore_db_schema=False (default)
    sql_database = SQLDatabase(engine)
    sql_context_container = SQLContextContainerBuilder(
        sql_database, context_dict=table_context_dict
    ).build_context_container()

    index = SQLStructStoreIndex.from_documents(
        docs,
        sql_database=sql_database,
        table_name=table_name,
        sql_context_container=sql_context_container,
        **index_kwargs
    )
    assert isinstance(index, SQLStructStoreIndex)
    for k, v in table_context_dict.items():
        context_dict = index.sql_context_container.context_dict
        assert context_dict is not None
        assert len(context_dict[k]) > len(v)
        assert v in context_dict[k]
    _delete_table_items(engine, test_table)

    # test setting sql_context_builder
    sql_database = SQLDatabase(engine)
    # this should cause the mock QuestionAnswer prompt to run
    context_documents_dict: Dict[str, List[BaseNode]] = {
        "test_table": [Document(text="test_table_context")]
    }
    sql_context_builder = SQLContextContainerBuilder.from_documents(
        context_documents_dict,
        sql_database=sql_database,
        table_context_prompt=MOCK_TABLE_CONTEXT_PROMPT,
        table_context_task="extract_test",
    )
    sql_context_container = sql_context_builder.build_context_container(
        ignore_db_schema=True
    )
    index = SQLStructStoreIndex.from_documents(
        docs,
        sql_database=sql_database,
        table_name=table_name,
        sql_context_container=sql_context_container,
        **index_kwargs
    )
    assert isinstance(index, SQLStructStoreIndex)
    assert index.sql_context_container.context_dict == {
        "test_table": "extract_test:test_table_context"
    }
