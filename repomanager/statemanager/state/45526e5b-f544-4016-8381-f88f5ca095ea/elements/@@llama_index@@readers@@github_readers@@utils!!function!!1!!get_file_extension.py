def get_file_extension(filename: str) -> str:
    """Get file extension."""
    return f".{os.path.splitext(filename)[1][1:].lower()}"
