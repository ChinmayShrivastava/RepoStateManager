    def patched_sync(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func_async(*args, **kwargs))
