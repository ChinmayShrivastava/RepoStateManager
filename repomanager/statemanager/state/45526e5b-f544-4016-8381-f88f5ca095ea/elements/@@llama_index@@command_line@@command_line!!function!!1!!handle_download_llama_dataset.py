def handle_download_llama_dataset(
    llama_dataset_class: Optional[str] = None,
    download_dir: Optional[str] = None,
    llama_hub_url: str = LLAMA_HUB_URL,
    llama_datasets_lfs_url: str = LLAMA_DATASETS_LFS_URL,
    llama_datasets_source_files_tree_url: str = LLAMA_DATASETS_SOURCE_FILES_GITHUB_TREE_URL,
    **kwargs: Any,
) -> None:
    assert llama_dataset_class is not None
    assert download_dir is not None

    download_llama_dataset(
        llama_dataset_class=llama_dataset_class,
        download_dir=download_dir,
        llama_hub_url=llama_hub_url,
        llama_datasets_lfs_url=llama_datasets_lfs_url,
        llama_datasets_source_files_tree_url=llama_datasets_source_files_tree_url,
    )

    print(f"Successfully downloaded {llama_dataset_class} to {download_dir}")
