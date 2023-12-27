def save_config(config: ConfigParser, root: str = ".") -> None:
    """Load configuration to file."""
    with open(os.path.join(root, CONFIG_FILE_NAME), "w") as fd:
        config.write(fd)
