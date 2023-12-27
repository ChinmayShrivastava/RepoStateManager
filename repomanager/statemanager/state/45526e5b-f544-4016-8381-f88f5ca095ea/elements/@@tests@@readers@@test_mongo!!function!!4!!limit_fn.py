        def limit_fn(limit: int, *_args: Any, **_kwargs: Any) -> List[Dict[str, str]]:
            if limit == 0:
                return mock_cursor
            return mock_cursor[:limit]
