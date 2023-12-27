def fn_with_exception(
    exception_cls: Optional[Union[Type[Exception], Exception]]
) -> bool:
    """Return true unless exception is specified."""
    global call_count
    call_count += 1
    if exception_cls:
        raise exception_cls
    return True
