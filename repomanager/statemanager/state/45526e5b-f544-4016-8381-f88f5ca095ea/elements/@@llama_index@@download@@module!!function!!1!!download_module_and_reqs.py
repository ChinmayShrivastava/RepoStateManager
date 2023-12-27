def download_module_and_reqs(
    local_dir_path: PATH_TYPE,
    remote_dir_path: PATH_TYPE,
    module_id: str,
    extra_files: List[str],
    refresh_cache: bool = False,
    use_gpt_index_import: bool = False,
    base_file_name: str = "base.py",
    override_path: bool = False,
) -> None:
    """Load module."""
    if isinstance(local_dir_path, str):
        local_dir_path = Path(local_dir_path)

    if override_path:
        module_path = str(local_dir_path)
    else:
        module_path = f"{local_dir_path}/{module_id}"

    if refresh_cache or not os.path.exists(module_path):
        os.makedirs(module_path, exist_ok=True)

        basepy_raw_content, _ = get_file_content(
            str(remote_dir_path), f"/{module_id}/{base_file_name}"
        )
        if use_gpt_index_import:
            basepy_raw_content = basepy_raw_content.replace(
                "import llama_index", "import llama_index"
            )
            basepy_raw_content = basepy_raw_content.replace(
                "from llama_index", "from llama_index"
            )

        with open(f"{module_path}/{base_file_name}", "w") as f:
            f.write(basepy_raw_content)

    # Get content of extra files if there are any
    # and write them under the loader directory
    for extra_file in extra_files:
        extra_file_raw_content, _ = get_file_content(
            str(remote_dir_path), f"/{module_id}/{extra_file}"
        )
        # If the extra file is an __init__.py file, we need to
        # add the exports to the __init__.py file in the modules directory
        if extra_file == "__init__.py":
            loader_exports = get_exports(extra_file_raw_content)
            existing_exports = []
            init_file_path = local_dir_path / "__init__.py"
            # if the __init__.py file do not exists, we need to create it
            mode = "a+" if not os.path.exists(init_file_path) else "r+"
            with open(init_file_path, mode) as f:
                f.write(f"from .{module_id} import {', '.join(loader_exports)}")
                existing_exports = get_exports(f.read())
            rewrite_exports(existing_exports + loader_exports, str(local_dir_path))

        with open(f"{module_path}/{extra_file}", "w") as f:
            f.write(extra_file_raw_content)

    # install requirements
    requirements_path = f"{local_dir_path}/requirements.txt"

    if not os.path.exists(requirements_path):
        # NOTE: need to check the status code
        response_txt, status_code = get_file_content(
            str(remote_dir_path), f"/{module_id}/requirements.txt"
        )
        if status_code == 200:
            with open(requirements_path, "w") as f:
                f.write(response_txt)

    # Install dependencies if there are any and not already installed
    if os.path.exists(requirements_path):
        try:
            requirements = pkg_resources.parse_requirements(
                Path(requirements_path).open()
            )
            pkg_resources.require([str(r) for r in requirements])
        except DistributionNotFound:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", requirements_path]
            )
