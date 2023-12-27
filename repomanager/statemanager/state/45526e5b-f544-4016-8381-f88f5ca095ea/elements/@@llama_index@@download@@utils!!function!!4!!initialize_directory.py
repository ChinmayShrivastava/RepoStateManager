def initialize_directory(
    custom_path: Optional[str] = None, custom_dir: Optional[str] = None
) -> Path:
    """Initialize directory."""
    if custom_path is not None and custom_dir is not None:
        raise ValueError(
            "You cannot specify both `custom_path` and `custom_dir` at the same time."
        )

    custom_dir = custom_dir or "llamadatasets"
    if custom_path is not None:
        dirpath = Path(custom_path)
    else:
        dirpath = Path(__file__).parent / custom_dir
    if not os.path.exists(dirpath):
        # Create a new directory because it does not exist
        os.makedirs(dirpath)

    return dirpath
