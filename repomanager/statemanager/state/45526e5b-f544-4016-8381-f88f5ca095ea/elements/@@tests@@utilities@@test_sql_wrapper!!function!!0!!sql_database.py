def sql_database() -> Generator[SQLDatabase, None, None]:
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()
    table_name = "test_table"
    Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
    )
    metadata.create_all(engine)

    yield SQLDatabase(engine=engine, metadata=metadata, sample_rows_in_table_info=1)

    metadata.drop_all(engine)
