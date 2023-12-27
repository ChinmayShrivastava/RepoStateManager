def init_vertexai(
    project: Optional[str] = None,
    location: Optional[str] = None,
    credentials: Optional[Any] = None,
) -> None:
    """Init vertexai.

    Args:
        project: The default GCP project to use when making Vertex API calls.
        location: The default location to use when making API calls.
        credentials: The default custom
            credentials to use when making API calls. If not provided credentials
            will be ascertained from the environment.

    Raises:
        ImportError: If importing vertexai SDK did not succeed.
    """
    try:
        import vertexai
    except ImportError:
        raise (ValueError(f"Please install vertex AI client by following the steps"))

    vertexai.init(
        project=project,
        location=location,
        credentials=credentials,
    )
