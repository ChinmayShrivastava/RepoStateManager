def test_init(sql_database: SQLDatabase) -> None:
    assert sql_database.engine
    assert isinstance(sql_database.metadata_obj, MetaData)
