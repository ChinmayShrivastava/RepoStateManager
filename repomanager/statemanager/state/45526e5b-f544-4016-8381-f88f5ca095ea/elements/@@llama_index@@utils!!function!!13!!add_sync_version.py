def add_sync_version(func: Any) -> Any:
    """Decorator for adding sync version of an async function. The sync version
    is added as a function attribute to the original function, func.

    Args:
        func(Any): the async function for which a sync variant will be built.
    """
    assert asyncio.iscoroutinefunction(func)

    @wraps(func)
    def _wrapper(*args: Any, **kwds: Any) -> Any:
        return asyncio.get_event_loop().run_until_complete(func(*args, **kwds))

    func.sync = _wrapper
    return func
