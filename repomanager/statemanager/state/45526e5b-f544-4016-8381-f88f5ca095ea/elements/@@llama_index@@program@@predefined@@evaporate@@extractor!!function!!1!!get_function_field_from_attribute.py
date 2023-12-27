def get_function_field_from_attribute(attribute: str) -> str:
    """Get function field from attribute.

    NOTE: copied from https://github.com/HazyResearch/evaporate.

    """
    return re.sub(r"[^A-Za-z0-9]", "_", attribute)
