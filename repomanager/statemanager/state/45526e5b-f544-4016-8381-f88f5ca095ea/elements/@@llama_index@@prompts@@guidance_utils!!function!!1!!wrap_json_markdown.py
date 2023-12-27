def wrap_json_markdown(text: str) -> str:
    """Wrap text in json markdown formatting block."""
    return "```json\n" + text + "\n```"
