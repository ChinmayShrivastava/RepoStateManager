def add_cli(args: Namespace) -> None:
    """Handle subcommand "add"."""
    index = load_index()

    for p in args.files:
        if not os.path.exists(p):
            raise FileNotFoundError(p)
        if os.path.isdir(p):
            documents = SimpleDirectoryReader(p).load_data()
            for document in documents:
                index.insert(document)
        else:
            documents = SimpleDirectoryReader(input_files=[p]).load_data()
            for document in documents:
                index.insert(document)

    save_index(index)
