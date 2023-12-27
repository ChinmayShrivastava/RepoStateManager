def register_init_cli(subparsers: _SubParsersAction) -> None:
    """Register subcommand "init" to ArgumentParser."""
    parser = subparsers.add_parser("init")
    parser.add_argument(
        "directory",
        default=".",
        nargs="?",
        help="Directory to init",
    )

    parser.set_defaults(func=init_cli)
