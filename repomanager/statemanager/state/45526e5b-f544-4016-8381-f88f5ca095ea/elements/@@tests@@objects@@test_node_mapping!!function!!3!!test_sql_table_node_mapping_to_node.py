def test_sql_table_node_mapping_to_node(mocker: MockerFixture) -> None:
    """Test to add node for sql table node mapping object to ensure no 'None' values in metadata output to avoid issues with nulls when upserting to indexes."""
    mocker.patch(
        "llama_index.utilities.sql_wrapper.SQLDatabase.get_single_table_info",
        return_value="",
    )

    # Define two table schemas with one that does not have context str defined
    table1 = SQLTableSchema(table_name="table1")
    table2 = SQLTableSchema(table_name="table2", context_str="stuff here")
    tables = [table1, table2]

    # Create the mapping
    sql_database = TestSQLDatabase()
    mapping = SQLTableNodeMapping(sql_database)

    # Create the nodes
    nodes = []
    for table in tables:
        node = mapping.to_node(table)
        nodes.append(node)

    # Make sure no None values are passed in otherwise PineconeVectorStore will fail the upsert
    for node in nodes:
        assert None not in node.metadata.values()
