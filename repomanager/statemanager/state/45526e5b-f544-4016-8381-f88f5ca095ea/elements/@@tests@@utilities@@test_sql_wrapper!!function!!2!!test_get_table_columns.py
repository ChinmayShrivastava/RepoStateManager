def test_get_table_columns(sql_database: SQLDatabase) -> None:
    columns = sql_database.get_table_columns("test_table")
    assert [column["name"] for column in columns] == ["id", "name"]
