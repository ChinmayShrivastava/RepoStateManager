def _get_default_service_context() -> ServiceContext:
    """Get default service context."""
    llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
    return ServiceContext.from_defaults(llm=llm, chunk_size_limit=3000)
