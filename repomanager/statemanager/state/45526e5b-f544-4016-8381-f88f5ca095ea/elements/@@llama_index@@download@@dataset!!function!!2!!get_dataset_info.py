def get_dataset_info(
    local_dir_path: PATH_TYPE,
    remote_dir_path: PATH_TYPE,
    remote_source_dir_path: PATH_TYPE,
    dataset_class: str,
    refresh_cache: bool = False,
    library_path: str = "library.json",
    source_files_path: str = "source_files",
    disable_library_cache: bool = False,
) -> Dict:
    """Get dataset info."""
    if isinstance(local_dir_path, str):
        local_dir_path = Path(local_dir_path)

    local_library_path = f"{local_dir_path}/{library_path}"
    dataset_id = None
    source_files = []

    # Check cache first
    if not refresh_cache and os.path.exists(local_library_path):
        with open(local_library_path) as f:
            library = json.load(f)
        if dataset_class in library:
            dataset_id = library[dataset_class]["id"]
            source_files = library[dataset_class].get("source_files", [])

    # Fetch up-to-date library from remote repo if dataset_id not found
    if dataset_id is None:
        library_raw_content, _ = get_file_content(
            str(remote_dir_path), f"/{library_path}"
        )
        library = json.loads(library_raw_content)
        if dataset_class not in library:
            raise ValueError("Loader class name not found in library")

        dataset_id = library[dataset_class]["id"]

        # get data card
        raw_card_content, _ = get_file_content(
            str(remote_dir_path), f"/{dataset_id}/card.json"
        )
        card = json.loads(raw_card_content)
        dataset_class_name = card["className"]

        source_files = []
        if dataset_class_name == "LabelledRagDataset":
            source_files = _get_source_files_list(
                str(remote_source_dir_path), f"/{dataset_id}/{source_files_path}"
            )

        # create cache dir if needed
        local_library_dir = os.path.dirname(local_library_path)
        if not disable_library_cache:
            if not os.path.exists(local_library_dir):
                os.makedirs(local_library_dir)

            # Update cache
            with open(local_library_path, "w") as f:
                f.write(library_raw_content)

    if dataset_id is None:
        raise ValueError("Dataset class name not found in library")

    return {
        "dataset_id": dataset_id,
        "dataset_class_name": dataset_class_name,
        "source_files": source_files,
    }
