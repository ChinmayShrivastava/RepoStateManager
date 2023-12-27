def register_query_cli(subparsers: _SubParsersAction) -> None:
    """Register subcommand "query" to ArgumentParser."""
    parser = subparsers.add_parser("query")
    parser.add_argument(
        "query",
        help="Query",
    )

    parser.set_defaults(func=query_cli)
