def get_from_param_or_env_without_error(
    param: Optional[str] = None,
    env_key: Optional[str] = None,
) -> Union[str, None]:
    """Get a value from a param or an environment variable without error."""
    if param is not None:
        return param
    elif env_key and env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    else:
        return None
