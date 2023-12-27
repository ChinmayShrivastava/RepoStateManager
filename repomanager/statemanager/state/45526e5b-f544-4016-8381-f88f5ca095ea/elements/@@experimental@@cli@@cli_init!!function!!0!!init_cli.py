def init_cli(args: Namespace) -> None:
    """Handle subcommand "init"."""
    config = load_config(args.directory)
    save_config(config, args.directory)
