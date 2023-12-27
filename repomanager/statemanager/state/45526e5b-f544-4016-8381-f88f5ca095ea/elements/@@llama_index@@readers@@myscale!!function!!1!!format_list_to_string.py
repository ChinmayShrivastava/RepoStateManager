def format_list_to_string(lst: List) -> str:
    return "[" + ",".join(str(item) for item in lst) + "]"
