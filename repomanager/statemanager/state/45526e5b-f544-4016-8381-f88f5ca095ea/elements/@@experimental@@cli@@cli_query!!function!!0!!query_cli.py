def query_cli(args: Namespace) -> None:
    """Handle subcommand "query"."""
    index = load_index()
    query_engine = index.as_query_engine()
    print(query_engine.query(args.query))
