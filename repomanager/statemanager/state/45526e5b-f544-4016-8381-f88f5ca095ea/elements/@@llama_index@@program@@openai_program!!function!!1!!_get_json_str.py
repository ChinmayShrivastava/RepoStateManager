def _get_json_str(raw_str: str, start_idx: int) -> Tuple[Optional[str], int]:
    """Extract JSON str from raw string and start index."""
    raw_str = raw_str[start_idx:]
    stack_count = 0
    for i, c in enumerate(raw_str):
        if c == "{":
            stack_count += 1
        if c == "}":
            stack_count -= 1
            if stack_count == 0:
                return raw_str[: i + 1], i + 2 + start_idx

    return None, start_idx
