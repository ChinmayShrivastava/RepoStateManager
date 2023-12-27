def default_parse_is_done_fn(response: str) -> bool:
    """Default parse is done function."""
    return "done" in response.lower()
