def create_indexes(spider_dir: str, llm: OpenAI) -> Dict[str, SQLStructStoreIndex]:
    """Create indexes for all databases."""
    # Create all necessary SQL database objects.
    databases = {}
    for db_name in os.listdir(os.path.join(spider_dir, "database")):
        db_path = os.path.join(spider_dir, "database", db_name, db_name + ".sqlite")
        if not os.path.exists(db_path):
            continue
        engine = create_engine("sqlite:///" + db_path)
        databases[db_name] = SQLDatabase(engine=engine)
        # Test connection.
        with engine.connect() as connection:
            connection.execute(
                text("select name from sqlite_master where type = 'table'")
            ).fetchone()

    llm_predictor = LLMPredictor(llm=llm)
    llm_indexes = {}
    for db_name, db in databases.items():
        llm_indexes[db_name] = SQLStructStoreIndex(
            llm_predictor=llm_predictor,
            sql_database=db,
        )
    return llm_indexes
