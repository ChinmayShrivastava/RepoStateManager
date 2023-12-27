def _get_source_files_list(source_tree_url: str, path: str) -> List[str]:
    """Get the list of source files to download."""
    resp = requests.get(source_tree_url + path + "?recursive=1")
    payload = resp.json()["payload"]
    return [item["name"] for item in payload["tree"]["items"]]
