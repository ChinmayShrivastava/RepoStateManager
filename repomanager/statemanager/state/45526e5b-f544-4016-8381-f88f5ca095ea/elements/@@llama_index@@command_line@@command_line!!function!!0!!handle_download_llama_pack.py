def handle_download_llama_pack(
    llama_pack_class: Optional[str] = None,
    download_dir: Optional[str] = None,
    llama_hub_url: str = LLAMA_HUB_URL,
    **kwargs: Any,
) -> None:
    assert llama_pack_class is not None
    assert download_dir is not None

    download_llama_pack(
        llama_pack_class=llama_pack_class,
        download_dir=download_dir,
        llama_hub_url=llama_hub_url,
    )
    print(f"Successfully downloaded {llama_pack_class} to {download_dir}")
