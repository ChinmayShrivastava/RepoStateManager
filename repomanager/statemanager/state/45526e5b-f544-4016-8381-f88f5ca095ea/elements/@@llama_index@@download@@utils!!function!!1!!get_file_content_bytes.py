def get_file_content_bytes(url: str, path: str) -> Tuple[bytes, int]:
    """Get the content of a file from the GitHub REST API."""
    resp = requests.get(url + path)
    return resp.content, resp.status_code
