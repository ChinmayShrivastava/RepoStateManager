def get_selector_from_context(
    service_context: ServiceContext, is_multi: bool = False
) -> BaseSelector:
    """Get a selector from a service context. Prefers Pydantic selectors if possible."""
    selector: Optional[BaseSelector] = None

    if is_multi:
        try:
            llm = service_context.llm
            selector = PydanticMultiSelector.from_defaults(llm=llm)  # type: ignore
        except ValueError:
            selector = LLMMultiSelector.from_defaults(service_context=service_context)
    else:
        try:
            llm = service_context.llm
            selector = PydanticSingleSelector.from_defaults(llm=llm)  # type: ignore
        except ValueError:
            selector = LLMSingleSelector.from_defaults(service_context=service_context)

    assert selector is not None

    return selector
