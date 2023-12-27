def _process_files(client: Any, files: List[str]) -> Dict[str, str]:
    """Process files."""
    from openai import OpenAI

    client = cast(OpenAI, client)

    file_dict = {}
    for file in files:
        file_obj = client.files.create(file=open(file, "rb"), purpose="assistants")
        file_dict[file_obj.id] = file
    return file_dict
