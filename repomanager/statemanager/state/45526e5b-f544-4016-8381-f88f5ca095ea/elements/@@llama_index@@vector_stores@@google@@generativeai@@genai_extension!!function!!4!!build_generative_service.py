def build_generative_service() -> genai.GenerativeServiceClient:
    credentials = _get_credentials()
    return genai.GenerativeServiceClient(
        credentials=credentials,
        client_info=gapic_v1.client_info.ClientInfo(user_agent=_USER_AGENT),
        client_options=client_options_lib.ClientOptions(
            api_endpoint=_config.api_endpoint
        ),
    )
