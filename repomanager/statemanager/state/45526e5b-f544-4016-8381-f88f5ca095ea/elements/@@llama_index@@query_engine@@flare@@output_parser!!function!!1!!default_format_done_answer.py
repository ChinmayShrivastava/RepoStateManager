def default_format_done_answer(response: str) -> str:
    """Default format done answer."""
    return response.replace("done", "").strip()
