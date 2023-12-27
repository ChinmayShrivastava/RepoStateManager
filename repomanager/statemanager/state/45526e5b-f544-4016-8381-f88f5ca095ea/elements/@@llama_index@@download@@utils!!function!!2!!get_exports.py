def get_exports(raw_content: str) -> List:
    """Read content of a Python file and returns a list of exported class names.

    For example:
    ```python
    from .a import A
    from .b import B

    __all__ = ["A", "B"]
    ```
    will return `["A", "B"]`.

    Args:
        - raw_content: The content of a Python file as a string.

    Returns:
        A list of exported class names.

    """
    exports = []
    for line in raw_content.splitlines():
        line = line.strip()
        if line.startswith("__all__"):
            exports = line.split("=")[1].strip().strip("[").strip("]").split(",")
            exports = [export.strip().strip("'").strip('"') for export in exports]
    return exports
