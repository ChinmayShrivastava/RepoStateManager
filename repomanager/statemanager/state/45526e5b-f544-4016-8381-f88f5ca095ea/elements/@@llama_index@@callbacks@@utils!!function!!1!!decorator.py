    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)  # preserve signature, name, etc. of func
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            try:
                callback_manager = getattr(self, callback_manager_attr)
            except AttributeError:
                logger.warning(
                    "Could not find attribute %s on %s.",
                    callback_manager_attr,
                    type(self),
                )
                return func(self, *args, **kwargs)
            callback_manager = cast(CallbackManager, callback_manager)
            with callback_manager.as_trace(trace_id):
                return func(self, *args, **kwargs)

        @functools.wraps(func)  # preserve signature, name, etc. of func
        async def async_wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            try:
                callback_manager = getattr(self, callback_manager_attr)
            except AttributeError:
                logger.warning(
                    "Could not find attribute %s on %s.",
                    callback_manager_attr,
                    type(self),
                )
                return await func(self, *args, **kwargs)
            callback_manager = cast(CallbackManager, callback_manager)
            with callback_manager.as_trace(trace_id):
                return await func(self, *args, **kwargs)

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper
