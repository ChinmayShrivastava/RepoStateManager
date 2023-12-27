def track_download(module_class: str, module_type: str) -> None:
    """Tracks number of downloads via Llamahub proxy.

    Args:
        module_class: The name of the llama module being downloaded, e.g.,`GmailOpenAIAgentPack`.
        module_type: Can be "loader", "tool", "llamapack", or "datasets"
    """
    try:
        requests.post(
            LLAMAHUB_ANALYTICS_PROXY_SERVER,
            json={"type": module_type, "plugin": module_class},
        )
    except Exception as e:
        logger.info(f"Error tracking downloads for {module_class} : {e}")
