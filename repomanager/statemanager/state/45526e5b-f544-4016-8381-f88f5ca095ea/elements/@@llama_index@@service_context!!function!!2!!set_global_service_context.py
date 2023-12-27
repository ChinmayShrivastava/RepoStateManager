def set_global_service_context(service_context: Optional[ServiceContext]) -> None:
    """Helper function to set the global service context."""
    llama_index.global_service_context = service_context
