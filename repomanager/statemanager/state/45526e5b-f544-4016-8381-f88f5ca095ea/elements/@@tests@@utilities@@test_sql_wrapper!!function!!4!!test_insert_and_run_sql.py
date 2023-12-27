def test_insert_and_run_sql(sql_database: SQLDatabase) -> None:
    result_str, _ = sql_database.run_sql("SELECT * FROM test_table;")
    assert result_str == "[]"

    sql_database.insert_into_table("test_table", {"id": 1, "name": "Paul McCartney"})

    result_str, _ = sql_database.run_sql("SELECT * FROM test_table;")

    assert result_str == "[(1, 'Paul McCartney')]"
