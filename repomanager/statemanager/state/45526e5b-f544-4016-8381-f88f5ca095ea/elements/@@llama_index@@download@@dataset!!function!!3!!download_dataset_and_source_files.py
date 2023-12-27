def download_dataset_and_source_files(
    local_dir_path: PATH_TYPE,
    remote_lfs_dir_path: PATH_TYPE,
    source_files_dir_path: PATH_TYPE,
    dataset_id: str,
    dataset_class_name: str,
    source_files: List[str],
    refresh_cache: bool = False,
    base_file_name: str = "rag_dataset.json",
    override_path: bool = False,
    show_progress: bool = False,
) -> None:
    """Download dataset and source files."""
    if isinstance(local_dir_path, str):
        local_dir_path = Path(local_dir_path)

    if override_path:
        module_path = str(local_dir_path)
    else:
        module_path = f"{local_dir_path}/{dataset_id}"

    if refresh_cache or not os.path.exists(module_path):
        os.makedirs(module_path, exist_ok=True)

        base_file_name = _resolve_dataset_file_name(dataset_class_name)

        dataset_raw_content, _ = get_file_content(
            str(remote_lfs_dir_path), f"/{dataset_id}/{base_file_name}"
        )

        with open(f"{module_path}/{base_file_name}", "w") as f:
            f.write(dataset_raw_content)

        # Get content of source files
        if dataset_class_name == "LabelledRagDataset":
            os.makedirs(f"{module_path}/{source_files_dir_path}", exist_ok=True)
            if show_progress:
                source_files_iterator = tqdm.tqdm(source_files)
            else:
                source_files_iterator = source_files
            for source_file in source_files_iterator:
                if ".pdf" in source_file:
                    source_file_raw_content_bytes, _ = get_file_content_bytes(
                        str(remote_lfs_dir_path),
                        f"/{dataset_id}/{source_files_dir_path}/{source_file}",
                    )
                    with open(
                        f"{module_path}/{source_files_dir_path}/{source_file}", "wb"
                    ) as f:
                        f.write(source_file_raw_content_bytes)
                else:
                    source_file_raw_content, _ = get_file_content(
                        str(remote_lfs_dir_path),
                        f"/{dataset_id}/{source_files_dir_path}/{source_file}",
                    )
                    with open(
                        f"{module_path}/{source_files_dir_path}/{source_file}", "w"
                    ) as f:
                        f.write(source_file_raw_content)
