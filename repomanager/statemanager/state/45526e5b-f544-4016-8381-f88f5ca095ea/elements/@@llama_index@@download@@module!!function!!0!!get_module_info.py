def get_module_info(
    local_dir_path: PATH_TYPE,
    remote_dir_path: PATH_TYPE,
    module_class: str,
    refresh_cache: bool = False,
    library_path: str = "library.json",
    disable_library_cache: bool = False,
) -> Dict:
    """Get module info."""
    if isinstance(local_dir_path, str):
        local_dir_path = Path(local_dir_path)

    local_library_path = f"{local_dir_path}/{library_path}"
    module_id = None  # e.g. `web/simple_web`
    extra_files = []  # e.g. `web/simple_web/utils.py`

    # Check cache first
    if not refresh_cache and os.path.exists(local_library_path):
        with open(local_library_path) as f:
            library = json.load(f)
        if module_class in library:
            module_id = library[module_class]["id"]
            extra_files = library[module_class].get("extra_files", [])

    # Fetch up-to-date library from remote repo if module_id not found
    if module_id is None:
        library_raw_content, _ = get_file_content(
            str(remote_dir_path), f"/{library_path}"
        )
        library = json.loads(library_raw_content)
        if module_class not in library:
            raise ValueError("Loader class name not found in library")

        module_id = library[module_class]["id"]
        extra_files = library[module_class].get("extra_files", [])

        # create cache dir if needed
        local_library_dir = os.path.dirname(local_library_path)
        if not disable_library_cache:
            if not os.path.exists(local_library_dir):
                os.makedirs(local_library_dir)

            # Update cache
            with open(local_library_path, "w") as f:
                f.write(library_raw_content)

    if module_id is None:
        raise ValueError("Loader class name not found in library")

    return {
        "module_id": module_id,
        "extra_files": extra_files,
    }
