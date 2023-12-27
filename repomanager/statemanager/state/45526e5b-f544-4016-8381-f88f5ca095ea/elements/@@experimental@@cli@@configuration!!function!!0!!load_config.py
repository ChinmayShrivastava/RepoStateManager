def load_config(root: str = ".") -> ConfigParser:
    """Load configuration from file."""
    config = ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    config.read(os.path.join(root, CONFIG_FILE_NAME))
    return config
