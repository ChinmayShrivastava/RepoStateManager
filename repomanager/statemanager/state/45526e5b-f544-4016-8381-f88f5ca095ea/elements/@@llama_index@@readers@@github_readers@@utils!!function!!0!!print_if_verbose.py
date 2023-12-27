def print_if_verbose(verbose: bool, message: str) -> None:
    """Log message if verbose is True."""
    if verbose:
        print(message)
