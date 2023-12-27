def register_add_cli(subparsers: _SubParsersAction) -> None:
    """Register subcommand "add" to ArgumentParser."""
    parser = subparsers.add_parser("add")
    parser.add_argument(
        "files",
        default=".",
        nargs="+",
        help="Files to add",
    )

    parser.set_defaults(func=add_cli)
