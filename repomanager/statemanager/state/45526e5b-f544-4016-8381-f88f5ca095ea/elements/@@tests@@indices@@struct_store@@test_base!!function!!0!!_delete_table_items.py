def _delete_table_items(engine: Any, table: Table) -> None:
    """Delete items from a table."""
    delete_stmt = delete(table)
    with engine.begin() as connection:
        connection.execute(delete_stmt)
