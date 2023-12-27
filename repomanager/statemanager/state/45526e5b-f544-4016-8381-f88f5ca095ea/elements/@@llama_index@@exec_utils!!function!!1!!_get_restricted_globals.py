def _get_restricted_globals(__globals: Union[dict, None]) -> Any:
    restricted_globals = copy.deepcopy(ALLOWED_BUILTINS)
    if __globals:
        restricted_globals.update(__globals)
    return restricted_globals
