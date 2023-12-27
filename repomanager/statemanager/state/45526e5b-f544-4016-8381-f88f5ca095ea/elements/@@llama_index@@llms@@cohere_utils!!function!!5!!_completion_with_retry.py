    def _completion_with_retry(**kwargs: Any) -> Any:
        if chat:
            return client.chat(**kwargs)
        else:
            return client.generate(**kwargs)
