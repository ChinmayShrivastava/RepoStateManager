def download_llama_module(
    module_class: str,
    llama_hub_url: str = LLAMA_HUB_URL,
    refresh_cache: bool = False,
    custom_dir: Optional[str] = None,
    custom_path: Optional[str] = None,
    library_path: str = "library.json",
    base_file_name: str = "base.py",
    use_gpt_index_import: bool = False,
    disable_library_cache: bool = False,
    override_path: bool = False,
) -> Any:
    """Download a module from LlamaHub.

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
    module_info = get_module_info(
        local_dir_path=dirpath,
        remote_dir_path=llama_hub_url,
        module_class=module_class,
        refresh_cache=refresh_cache,
        library_path=library_path,
        disable_library_cache=disable_library_cache,
    )
    module_id = module_info["module_id"]
    extra_files = module_info["extra_files"]

    # download the module, install requirements
    download_module_and_reqs(
        local_dir_path=dirpath,
        remote_dir_path=llama_hub_url,
        module_id=module_id,
        extra_files=extra_files,
        refresh_cache=refresh_cache,
        use_gpt_index_import=use_gpt_index_import,
        base_file_name=base_file_name,
        override_path=override_path,
    )

    # loads the module into memory
    if override_path:
        spec = util.spec_from_file_location(
            "custom_module", location=f"{dirpath}/{base_file_name}"
        )
        if spec is None:
            raise ValueError(f"Could not find file: {dirpath}/{base_file_name}.")
    else:
        spec = util.spec_from_file_location(
            "custom_module", location=f"{dirpath}/{module_id}/{base_file_name}"
        )
        if spec is None:
            raise ValueError(
                f"Could not find file: {dirpath}/{module_id}/{base_file_name}."
            )

    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    return getattr(module, module_class)
