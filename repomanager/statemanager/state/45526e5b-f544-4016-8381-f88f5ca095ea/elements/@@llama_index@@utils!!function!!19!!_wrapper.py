    def _wrapper(*args: Any, **kwds: Any) -> Any:
        return asyncio.get_event_loop().run_until_complete(func(*args, **kwds))
