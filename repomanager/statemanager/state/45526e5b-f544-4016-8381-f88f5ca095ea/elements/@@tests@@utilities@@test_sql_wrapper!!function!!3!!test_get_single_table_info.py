def test_get_single_table_info(sql_database: SQLDatabase) -> None:
    assert sql_database.get_single_table_info("test_table") == (
        "Table 'test_table' has columns: "
        "id (INTEGER), "
        "name (VARCHAR), "
        "and foreign keys: ."
    )
