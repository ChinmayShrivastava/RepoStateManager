def rewrite_exports(exports: List[str], dirpath: str) -> None:
    """Write the `__all__` variable to the `__init__.py` file in the modules dir.

    Removes the line that contains `__all__` and appends a new line with the updated
    `__all__` variable.

    Args:
        - exports: A list of exported class names.

    """
    init_path = f"{dirpath}/__init__.py"
    with open(init_path) as f:
        lines = f.readlines()
    with open(init_path, "w") as f:
        for line in lines:
            line = line.strip()
            if line.startswith("__all__"):
                continue
            f.write(line + os.linesep)
        f.write(f"__all__ = {list(set(exports))}" + os.linesep)
