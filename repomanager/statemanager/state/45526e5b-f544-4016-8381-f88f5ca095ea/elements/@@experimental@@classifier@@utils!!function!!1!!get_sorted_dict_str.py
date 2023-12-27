def get_sorted_dict_str(d: dict) -> str:
    """Get sorted dict string."""
    keys = sorted(d.keys())
    return "\n".join([f"{k}:{d[k]}" for k in keys])
