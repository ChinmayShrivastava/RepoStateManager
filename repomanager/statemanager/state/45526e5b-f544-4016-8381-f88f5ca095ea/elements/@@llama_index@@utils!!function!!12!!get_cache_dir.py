def get_cache_dir() -> str:
    """Locate a platform-appropriate cache directory for llama_index,
    and create it if it doesn't yet exist.
    """
    # User override
    if "LLAMA_INDEX_CACHE_DIR" in os.environ:
        path = Path(os.environ["LLAMA_INDEX_CACHE_DIR"])

    # Linux, Unix, AIX, etc.
    elif os.name == "posix" and sys.platform != "darwin":
        path = Path("/tmp/llama_index")

    # Mac OS
    elif sys.platform == "darwin":
        path = Path(os.path.expanduser("~"), "Library/Caches/llama_index")

    # Windows (hopefully)
    else:
        local = os.environ.get("LOCALAPPDATA", None) or os.path.expanduser(
            "~\\AppData\\Local"
        )
        path = Path(local, "llama_index")

    if not os.path.exists(path):
        os.makedirs(
            path, exist_ok=True
        )  # prevents https://github.com/jerryjliu/llama_index/issues/7362
    return str(path)
