def _get_rockset() -> ModuleType:
    """Gets the rockset module and raises an ImportError if
    the rockset package hasn't been installed.

    Returns:
        rockset module (ModuleType)
    """
    try:
        import rockset
    except ImportError:
        raise ImportError("Please install rockset with `pip install rockset`")
    return rockset
