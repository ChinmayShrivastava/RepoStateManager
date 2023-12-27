def download_llama_dataset(
    dataset_class: str,
    llama_hub_url: str = LLAMA_HUB_URL,
    llama_datasets_lfs_url: str = LLAMA_DATASETS_LFS_URL,
    llama_datasets_source_files_tree_url: str = LLAMA_DATASETS_SOURCE_FILES_GITHUB_TREE_URL,
    refresh_cache: bool = False,
    custom_dir: Optional[str] = None,
    custom_path: Optional[str] = None,
    source_files_dirpath: str = LLAMA_SOURCE_FILES_PATH,
    library_path: str = "llama_datasets/library.json",
    disable_library_cache: bool = False,
    override_path: bool = False,
    show_progress: bool = False,
) -> Any:
    """
    Download a module from LlamaHub.

    Can be a loader, tool, pack, or more.

    Args:
        loader_class: The name of the llama module class you want to download,
            such as `GmailOpenAIAgentPack`.
        refresh_cache: If true, the local cache will be skipped and the
            loader will be fetched directly from the remote repo.
        custom_dir: Custom dir name to download loader into (under parent folder).
        custom_path: Custom dirpath to download loader into.
        library_path: File name of the library file.
        use_gpt_index_import: If true, the loader files will use
            llama_index as the base dependency. By default (False),
            the loader files use llama_index as the base dependency.
            NOTE: this is a temporary workaround while we fully migrate all usages
            to llama_index.
        is_dataset: whether or not downloading a LlamaDataset

    Returns:
        A Loader, A Pack, An Agent, or A Dataset
    """
    # create directory / get path
    dirpath = initialize_directory(custom_path=custom_path, custom_dir=custom_dir)

    # fetch info from library.json file
    dataset_info = get_dataset_info(
        local_dir_path=dirpath,
        remote_dir_path=llama_hub_url,
        remote_source_dir_path=llama_datasets_source_files_tree_url,
        dataset_class=dataset_class,
        refresh_cache=refresh_cache,
        library_path=library_path,
        disable_library_cache=disable_library_cache,
    )
    dataset_id = dataset_info["dataset_id"]
    source_files = dataset_info["source_files"]
    dataset_class_name = dataset_info["dataset_class_name"]

    dataset_filename = _resolve_dataset_file_name(dataset_class_name)

    download_dataset_and_source_files(
        local_dir_path=dirpath,
        remote_lfs_dir_path=llama_datasets_lfs_url,
        source_files_dir_path=source_files_dirpath,
        dataset_id=dataset_id,
        dataset_class_name=dataset_class_name,
        source_files=source_files,
        refresh_cache=refresh_cache,
        override_path=override_path,
        show_progress=show_progress,
    )

    if override_path:
        module_path = str(dirpath)
    else:
        module_path = f"{dirpath}/{dataset_id}"

    return (
        f"{module_path}/{dataset_filename}",
        f"{module_path}/{LLAMA_SOURCE_FILES_PATH}",
    )
