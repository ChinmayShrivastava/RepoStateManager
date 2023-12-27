def get_responses(
    *args: Any,
    **kwargs: Any,
) -> List[str]:
    """Get responses.

    Sync version of aget_responses.

    """
    return asyncio.run(aget_responses(*args, **kwargs))
