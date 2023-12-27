def get_file_content(url: str, path: str) -> Tuple[str, int]:
    """Get the content of a file from the GitHub REST API."""
    resp = requests.get(url + path)
    return resp.text, resp.status_code
