def _get_base_url(*, base_url: typing.Optional[str] = None, environment: SuperagentEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
