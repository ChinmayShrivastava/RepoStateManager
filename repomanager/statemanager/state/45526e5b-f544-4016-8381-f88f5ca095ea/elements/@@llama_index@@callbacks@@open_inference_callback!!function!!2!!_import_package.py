def _import_package(package_name: str) -> ModuleType:
    """Dynamically imports a package.

    Args:
        package_name (str): Name of the package to import.

    Raises:
        ImportError: If the package is not installed.

    Returns:
        ModuleType: The imported package.
    """
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        raise ImportError(f"The {package_name} package must be installed.")
    return package
