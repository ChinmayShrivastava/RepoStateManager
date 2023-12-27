def get_zcp_type(value: Any) -> str:
    if isinstance(value, str):
        return "VarChar"
    elif isinstance(value, bool):
        return "Bool"
    elif isinstance(value, int):
        return "Int64"
    elif isinstance(value, float):
        return "Double"
    else:
        raise TypeError(
            "Invalid data type of metadata: must be str, bool, int, or float."
        )
