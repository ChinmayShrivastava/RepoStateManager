def resolve_from_aliases(*args: Optional[str]) -> Optional[str]:
    for arg in args:
        if arg is not None:
            return arg
    return None
