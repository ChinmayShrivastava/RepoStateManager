def test_sql_index_with_derive_index(mock_service_context: ServiceContext) -> None:
    """Test derive index."""
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
    sql_database = SQLDatabase(engine)
    table_context_dict = {"test_table": "test_table_context"}

    context_builder = SQLContextContainerBuilder(
        sql_database, context_dict=table_context_dict
    )
    context_index_no_ignore = context_builder.derive_index_from_context(
        SummaryIndex,
    )
    context_index_with_ignore = context_builder.derive_index_from_context(
        SummaryIndex, ignore_db_schema=True
    )
    assert len(context_index_with_ignore.index_struct.nodes) == 1
    assert len(context_index_no_ignore.index_struct.nodes) > 1
